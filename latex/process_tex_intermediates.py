import shutil
from pathlib import Path
import sys

# ===== Settings =====
target_dir = Path(".tex_intermediates")  # source folder
ext = ".log"                              # target extension (e.g. .txt)

# ===== Run =====
parent_dir = target_dir.parent

# Check existence
if not target_dir.exists():
	print(f"Specified folder {target_dir} does not exist.")
	sys.exit(1)

# Find files & copy
for file_path in target_dir.glob(f"*{ext}"):
	dest = parent_dir / file_path.name
	print(f"Copy: {file_path} -> {dest}")
	shutil.copy2(file_path, dest)

# Remove folder
print(f"Removing folder: {target_dir}")
print("")
shutil.rmtree(target_dir)