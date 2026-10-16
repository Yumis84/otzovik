#!/usr/bin/env python3
"""Build the exact public-only site tree for CI and deployment."""
from pathlib import Path
import shutil
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "_site"
FILES = [
    "index.html", "404.html", "favicon.svg", "robots.txt",
    "sitemap.xml", "llms.txt", "CNAME",
    "reviews/moderation.html", "reviews/moderation.css",
]
DIRS = [
    "about", "add", "ai", "business", "contacts",
    "methodology", "privacy", "reviews", "terms",
]
FILES += [f"{name}/index.html" for name in DIRS]


def build():
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir()
    for name in FILES:
        src = ROOT / name
        if not src.is_file() or src.is_symlink() or src.stat().st_size == 0:
            raise RuntimeError(f"Missing, empty or symlinked public file: {name}")
        target = DEST / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
    actual = {p.relative_to(DEST).as_posix() for p in DEST.rglob("*") if p.is_file()}
    if actual != set(FILES):
        raise RuntimeError(f"Artifact mismatch: {actual ^ set(FILES)}")
    ET.parse(DEST / "sitemap.xml")
    if "Sitemap:" not in (DEST / "robots.txt").read_text(encoding="utf-8"):
        raise RuntimeError("robots.txt has no sitemap")
    if any(p.name.startswith(".") or p.is_symlink() for p in DEST.rglob("*")):
        raise RuntimeError("Hidden file or symlink in public artifact")
    print(f"PASS: public artifact contains exactly {len(actual)} allowed files")


if __name__ == "__main__":
    try:
        build()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
