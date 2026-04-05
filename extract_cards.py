#!/usr/bin/env python3
"""Extract MTG role cards from the Advanced Kingdoms PDF as standalone images."""

import argparse
from pathlib import Path

import pymupdf


def extract_cards(pdf_path: str, output_dir: str = "cards") -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(pdf_path)
    card_num = 1

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        # get_image_info returns images sorted by appearance; we sort by position (row then col)
        images = sorted(
            page.get_image_info(xrefs=True),
            key=lambda i: (round(i["bbox"][1]), round(i["bbox"][0])),
        )

        for img_info in images:
            xref = img_info["xref"]
            img_data = doc.extract_image(xref)
            ext = img_data["ext"]  # usually "png" or "jpeg"
            img_bytes = img_data["image"]

            filename = out / f"card_{card_num:03d}.{ext}"
            filename.write_bytes(img_bytes)
            print(f"  Saved {filename}  ({img_data['width']}x{img_data['height']})")
            card_num += 1

    doc.close()
    print(f"\nExtracted {card_num - 1} cards to '{out}/'")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract cards from Advanced Kingdoms PDF")
    parser.add_argument(
        "pdf",
        nargs="?",
        default="Advanced Kingdoms v1.56 A4 (Full).pdf",
        help="Path to the PDF file",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="cards",
        help="Output directory (default: cards/)",
    )
    args = parser.parse_args()
    extract_cards(args.pdf, args.output)


if __name__ == "__main__":
    main()
