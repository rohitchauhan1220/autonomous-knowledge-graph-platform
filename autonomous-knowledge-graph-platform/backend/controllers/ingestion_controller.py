import hashlib
from flask import current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity
from config.database import db
from backend.models.document_model import Document
from backend.services.document_parser import parse_document
from backend.services.email_parser import parse_email
from backend.services.ticket_parser import parse_ticket
from backend.services.metadata_extractor import extract_metadata
from backend.services.summarization_service import summarize
from backend.services.graph_builder import build_graph_for_document
from backend.services.audit_logger import audit
from backend.services.nlp_service import classify_document, extract_keywords
from backend.utils.file_utils import save_upload
from backend.utils.validators import allowed_file


def upload_document():
    file = request.files.get("file")
    source_type = request.form.get("source_type", "text")
    return _process_uploaded_file(file, source_type)


def _process_uploaded_file(file, source_type):
    """Shared ingestion workflow used by single and bulk uploads."""
    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Unsupported or missing file"}), 400
    filename, path = save_upload(file, current_app.config["UPLOAD_FOLDER"])
    try:
        source_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception as e:
        return jsonify({"error": f"Failed to read file: {str(e)}"}), 400
    
    duplicate = Document.query.filter_by(source_hash=source_hash).first()
    if duplicate:
        return jsonify({"error": "Duplicate document detected", "document": duplicate.to_dict()}), 409
    
    try:
        if source_type == "email" or filename.endswith(".eml"):
            content = parse_email(path)
        elif source_type == "ticket" or filename.endswith(".json"):
            content = parse_ticket(path)
        else:
            content = parse_document(path)
    except Exception as e:
        return jsonify({"error": f"Failed to parse document: {str(e)}"}), 400
    
    try:
        document = Document(
            filename=filename,
            source_type=source_type,
            source_hash=source_hash,
            metadata_json=extract_metadata(path, source_type),
            content=content,
            summary=summarize(content),
            classification=classify_document(content),
            keywords_json=extract_keywords(content),
            owner_id=int(get_jwt_identity()) if get_jwt_identity() else None,
        )
        db.session.add(document)
        db.session.commit()
        entities = build_graph_for_document(document)
        audit("document_ingested", actor=str(get_jwt_identity()), filename=filename, entities=len(entities))
        return jsonify({"document": document.to_dict(), "entities_created": len(entities)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to save document: {str(e)}"}), 500


def bulk_upload():
    files = request.files.getlist("files")
    source_type = request.form.get("source_type", "text")
    results = []
    for file in files:
        if not file or not allowed_file(file.filename):
            results.append({"filename": getattr(file, "filename", "unknown"), "status": "skipped"})
            continue
        response, status = _process_uploaded_file(file, source_type)
        payload = response.get_json()
        results.append({"filename": file.filename, "status": status, "result": payload})
    return jsonify({
        "message": "Bulk ingestion completed.",
        "source_type": source_type,
        "files": results,
    })


def list_documents():
    docs = Document.query.order_by(Document.created_at.desc()).limit(100).all()
    return jsonify({"documents": [doc.to_dict() for doc in docs]})
