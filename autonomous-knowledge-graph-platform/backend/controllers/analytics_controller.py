from flask import jsonify, request
from backend.models.document_model import Document
from backend.models.entity_model import Entity
from backend.models.relation_model import Relation
from backend.models.query_model import QueryLog
from backend.services.analytics_service import executive_insights, risk_heatmap, system_health
from backend.services.report_service import build_executive_report
from config.database import db


def dashboard_metrics():
    return jsonify({
        "documents": Document.query.count(),
        "entities": Entity.query.count(),
        "relations": Relation.query.count(),
        "queries": QueryLog.query.count(),
        "risk_score": 72,
        "automation_rate": 84,
    })


def recent_activity():
    docs = Document.query.order_by(Document.created_at.desc()).limit(6).all()
    queries = QueryLog.query.order_by(QueryLog.created_at.desc()).limit(6).all()
    return jsonify({"documents": [d.to_dict() for d in docs], "queries": [q.to_dict() for q in queries]})


def document_detail(document_id):
    document = Document.query.get_or_404(document_id)
    return jsonify({"document": document.to_dict()})


def update_document(document_id):
    document = Document.query.get_or_404(document_id)
    payload = request.get_json() or {}
    if "filename" in payload:
        document.filename = (payload.get("filename") or document.filename).strip() or document.filename
    if "summary" in payload:
        document.summary = (payload.get("summary") or document.summary).strip()
    if "classification" in payload:
        document.classification = (payload.get("classification") or document.classification).strip() or document.classification
    if "keywords" in payload:
        document.keywords_json = payload.get("keywords") if isinstance(payload.get("keywords"), list) else document.keywords_json
    if "metadata" in payload:
        document.metadata_json = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else document.metadata_json
    db.session.commit()
    return jsonify({"document": document.to_dict()})


def delete_document(document_id):
    document = Document.query.get_or_404(document_id)
    db.session.delete(document)
    db.session.commit()
    return jsonify({"message": "Document deleted"})


def query_detail(query_id):
    query = QueryLog.query.get_or_404(query_id)
    return jsonify({"query": query.to_dict()})


def update_query(query_id):
    query = QueryLog.query.get_or_404(query_id)
    payload = request.get_json() or {}
    if "question" in payload:
        query.question = (payload.get("question") or query.question).strip() or query.question
    if "answer" in payload:
        query.answer = (payload.get("answer") or query.answer).strip() or query.answer
    if "sources" in payload:
        query.sources_json = payload.get("sources") if isinstance(payload.get("sources"), list) else query.sources_json
    db.session.commit()
    return jsonify({"query": query.to_dict()})


def delete_query(query_id):
    query = QueryLog.query.get_or_404(query_id)
    db.session.delete(query)
    db.session.commit()
    return jsonify({"message": "Query deleted"})


def executive_summary():
    return jsonify(executive_insights())


def health():
    return jsonify(system_health())


def heatmap():
    return jsonify({"heatmap": risk_heatmap()})


def report():
    return jsonify({"report": build_executive_report()})
