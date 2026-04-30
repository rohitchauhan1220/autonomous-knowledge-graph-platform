from datetime import datetime
from config.database import db


class GraphVersion(db.Model):
    """Stores graph change checkpoints for timeline and rollback demos."""

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, nullable=False, index=True)
    change_type = db.Column(db.String(80), default="ingestion")
    summary = db.Column(db.Text, default="")
    document_id = db.Column(db.Integer, db.ForeignKey("document.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "version": self.version,
            "change_type": self.change_type,
            "summary": self.summary,
            "document_id": self.document_id,
            "created_at": self.created_at.isoformat(),
        }


class Annotation(db.Model):
    """Team comments attached to graph nodes for collaborative investigation."""

    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "entity_id": self.entity_id,
            "user_id": self.user_id,
            "note": self.note,
            "created_at": self.created_at.isoformat(),
        }


class IntegrationConfig(db.Model):
    """Marketplace-style integration registry without storing plain secrets."""

    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(40), default="configured")
    config_json = db.Column(db.JSON, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        safe_config = {key: value for key, value in (self.config_json or {}).items() if "key" not in key.lower()}
        return {
            "id": self.id,
            "provider": self.provider,
            "status": self.status,
            "config": safe_config,
            "created_at": self.created_at.isoformat(),
        }


class ScheduledIngestion(db.Model):
    """Represents scheduled connector jobs for demo and future worker queues."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    source_type = db.Column(db.String(80), default="api")
    cadence = db.Column(db.String(80), default="daily")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "source_type": self.source_type,
            "cadence": self.cadence,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }
