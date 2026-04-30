from config.database import db


class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    label = db.Column(db.String(80), default="Concept")
    attributes_json = db.Column(db.JSON, default=dict)
    canonical_id = db.Column(db.String(255), index=True, nullable=True)
    document_id = db.Column(db.Integer, db.ForeignKey("document.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "label": self.label,
            "attributes": self.attributes_json or {},
            "canonical_id": self.canonical_id,
            "document_id": self.document_id,
        }
