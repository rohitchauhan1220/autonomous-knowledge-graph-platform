from email import policy
from email.parser import BytesParser
from pathlib import Path
from backend.utils.text_cleaner import normalize_text


def parse_email(path):
    msg = BytesParser(policy=policy.default).parsebytes(Path(path).read_bytes())
    body = msg.get_body(preferencelist=("plain", "html"))
    return normalize_text(f"Subject: {msg.get('subject', '')}. From: {msg.get('from', '')}. {body.get_content() if body else ''}")
