from backend.utils.helpers import truncate


def summarize(text):
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if len(s.strip()) > 20]
    return truncate(". ".join(sentences[:3]) + ("." if sentences else ""), 600)
