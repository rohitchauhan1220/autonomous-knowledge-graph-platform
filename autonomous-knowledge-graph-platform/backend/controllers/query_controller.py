from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from backend.services.semantic_search import search
from backend.services.reasoning_engine import ReasoningEngine
from backend.models.query_model import QueryLog


def semantic_search():
    query = request.args.get("q", "")
    return jsonify(search(query))


def ask():
    payload = request.get_json() or {}
    question = payload.get("question", "")
    if not question:
        return jsonify({"error": "Question is required"}), 400
    result = ReasoningEngine().answer(question, user_id=int(get_jwt_identity()) if get_jwt_identity() else None)
    return jsonify(result)


def suggestions():
    return jsonify({"suggestions": [
        "Which suppliers have delivery risk?",
        "Show dependencies connected to Orion Cloud.",
        "What incidents affect customer renewals?",
        "Generate executive recommendations from current graph.",
        "Which documents contain compliance or fraud risk?",
    ]})


def history():
    items = QueryLog.query.order_by(QueryLog.created_at.desc()).limit(30).all()
    return jsonify({"history": [item.to_dict() for item in items]})
