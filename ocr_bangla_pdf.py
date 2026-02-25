import argparse
from pathlib import Path

import easyocr
import fitz
import numpy as np


def page_to_array(page: fitz.Page, zoom: float = 2.0) -> np.ndarray:
    matrix = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)


def extract_text_basic(
    pdf_path: Path,
    output_path: Path,
    start_page: int | None = None,
    end_page: int | None = None,
) -> None:
    pages: list[str] = []
    reader = easyocr.Reader(["bn", "en"], gpu=False)

    with fitz.open(pdf_path) as doc:
        total_pages = len(doc)
        start = start_page if start_page is not None else 1
        end = end_page if end_page is not None else total_pages

        if start < 1 or end < 1 or start > total_pages or end > total_pages or start > end:
            raise ValueError(
                f"Invalid page range: start={start}, end={end}, total_pages={total_pages}"
            )

        for index in range(start - 1, end):
            page = doc[index]
            text = page.get_text("text").strip()

            if not text:
                image_array = page_to_array(page)
                text = "\n".join(reader.readtext(image_array, detail=0, paragraph=True)).strip()

            pages.append(f"===== Page {index + 1} =====\n{text}")

    output_path.write_text("\n\n".join(pages), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_txt", nargs="?", default="output.txt")
    parser.add_argument("--start-page", type=int, default=None, help="1-based start page")
    parser.add_argument("--end-page", type=int, default=None, help="1-based end page")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf_path = args.input_pdf
    output_path = Path(args.output_txt)

    if not pdf_path.exists():
        print(f"Error: file not found - {pdf_path}")
        return 1

    try:
        extract_text_basic(
            pdf_path,
            output_path,
            start_page=args.start_page,
            end_page=args.end_page,
        )
    except ValueError as exc:
        print(f"Error: {exc}")
        return 1

    print(f"Done. Saved text to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
