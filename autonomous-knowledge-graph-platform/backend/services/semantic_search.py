import re

from sqlalchemy import or_

from backend.models.document_model import Document
from backend.models.entity_model import Entity


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has",
    "have", "how", "in", "is", "it", "of", "on", "or", "show", "that", "the",
    "their", "to", "what", "which", "with",
}


def _tokens(query):
    words = re.findall(r"[a-z0-9]+", (query or "").lower())
    tokens = []
    for word in words:
        if len(word) < 3 or word in STOP_WORDS:
            continue
        tokens.append(word)
        if word.endswith("ies") and len(word) > 4:
            tokens.append(f"{word[:-3]}y")
        elif word.endswith("s") and len(word) > 3:
            tokens.append(word[:-1])
    return list(dict.fromkeys(tokens))


def _document_text(document):
    keywords = " ".join(document.keywords_json or [])
    return " ".join([
        document.filename or "",
        document.classification or "",
        document.summary or "",
        document.content or "",
        keywords,
    ]).lower()


def _entity_text(entity):
    attributes = " ".join(str(value) for value in (entity.attributes_json or {}).values())
    return " ".join([
        entity.name or "",
        entity.label or "",
        entity.canonical_id or "",
        attributes,
    ]).lower()


def _score(text, query, tokens):
    if not text:
        return 0
    score = 0
    if query and query.lower() in text:
        score += 8
    for token in tokens:
        if token in text:
            score += 2
        score += len(re.findall(rf"\b{re.escape(token)}\b", text))
    return score


def _rank(items, text_builder, query, tokens, limit):
    scored = [
        (score, item)
        for item in items
        if (score := _score(text_builder(item), query, tokens)) > 0
    ]
    scored.sort(key=lambda pair: (-pair[0], getattr(pair[1], "created_at", None) or getattr(pair[1], "id", 0)))
    return [item for _, item in scored[:limit]]


def _entity_linked_documents(entities, existing_doc_ids, limit):
    document_ids = []
    for entity in entities:
        if entity.document_id and entity.document_id not in existing_doc_ids:
            document_ids.append(entity.document_id)
    document_ids = list(dict.fromkeys(document_ids))
    if not document_ids:
        return []

    documents = Document.query.filter(Document.id.in_(document_ids)).all()
    by_id = {document.id: document for document in documents}
    return [by_id[document_id] for document_id in document_ids if document_id in by_id][:limit]


def search(query, limit=10):
    query = (query or "").strip()
    if not query:
        return {"documents": [], "entities": []}

    tokens = _tokens(query)
    if not tokens:
        return {"documents": [], "entities": []}

    doc_filters = []
    entity_filters = []
    for token in tokens:
        like = f"%{token}%"
        doc_filters.extend([
            Document.filename.ilike(like),
            Document.classification.ilike(like),
            Document.summary.ilike(like),
            Document.content.ilike(like),
        ])
        entity_filters.extend([
            Entity.name.ilike(like),
            Entity.label.ilike(like),
            Entity.canonical_id.ilike(like),
        ])

    docs = Document.query.filter(or_(*doc_filters)).limit(max(limit * 5, limit)).all()
    entities = Entity.query.filter(or_(*entity_filters)).limit(max(limit * 5, limit)).all()
    ranked_docs = _rank(docs, _document_text, query, tokens, limit)
    ranked_entities = _rank(entities, _entity_text, query, tokens, limit)
    if not ranked_docs:
        ranked_docs.extend(_entity_linked_documents(ranked_entities, set(), limit))

    return {
        "documents": [doc.to_dict() for doc in ranked_docs],
        "entities": [entity.to_dict() for entity in ranked_entities],
    }
