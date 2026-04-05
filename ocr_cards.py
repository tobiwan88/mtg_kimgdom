#!/usr/bin/env python3
"""Extract text from card images using Tesseract OCR.

Upscales each image 3× before OCR for better accuracy on small card text.
Output: one .txt file per card in cards/ alongside the image.

Usage:
    uv run python ocr_cards.py [cards_dir]   # default: cards/
"""

import argparse
import sys
from pathlib import Path

import pytesseract
from PIL import Image


def ocr_card(image_path: Path) -> str:
    img = Image.open(image_path)
    # Upscale 3× — significantly improves tesseract accuracy on small text
    w, h = img.size
    img = img.resize((w * 3, h * 3), Image.Resampling.LANCZOS)
    # Tesseract config: treat as a single block of text, English
    text = pytesseract.image_to_string(img, lang="eng", config="--psm 6")
    return text.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="OCR all card images in a directory")
    parser.add_argument("cards_dir", nargs="?", default="cards", help="Directory with card images")
    args = parser.parse_args()

    cards_dir = Path(args.cards_dir)
    if not cards_dir.is_dir():
        print(f"ERROR: '{cards_dir}' is not a directory", file=sys.stderr)
        sys.exit(1)

    images = sorted(p for p in cards_dir.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"})

    if not images:
        print("No images found.", file=sys.stderr)
        sys.exit(1)

    for img_path in images:
        out_path = img_path.with_suffix(".txt")
        text = ocr_card(img_path)
        out_path.write_text(text + "\n", encoding="utf-8")
        preview = text.replace("\n", " ")[:80]
        print(f"{img_path.name} → {out_path.name}  |  {preview}")

    print(f"\nDone — {len(images)} cards processed.")


if __name__ == "__main__":
    main()
