import sys
from pathlib import Path
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil

# -*- coding: utf-8 -*-
# cspell:words Poppler poppler pdfinfo pdftoppm cwebp webp Pillow

# This script uses Poppler.
# macOS: brew install poppler
# Ubuntu/Debian: sudo apt-get install poppler-utils
# Windows: https://github.com/oschwartz10612/poppler-windows/releases/
# WebP 変換には cwebp (推奨) または Pillow が必要です。
# macOS: brew install webp
# Ubuntu/Debian: sudo apt-get install webp
# Pillow: pip install pillow

def safe_print(*args, **kwargs):
    text = ' '.join(str(a) for a in args)
    text_ascii = text.encode('ascii', 'ignore').decode('ascii')
    print(text_ascii, **kwargs)

def get_pdf_page_count(pdf_path: Path):
    try:
        result = subprocess.run(['pdfinfo', str(pdf_path)], capture_output=True, text=True, errors='replace', check=True)
        for line in result.stdout.splitlines():
            if line.lower().startswith('pages:'):
                return int(line.split(':', 1)[1].strip())
        safe_print("Error: Could not parse page count from pdfinfo.")
    except FileNotFoundError:
        safe_print("Error: 'pdfinfo' command not found. Please ensure Poppler is installed and in PATH.")
    except Exception as e:
        safe_print(f"Error: Failed to get page count: {e}")
    return None

def _convert_single_page(pdf_path: Path, output_prefix: Path, dpi: int, page: int):
    # pdftoppm -png -r {dpi} -f {page} -l {page} input.pdf output_prefix
    cmd = ['pdftoppm', '-png', '-r', str(dpi), '-f', str(page), '-l', str(page), str(pdf_path), str(output_prefix)]
    result = subprocess.run(cmd, capture_output=True, text=True, errors='replace', check=True)
    return result.stderr  # pdftoppm messages may come via stderr

def _show_progress(done: int, total: int, failures: int, prefix: str = "Progress"):
    percent = int(done * 100 / total) if total else 0
    msg = f"\r{prefix}: {done}/{total} ({percent}%) | failures: {failures}"
    safe_print(msg, end='', flush=True)

def _end_progress_line(progress_line_active: list):
    if progress_line_active and progress_line_active[0]:
        print()
        progress_line_active[0] = False

def _choose_webp_converter():
    """
    戻り値: 'cwebp' | 'pillow' | None
    """
    if shutil.which('cwebp'):
        return 'cwebp'
    try:
        from PIL import Image  # noqa: F401
        return 'pillow'
    except Exception:
        return None

def _png_to_webp_cwebp(png_path: Path, webp_path: Path, quality: int, lossless: bool):
    cmd = ['cwebp']
    if lossless:
        cmd += ['-lossless']
    else:
        cmd += ['-q', str(quality)]
    cmd += [str(png_path), '-o', str(webp_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, errors='replace', check=True)
    return result.stderr

def _png_to_webp_pillow(png_path: Path, webp_path: Path, quality: int, lossless: bool):
    from PIL import Image
    with Image.open(png_path) as im:
        im.save(webp_path, 'WEBP', quality=quality, lossless=lossless, method=6)
    return ""  # Pillowは特にstderrなし

def _convert_pngs_to_webp_parallel(output_dir: Path, stem: str):
    png_files = sorted(output_dir.glob(f'{stem}-*.png'))
    if not png_files:
        safe_print("No PNG files to convert to WebP.")
        return

    converter = _choose_webp_converter()
    if not converter:
        safe_print("Error: Neither 'cwebp' nor Pillow is available for WebP conversion.")
        safe_print("Install 'webp' (cwebp) or 'pip install pillow'.")
        return

    quality = int(os.environ.get('PDF2PNG_WEBP_Q', '90'))
    lossless = os.environ.get('PDF2PNG_WEBP_LOSSLESS', '0') in ('1', 'true', 'True')

    max_workers = os.cpu_count() or 1

    safe_print(f"Starting PNG -> WebP conversion in parallel... (files: {len(png_files)}, mode: {converter}, threads: {max_workers})")

    poppler_like_msgs = []
    failures = 0
    completed = 0
    progress_line_active = [False]

    def worker(png_path: Path):
        webp_path = png_path.with_suffix('.webp')
        if converter == 'cwebp':
            stderr = _png_to_webp_cwebp(png_path, webp_path, quality, lossless)
        else:
            stderr = _png_to_webp_pillow(png_path, webp_path, quality, lossless)
        # 変換成功時のみPNG削除
        try:
            png_path.unlink(missing_ok=False)
        except Exception as e:
            return False, f"Could not delete PNG after convert: {png_path.name} ({e})"
        return True, stderr

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(worker, p): p for p in png_files}
        _show_progress(completed, len(png_files), failures, prefix="WEBP")
        progress_line_active[0] = True

        for fut in as_completed(futures):
            png_path = futures[fut]
            try:
                ok, stderr = fut.result()
                if not ok:
                    failures += 1
                if stderr:
                    poppler_like_msgs.append(f"[{png_path.name}] {stderr.strip()}")
            except FileNotFoundError:
                failures += 1
                _end_progress_line(progress_line_active)
                if converter == 'cwebp':
                    safe_print("Error: 'cwebp' command not found.")
                    safe_print("Please install 'webp' package (cwebp).")
                else:
                    safe_print("Error: Pillow could not process file:", png_path.name)
            except subprocess.CalledProcessError as e:
                failures += 1
                _end_progress_line(progress_line_active)
                safe_print(f"Error: WebP convert failed: {png_path.name}. rc={e.returncode}")
                if e.stderr:
                    poppler_like_msgs.append(f"[{png_path.name}] {e.stderr.strip()}")
            except Exception as e:
                failures += 1
                _end_progress_line(progress_line_active)
                safe_print(f"Unexpected error in WebP conversion for {png_path.name}: {e}")
            finally:
                completed += 1
                _show_progress(completed, len(png_files), failures, prefix="WEBP")
                progress_line_active[0] = True

    _end_progress_line(progress_line_active)
    safe_print("WebP conversion finished.")
    # if poppler_like_msgs:
    #     # safe_print("WebP converter messages:")
    #     # for m in poppler_like_msgs:
    #     #     safe_print(" ", m)

    if failures:
        safe_print(f"Completed with {failures} failed WebP files.")

    # safe_print("Generated WebP files:")
    # for f in sorted(output_dir.glob(f'{stem}-*.webp')):
    #     safe_print(f"  -> {f.name}")

