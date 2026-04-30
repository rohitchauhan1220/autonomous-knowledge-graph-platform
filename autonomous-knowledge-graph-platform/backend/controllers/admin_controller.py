from flask import jsonify, request
from backend.models.analytics_model import AuditLog
from backend.models.user_model import User
from backend.models.enterprise_model import IntegrationConfig, ScheduledIngestion
from backend.services.audit_logger import audit
from config.database import db


def users():
    return jsonify({"users": [user.to_dict() for user in User.query.order_by(User.created_at.desc()).all()]})


def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "DELETE":
        username = user.email
        db.session.delete(user)
        db.session.commit()
        audit("user_deleted", target=username)
        return jsonify({"message": "User deleted"})

    payload = request.get_json() or {}
    for field in ("name", "email", "role", "organization", "department", "tenant_id"):
        if field in payload and payload[field] is not None:
            setattr(user, field, payload[field])
    if payload.get("password"):
        user.set_password(payload["password"])
    db.session.commit()
    audit("user_updated", target=user.email)
    return jsonify({"user": user.to_dict()})


def audit_logs():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    return jsonify({"audit_logs": [log.to_dict() for log in logs]})


def integrations():
    if request.method == "POST":
        payload = request.get_json() or {}
        item = IntegrationConfig(provider=payload.get("provider", "custom-api"), config_json=payload.get("config", {}))
        db.session.add(item)
        db.session.commit()
        audit("integration_configured", provider=item.provider)
        return jsonify({"integration": item.to_dict()}), 201
    items = IntegrationConfig.query.order_by(IntegrationConfig.created_at.desc()).all()
    return jsonify({"integrations": [item.to_dict() for item in items]})


def integration_detail(integration_id):
    item = IntegrationConfig.query.get_or_404(integration_id)
    if request.method == "DELETE":
        provider = item.provider
        db.session.delete(item)
        db.session.commit()
        audit("integration_deleted", provider=provider)
        return jsonify({"message": "Integration deleted"})

    payload = request.get_json() or {}
    if "provider" in payload and payload["provider"] is not None:
        item.provider = payload["provider"]
    if "status" in payload and payload["status"] is not None:
        item.status = payload["status"]
    if "config" in payload and payload["config"] is not None:
        item.config_json = payload["config"]
    db.session.commit()
    audit("integration_updated", provider=item.provider)
    return jsonify({"integration": item.to_dict()})


def scheduled_ingestion():
    if request.method == "POST":
        payload = request.get_json() or {}
        job = ScheduledIngestion(
            name=payload.get("name", "Daily enterprise sync"),
            source_type=payload.get("source_type", "api"),
            cadence=payload.get("cadence", "daily"),
        )
        db.session.add(job)
        db.session.commit()
        audit("scheduled_ingestion_created", name=job.name)
        return jsonify({"job": job.to_dict()}), 201
    jobs = ScheduledIngestion.query.order_by(ScheduledIngestion.created_at.desc()).all()
    return jsonify({"jobs": [job.to_dict() for job in jobs]})


def scheduled_ingestion_detail(job_id):
    job = ScheduledIngestion.query.get_or_404(job_id)
    if request.method == "DELETE":
        name = job.name
        db.session.delete(job)
        db.session.commit()
        audit("scheduled_ingestion_deleted", name=name)
        return jsonify({"message": "Scheduled ingestion deleted"})

    payload = request.get_json() or {}
    for field in ("name", "source_type", "cadence", "is_active"):
        if field in payload and payload[field] is not None:
            setattr(job, field, payload[field])
    db.session.commit()
    audit("scheduled_ingestion_updated", name=job.name)
    return jsonify({"job": job.to_dict()})
