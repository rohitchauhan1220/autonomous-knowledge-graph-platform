from flask import Blueprint
from flask_jwt_extended import jwt_required
from backend.controllers import auth_controller

auth_bp = Blueprint("auth", __name__)
auth_bp.post("/signup")(auth_controller.signup)
auth_bp.post("/login")(auth_controller.login)
auth_bp.post("/forgot-password")(auth_controller.forgot_password)
auth_bp.post("/reset-password")(auth_controller.reset_password)
auth_bp.get("/me")(jwt_required()(auth_controller.me))
