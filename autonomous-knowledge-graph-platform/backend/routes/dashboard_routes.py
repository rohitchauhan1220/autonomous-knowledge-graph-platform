from flask import Blueprint
from flask_jwt_extended import jwt_required
from backend.controllers import analytics_controller

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/metrics", methods=["GET"])
@jwt_required()
def metrics_route():
	return analytics_controller.dashboard_metrics()

@dashboard_bp.route("/activity", methods=["GET"])
@jwt_required()
def activity_route():
	return analytics_controller.recent_activity()

@dashboard_bp.route("/activity/documents/<int:document_id>", methods=["GET"])
@jwt_required()
def get_document(document_id):
	return analytics_controller.document_detail(document_id)

@dashboard_bp.route("/activity/documents/<int:document_id>", methods=["PATCH"])
@jwt_required()
def patch_document(document_id):
	return analytics_controller.update_document(document_id)

@dashboard_bp.route("/activity/documents/<int:document_id>", methods=["DELETE"])
@jwt_required()
def delete_doc(document_id):
	return analytics_controller.delete_document(document_id)

@dashboard_bp.route("/activity/queries/<int:query_id>", methods=["GET"])
@jwt_required()
def get_query(query_id):
	return analytics_controller.query_detail(query_id)

@dashboard_bp.route("/activity/queries/<int:query_id>", methods=["PATCH"])
@jwt_required()
def patch_query(query_id):
	return analytics_controller.update_query(query_id)

@dashboard_bp.route("/activity/queries/<int:query_id>", methods=["DELETE"])
@jwt_required()
def delete_qry(query_id):
	return analytics_controller.delete_query(query_id)

@dashboard_bp.route("/executive-summary", methods=["GET"])
@jwt_required()
def exec_summary():
	return analytics_controller.executive_summary()

@dashboard_bp.route("/health", methods=["GET"])
@jwt_required()
def health_route():
	return analytics_controller.health()

@dashboard_bp.route("/heatmap", methods=["GET"])
@jwt_required()
def heatmap_route():
	return analytics_controller.heatmap()

@dashboard_bp.route("/report", methods=["GET"])
@jwt_required()
def report_route():
	return analytics_controller.report()