def convert_pdf_to_png(pdf_path_str: str):
    """
    Convert each page of the specified PDF to PNG images using parallel processing.
    Then convert PNGs to WebP in parallel and delete PNGs after successful conversion.

    Args:
        pdf_path_str (str): Absolute path to the target PDF file.
    """
    pdf_path = Path(pdf_path_str)

    # Validate file existence and .pdf extension
    if not pdf_path.is_file() or pdf_path.suffix.lower() != '.pdf':
        safe_print(f"Error: Not a PDF file: {pdf_path_str}")
        return

    # Create output directory (PDF name without extension)
    output_dir = pdf_path.parent / pdf_path.stem
    output_dir.mkdir(exist_ok=True)
    safe_print(f"Output dir: {output_dir}")

    # Remove existing PNG files in output directory
    safe_print("Removing existing PNG files...")
    deleted_count = 0
    for file_in_dir in output_dir.iterdir():
        if file_in_dir.is_file() and file_in_dir.suffix.lower() == '.png':
            try:
                file_in_dir.unlink()
                deleted_count += 1
                safe_print(f"  - Deleted: {file_in_dir.name}")
            except OSError as e:
                safe_print(f"Error: Cannot delete file {file_in_dir}: {e}")

    if deleted_count > 0:
        safe_print(f"Deleted {deleted_count} existing PNG files.")
    else:
        safe_print("No existing PNG files to delete.")

    # Determine page count
    pages = get_pdf_page_count(pdf_path)
    conversion_attempted = False

    if not pages:
        safe_print("Falling back to single-process conversion (no page count).")
        try:
            output_prefix = output_dir / pdf_path.stem
            command = ['pdftoppm', '-png', '-r', '600', str(pdf_path), str(output_prefix)]
            result = subprocess.run(command, capture_output=True, text=True, errors='replace', check=True)
            safe_print("Conversion finished.")
            if result.stderr:
                safe_print("Poppler messages:\n", result.stderr)
            conversion_attempted = True
        except FileNotFoundError:
            safe_print("Error: 'pdftoppm' command not found.")
            safe_print("Please ensure Poppler is installed and in PATH.")
            return
        except subprocess.CalledProcessError as e:
            safe_print("Error during conversion.")
            safe_print(f"Command: {' '.join(e.cmd)}")
            safe_print(f"Return code: {e.returncode}")
            safe_print(f"Stdout:\n{e.stdout}")
            safe_print(f"Stderr:\n{e.stderr}")
            return
        except Exception as e:
            safe_print(f"Unexpected error: {e}")
            return
    else:
        try:
            dpi = int(os.environ.get('PDF2PNG_DPI', '600'))
            max_workers = os.cpu_count() or 1
            safe_print(f"Starting PDF to PNG conversion in parallel... (pages: {pages}, threads: {max_workers})")

            output_prefix = output_dir / pdf_path.stem

            poppler_msgs = []
            failures = 0
            completed = 0

            progress_line_active = [False]

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(_convert_single_page, pdf_path, output_prefix, dpi, page): page
                    for page in range(1, pages + 1)
                }

                _show_progress(completed, pages, failures)
                progress_line_active[0] = True

                for fut in as_completed(futures):
                    page_no = futures[fut]
                    try:
                        stderr = fut.result()
                        if stderr:
                            poppler_msgs.append(f"[page {page_no}] {stderr.strip()}")
                    except FileNotFoundError:
                        failures += 1
                        _end_progress_line(progress_line_active)
                        safe_print(f"Error: 'pdftoppm' not found for page {page_no}.")
                    except subprocess.CalledProcessError as e:
                        failures += 1
                        _end_progress_line(progress_line_active)
                        safe_print(f"Error: Conversion failed on page {page_no}. rc={e.returncode}")
                        if e.stderr:
                            poppler_msgs.append(f"[page {page_no}] {e.stderr.strip()}")
                    except Exception as e:
                        failures += 1
                        _end_progress_line(progress_line_active)
                        safe_print(f"Unexpected error on page {page_no}: {e}")
                    finally:
                        completed += 1
                        _show_progress(completed, pages, failures)
                        progress_line_active[0] = True

            _end_progress_line(progress_line_active)
            safe_print("Conversion finished.")
            if poppler_msgs:
                safe_print("Poppler messages:")
                for m in poppler_msgs:
                    safe_print(" ", m)
            if failures:
                safe_print(f"Completed with {failures} failed pages.")
            conversion_attempted = True

        except Exception as e:
            safe_print(f"Unexpected error: {e}")
            return

    # PNG -> WebP 並列変換 (成功したPNGのみ削除)
    if conversion_attempted:
        _convert_pngs_to_webp_parallel(output_dir, pdf_path.stem)

if __name__ == "__main__":
    # Check command line args
    if len(sys.argv) != 2:
        safe_print("Usage: python pdf2png_convert.py <absolute path to PDF>")
        sys.exit(1)

    pdf_file_path = sys.argv[1]
    convert_pdf_to_png(pdf_file_path)
