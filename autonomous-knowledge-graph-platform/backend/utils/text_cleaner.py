import re


def normalize_text(text):
    text = re.sub(r"\s+", " ", text or "").strip()
    return text.replace("\x00", "")
