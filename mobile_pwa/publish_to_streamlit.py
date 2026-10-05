"""Copy the PWA shell to Streamlit's same-origin static directory."""

from __future__ import annotations

import shutil
from pathlib import Path


PWA_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PWA_ROOT.parent
STATIC_TARGET = PROJECT_ROOT / "app" / "static" / "mobile_pwa"
PUBLISHED_FILES = (
    "index.html",
    "app.js",
    "styles.css",
    "manifest.webmanifest",
    "sw.js",
)


def publish() -> Path:
    STATIC_TARGET.mkdir(parents=True, exist_ok=True)
    for filename in PUBLISHED_FILES:
        shutil.copy2(PWA_ROOT / filename, STATIC_TARGET / filename)
    source_icons = PWA_ROOT / "icons"
    target_icons = STATIC_TARGET / "icons"
    target_icons.mkdir(exist_ok=True)
    for icon in source_icons.glob("*.png"):
        shutil.copy2(icon, target_icons / icon.name)
    return STATIC_TARGET


if __name__ == "__main__":
    print(publish())
