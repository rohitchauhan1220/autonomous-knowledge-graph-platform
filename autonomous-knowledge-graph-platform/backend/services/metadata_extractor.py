from datetime import datetime
from pathlib import Path


def extract_metadata(path, source_type):
    file_path = Path(path)
    return {
        "source_type": source_type,
        "filename": file_path.name,
        "size_bytes": file_path.stat().st_size if file_path.exists() else 0,
        "ingested_at": datetime.utcnow().isoformat(),
    }
