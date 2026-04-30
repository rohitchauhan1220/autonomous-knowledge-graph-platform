from config.database import db
from backend.models.analytics_model import AuditLog


def audit(action, actor="system", **details):
    log = AuditLog(actor=actor, action=action, details_json=details)
    db.session.add(log)
    db.session.commit()
    return log
