from flask import Blueprint
from flask_jwt_extended import jwt_required
from backend.controllers import ingestion_controller

ingestion_bp = Blueprint("ingestion", __name__)
ingestion_bp.post("/upload")(jwt_required()(ingestion_controller.upload_document))
ingestion_bp.post("/bulk-upload")(jwt_required()(ingestion_controller.bulk_upload))
ingestion_bp.get("/documents")(jwt_required()(ingestion_controller.list_documents))
