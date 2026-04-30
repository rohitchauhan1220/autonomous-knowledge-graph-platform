from flask import Blueprint
from backend.controllers import admin_controller
from backend.middleware.auth_middleware import role_required

admin_bp = Blueprint("admin", __name__)
admin_bp.get("/users")(role_required("admin")(admin_controller.users))
admin_bp.route("/users/<int:user_id>", methods=["PATCH", "DELETE"])(role_required("admin")(admin_controller.user_detail))
admin_bp.get("/audit-logs")(role_required("admin")(admin_controller.audit_logs))
admin_bp.route("/integrations", methods=["GET", "POST"])(role_required("admin")(admin_controller.integrations))
admin_bp.route("/integrations/<int:integration_id>", methods=["PATCH", "DELETE"])(role_required("admin")(admin_controller.integration_detail))
admin_bp.route("/scheduled-ingestion", methods=["GET", "POST"])(role_required("admin")(admin_controller.scheduled_ingestion))
admin_bp.route("/scheduled-ingestion/<int:job_id>", methods=["PATCH", "DELETE"])(role_required("admin")(admin_controller.scheduled_ingestion_detail))
