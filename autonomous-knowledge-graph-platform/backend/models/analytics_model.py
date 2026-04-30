from datetime import datetime
from config.database import db


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor = db.Column(db.String(180), default="system")
    action = db.Column(db.String(120), nullable=False)
    details_json = db.Column(db.JSON, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "actor": self.actor,
            "action": self.action,
            "details": self.details_json or {},
            "created_at": self.created_at.isoformat(),
        }
