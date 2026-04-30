import re
from collections import Counter


ENTITY_PATTERNS = {
    "Risk": r"\b(delay|risk|outage|breach|incident|escalation)\b",
    "Metric": r"\b\d+(?:\.\d+)?\s?(?:%|days|hours|usd|inr|units)(?=\W|$)",
    "Organization": r"\b[A-Z][A-Za-z0-9& ]{2,}\s(?:Inc|Ltd|LLC|Corp|Logistics|Systems|Cloud)\b",
}


def extract_entities(text):
    found = []
    for label, pattern in ENTITY_PATTERNS.items():
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            found.append({"name": match.group(0).strip(), "label": label, "attributes": {"method": "rule"}})
    capitalized = re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+){0,2}\b", text)
    for name, _ in Counter(capitalized).most_common(10):
        if len(name) > 3:
            found.append({"name": name, "label": "Concept", "attributes": {"method": "heuristic"}})
    dedup = {}
    for entity in found:
        dedup[(entity["name"].lower(), entity["label"])] = entity
    return list(dedup.values())[:40]


def extract_relations(entities):
    relations = []
    for idx in range(len(entities) - 1):
        relations.append({
            "source": entities[idx]["name"],
            "target": entities[idx + 1]["name"],
            "type": "CO_OCCURS_WITH",
            "confidence": 0.68,
        })
    return relations


def extract_keywords(text, limit=12):
    """Simple transparent keyword extractor for demos when no AI key is present."""
    stopwords = {"the", "and", "for", "with", "that", "this", "from", "into", "reported", "enterprise"}
    words = re.findall(r"\b[a-zA-Z][a-zA-Z]{3,}\b", text.lower())
    ranked = Counter(word for word in words if word not in stopwords)
    return [word for word, _ in ranked.most_common(limit)]


def classify_document(text):
    lowered = text.lower()
    if any(word in lowered for word in ["supplier", "shipment", "delivery", "procurement"]):
        return "Supply Chain Intelligence"
    if any(word in lowered for word in ["incident", "ticket", "outage", "sla"]):
        return "IT Incident Intelligence"
    if any(word in lowered for word in ["fraud", "compliance", "audit", "breach"]):
        return "Risk & Compliance"
    return "General Intelligence"


def cluster_entities(entities):
    clusters = {}
    for entity in entities:
        clusters.setdefault(entity.get("label", "Concept"), []).append(entity.get("name"))
    return clusters
