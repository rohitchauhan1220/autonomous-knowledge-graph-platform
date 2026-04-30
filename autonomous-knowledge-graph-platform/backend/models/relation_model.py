from config.database import db


class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"))
    target_entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"))
    relation_type = db.Column(db.String(100), default="RELATED_TO")
    confidence = db.Column(db.Float, default=0.72)
    evidence = db.Column(db.Text, default="")
    source_document_id = db.Column(db.Integer, db.ForeignKey("document.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "source": self.source_entity_id,
            "target": self.target_entity_id,
            "type": self.relation_type,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "source_document_id": self.source_document_id,
        }
