import secrets
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity
from config.database import db
from backend.models.user_model import User
from backend.services.audit_logger import audit
from backend.utils.validators import password_strength_error


def signup():
    payload = request.get_json() or {}
    if User.query.filter_by(email=payload.get("email")).first():
        return jsonify({"error": "Email already registered"}), 409
    password = payload.get("password", "")
    if error := password_strength_error(password):
        return jsonify({"error": error}), 400
    user = User(
        name=payload.get("name", "Enterprise User"),
        email=payload.get("email", ""),
        role=payload.get("role", "analyst"),
        organization=payload.get("organization", "Demo Enterprise"),
        department=payload.get("department", "Enterprise Intelligence"),
        tenant_id=payload.get("tenant_id", "demo-tenant"),
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"user": user.to_dict()}), 201


def login():
    payload = request.get_json() or {}
    user = User.query.filter_by(email=payload.get("email")).first()
    if not user or not user.check_password(payload.get("password", "")):
        return jsonify({"error": "Invalid credentials"}), 401
    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role, "email": user.email})
    return jsonify({"access_token": token, "user": user.to_dict()})


def me():
    user = User.query.get(int(get_jwt_identity()))
    return jsonify({"user": user.to_dict()})


def forgot_password():
    """Demo-safe password reset: returns token instead of sending email."""
    payload = request.get_json() or {}
    user = User.query.filter_by(email=payload.get("email")).first()
    if not user:
        return jsonify({"message": "If the account exists, a reset link was generated."})
    user.reset_token = secrets.token_urlsafe(24)
    db.session.commit()
    audit("password_reset_requested", actor=user.email)
    return jsonify({
        "message": "Reset token generated for demo use.",
        "reset_token": user.reset_token,
    })


def reset_password():
    payload = request.get_json() or {}
    user = User.query.filter_by(reset_token=payload.get("reset_token")).first()
    if not user:
        return jsonify({"error": "Invalid reset token"}), 400
    new_password = payload.get("new_password", "")
    if error := password_strength_error(new_password):
        return jsonify({"error": error}), 400
    user.set_password(new_password)
    user.reset_token = None
    db.session.commit()
    audit("password_reset_completed", actor=user.email)
    return jsonify({"message": "Password updated successfully"})
