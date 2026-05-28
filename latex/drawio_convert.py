#!/usr/bin/env python3
from __future__ import annotations

import argparse
import enum
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

print("---Draw.io PNG Converter---")

DRAWIO_CANDIDATES = ("drawio", "drawio-desktop", "draw.io")

def find_drawio_command() -> str:
    for cmd in DRAWIO_CANDIDATES:
        if shutil.which(cmd):
            return cmd
    print("ERROR: drawio command not found. Please install Draw.io Desktop / CLI.", file=sys.stderr)
    sys.exit(1)


def newer(src: Path, dst: Path) -> bool:
    return not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime


class Result(enum.Enum):
    CREATED = "created"
    UPDATED = "updated"
    SKIPPED = "skipped"
    FAILED = "failed"


def export_drawio(drawio_cmd: str, src: Path, scale: float, force: bool) -> Result:
    png = src.with_suffix(".png")

    if not force and png.exists() and not newer(src, png):
        print(f"Skip (up-to-date): {png}")
        return Result.SKIPPED

    status = Result.CREATED if not png.exists() else Result.UPDATED
    msg = "Create" if status is Result.CREATED else "Update"
    print(f"{msg}: {png} (from {src})")

    try:
        proc = subprocess.run(
            [
                drawio_cmd,
                "--export",
                "--format", "png",
                "--output", str(png),
                "--scale", str(scale),
                str(src),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        print("ERROR: Cannot execute drawio command. Check PATH.", file=sys.stderr)
        return Result.FAILED

    if proc.returncode != 0:
        print(f"ERROR: Conversion failed {src} (exit={proc.returncode})", file=sys.stderr)
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
        return Result.FAILED

    # 不要なmacOS Electronノイズをフィルタ
    if proc.stderr:
        filtered_lines = [
            line for line in proc.stderr.splitlines()
            if "task_policy_set" not in line
        ]
        if filtered_lines:
            print("\n".join(filtered_lines), file=sys.stderr)

    return status


def delete_legacy(root: Path) -> int:
    cnt = 0
    for f in root.rglob("*.drawio.png"):
        try:
            f.unlink()
            print(f"Delete (legacy): {f}")
            cnt += 1
        except OSError as e:
            print(f"Failed to delete: {f}: {e}", file=sys.stderr)
    return cnt


@dataclass
class Stats:
    created: int = 0
    updated: int = 0
    skipped: int = 0
    failed: int = 0
    deleted_legacy: int = 0

    def summarize(self) -> str:
        return (
            f"Summary: created={self.created}, updated={self.updated}, "
            f"skipped={self.skipped}, failed={self.failed}, deleted_legacy={self.deleted_legacy}"
        )


def gather_targets(root: Path) -> List[Path]:
    return sorted(root.rglob("*.drawio"))


def process(drawio_cmd: str, targets: Iterable[Path], scale: float, jobs: int, force: bool) -> Stats:
    stats = Stats()
    targets_list = list(targets)
    if not targets_list:
        return stats

    workers = max(1, min(jobs, len(targets_list)))

    def worker(src: Path) -> Result:
        return export_drawio(drawio_cmd, src, scale, force)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        future_map = {ex.submit(worker, src): src for src in targets_list}
        for fut in as_completed(future_map):
            src = future_map[fut]
            try:
                res = fut.result()
            except Exception as e:
                print(f"ERROR: Unexpected exception during conversion {src}: {e}", file=sys.stderr)
                res = Result.FAILED

            if res is Result.CREATED:
                stats.created += 1
            elif res is Result.UPDATED:
                stats.updated += 1
            elif res is Result.SKIPPED:
                stats.skipped += 1
            elif res is Result.FAILED:
                stats.failed += 1

    return stats


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="*.drawio -> *.png converter")
    p.add_argument("-r", "--root", type=Path, default=Path("."), help="Root directory (default: .)")
    p.add_argument("--scale", type=float, default=6.25, help="Scale (drawio --scale) default: 6.25")
    p.add_argument("--no-legacy-clean", action="store_true", help="Do not delete *.drawio.png")
    p.add_argument("-j", "--jobs", type=int, default=(os.cpu_count() or 4), help="Number of parallel jobs (default: CPU cores)")
    p.add_argument("-f", "--force", action="store_true", help="全ファイルを強制再生成（更新日時を無視）")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if not args.root.exists():
        print(f"ERROR: Root does not exist: {args.root}", file=sys.stderr)
        return 2

    stats = Stats()

    if not args.no_legacy_clean:
        stats.deleted_legacy = delete_legacy(args.root)

    drawio_cmd = find_drawio_command()

    targets = gather_targets(args.root)
    if not targets:
        print("No .drawio files found.")
        print()
        print(stats.summarize())
        return 0

    run_stats = process(drawio_cmd, targets, args.scale, args.jobs, args.force)
    stats.created = run_stats.created
    stats.updated = run_stats.updated
    stats.skipped = run_stats.skipped
    stats.failed = run_stats.failed

    print()
    print(stats.summarize())
    return 1 if stats.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
