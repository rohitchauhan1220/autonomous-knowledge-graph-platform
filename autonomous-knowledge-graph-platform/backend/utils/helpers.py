def truncate(text, limit=320):
    return text if len(text or "") <= limit else text[: limit - 3] + "..."
