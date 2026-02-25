# Bangla PDF OCR Setup

This project extracts Bangla text from PDFs.
It supports:
- normal text PDFs (direct extraction)
- scanned/image PDFs (OCR fallback)

## 1) Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 2) Run OCR

```bash
python ocr_bangla_pdf.py books/Class_1_bangla_1.pdf output.txt
```

If `output.txt` is omitted, default output is `output.txt`.

Process only a specific page range:

```bash
python ocr_bangla_pdf.py books/Class_1_bangla_1.pdf output.txt --start-page 1 --end-page 20
```

Notes:
- No `poppler` or `tesseract` install is required.
- First run may take longer because EasyOCR downloads model files.
