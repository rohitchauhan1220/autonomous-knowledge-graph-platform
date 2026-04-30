from flask import Blueprint
from flask_jwt_extended import jwt_required
from backend.controllers import graph_controller

graph_bp = Blueprint("graph", __name__)
graph_bp.get("/snapshot")(jwt_required()(graph_controller.graph_snapshot))
graph_bp.get("/traverse/<int:entity_id>")(jwt_required()(graph_controller.traverse))
graph_bp.get("/versions")(jwt_required()(graph_controller.versions))
graph_bp.get("/annotations/<int:entity_id>")(jwt_required()(graph_controller.list_annotations))
graph_bp.post("/annotations/<int:entity_id>")(jwt_required()(graph_controller.add_annotation))
