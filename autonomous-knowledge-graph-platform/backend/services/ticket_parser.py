import json
from pathlib import Path
from backend.utils.text_cleaner import normalize_text


def parse_ticket(path):
    data = json.loads(Path(path).read_text(encoding="utf-8", errors="ignore"))
    return normalize_text(f"{data.get('title', '')} {data.get('priority', '')} {data.get('description', '')} {data.get('status', '')}")
