import csv
import json
from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from backend.utils.text_cleaner import normalize_text


def parse_document(path):
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        text = " ".join(page.extract_text() or "" for page in reader.pages)
        return normalize_text(text)
    if suffix == ".docx":
        doc = DocxDocument(str(path))
        return normalize_text(" ".join(paragraph.text for paragraph in doc.paragraphs))
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8-sig", errors="ignore") as fh:
            rows = list(csv.DictReader(fh))
        # Normalize keys by removing any remaining BOM characters
        if rows:
            first_row = rows[0]
            normalized_keys = {k.replace('\ufeff', '').strip(): v for k, v in first_row.items()}
            rows_normalized = [normalized_keys] + [{k.replace('\ufeff', '').strip(): v for k, v in row.items()} for row in rows[1:]]
            return normalize_text(json.dumps(rows_normalized[:100], ensure_ascii=True))
        return normalize_text(json.dumps(rows[:100], ensure_ascii=True))
    return normalize_text(path.read_text(encoding="utf-8", errors="ignore"))
