from datetime import datetime
from config.database import db


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    source_type = db.Column(db.String(50), nullable=False)
    source_hash = db.Column(db.String(80), index=True, nullable=True)
    status = db.Column(db.String(50), default="processed")
    classification = db.Column(db.String(100), default="General Intelligence")
    keywords_json = db.Column(db.JSON, default=list)
    metadata_json = db.Column(db.JSON, default=dict)
    summary = db.Column(db.Text, default="")
    content = db.Column(db.Text, default="")
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "source_type": self.source_type,
            "status": self.status,
            "classification": self.classification,
            "keywords": self.keywords_json or [],
            "metadata": self.metadata_json or {},
            "summary": self.summary,
            "created_at": self.created_at.isoformat(),
        }
