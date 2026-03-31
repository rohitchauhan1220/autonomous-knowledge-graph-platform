def extract_relation(text):
    if "founded" in text:
        return "FOUNDED"
    elif "CEO" in text:
        return "CEO_OF"
    else:
        return "RELATED_TO"