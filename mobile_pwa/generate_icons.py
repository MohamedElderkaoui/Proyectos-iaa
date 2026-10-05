"""Generate the two PNG sizes required by common PWA installers."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path


OUTPUT_DIR = Path(__file__).resolve().parent / "icons"
CANVAS_SIZE = 512
BACKGROUND = (16, 42, 67, 255)
FOREGROUND = (255, 255, 255, 255)
ACCENT = (57, 182, 196, 255)


def _distance_to_segment(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
    dx, dy = x2 - x1, y2 - y1
    length_squared = dx * dx + dy * dy
    projection = 0 if length_squared == 0 else ((px - x1) * dx + (py - y1) * dy) / length_squared
    projection = min(1, max(0, projection))
    nearest_x, nearest_y = x1 + projection * dx, y1 + projection * dy
    return ((px - nearest_x) ** 2 + (py - nearest_y) ** 2) ** 0.5


def _pixel(x: float, y: float) -> tuple[int, int, int, int]:
    # Keep the symbol inside a generous maskable-icon safe area.
    if (x - 235) ** 2 + (y - 326) ** 2 < 115**2 and (x - 235) ** 2 + (y - 326) ** 2 > 99**2:
        return ACCENT
    if (x - 304) ** 2 + (y - 127) ** 2 <= 27**2:
        return FOREGROUND

    lines = [
        (300, 164, 280, 245, 14, FOREGROUND),
        (294, 178, 353, 220, 12, FOREGROUND),
        (282, 245, 336, 245, 15, FOREGROUND),
        (281, 240, 245, 318, 14, FOREGROUND),
        (336, 245, 372, 322, 14, FOREGROUND),
        (245, 318, 338, 318, 16, FOREGROUND),
        (338, 318, 372, 322, 12, FOREGROUND),
        (245, 318, 214, 398, 13, FOREGROUND),
        (214, 398, 319, 398, 13, FOREGROUND),
        (319, 398, 372, 322, 13, FOREGROUND),
    ]
    for x1, y1, x2, y2, width, color in lines:
        if _distance_to_segment(x, y, x1, y1, x2, y2) <= width / 2:
            return color
    return BACKGROUND


def _chunk(kind: bytes, data: bytes) -> bytes:
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def write_png(size: int) -> None:
    rows = bytearray()
    scale = CANVAS_SIZE / size
    for y in range(size):
        rows.append(0)
        for x in range(size):
            rows.extend(_pixel((x + 0.5) * scale, (y + 0.5) * scale))
    header = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", header)
    png += _chunk(b"IDAT", zlib.compress(bytes(rows), level=9)) + _chunk(b"IEND", b"")
    (OUTPUT_DIR / f"icon-{size}.png").write_bytes(png)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for size in (192, 512):
        write_png(size)


if __name__ == "__main__":
    main()
