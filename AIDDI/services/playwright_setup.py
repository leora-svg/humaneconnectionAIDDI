import subprocess
import sys
from pathlib import Path

def ensure_playwright_browser():
  marker = Path("/tmp/playwright-installed")

if marker.exists():
  return

subprocess.run(
  [
    sys.executable,
    "-m",
    "playwright",
    "install",
    "chromium",
  ],
  check=True,
)

marker.touch()
