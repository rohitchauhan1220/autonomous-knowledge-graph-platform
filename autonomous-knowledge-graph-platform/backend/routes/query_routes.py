from flask import Blueprint
from flask_jwt_extended import jwt_required
from backend.controllers import query_controller

query_bp = Blueprint("query", __name__)
query_bp.get("/search")(jwt_required()(query_controller.semantic_search))
query_bp.post("/ask")(jwt_required()(query_controller.ask))
query_bp.get("/suggestions")(jwt_required()(query_controller.suggestions))
query_bp.get("/history")(jwt_required()(query_controller.history))
