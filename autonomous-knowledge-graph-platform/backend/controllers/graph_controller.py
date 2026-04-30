from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from backend.models.entity_model import Entity
from backend.models.relation_model import Relation
from backend.models.enterprise_model import Annotation, GraphVersion
from config.database import db


def graph_snapshot():
    entities = Entity.query.limit(300).all()
    relations = Relation.query.limit(600).all()
    nodes = [{"data": {"id": str(e.id), "label": e.name, "type": e.label}} for e in entities]
    edges = [{
        "data": {
            "id": f"e{r.id}",
            "source": str(r.source_entity_id),
            "target": str(r.target_entity_id),
            "label": r.relation_type,
            "confidence": r.confidence,
        }
    } for r in relations]
    return jsonify({"nodes": nodes, "edges": edges, "version": 1})


def traverse(entity_id):
    relations = Relation.query.filter(
        (Relation.source_entity_id == entity_id) | (Relation.target_entity_id == entity_id)
    ).limit(50).all()
    return jsonify({"relations": [relation.to_dict() for relation in relations]})


def versions():
    items = GraphVersion.query.order_by(GraphVersion.version.desc()).limit(50).all()
    return jsonify({"versions": [item.to_dict() for item in items]})


def add_annotation(entity_id):
    payload = request.get_json() or {}
    note = (payload.get("note") or "").strip()
    if not note:
        return jsonify({"error": "Annotation note is required"}), 400
    annotation = Annotation(entity_id=entity_id, user_id=int(get_jwt_identity()), note=note)
    db.session.add(annotation)
    db.session.commit()
    return jsonify({"annotation": annotation.to_dict()}), 201


def list_annotations(entity_id):
    notes = Annotation.query.filter_by(entity_id=entity_id).order_by(Annotation.created_at.desc()).all()
    return jsonify({"annotations": [note.to_dict() for note in notes]})
