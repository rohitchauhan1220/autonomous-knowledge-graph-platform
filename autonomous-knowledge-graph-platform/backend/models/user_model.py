from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(40), default="analyst")
    organization = db.Column(db.String(160), default="Demo Enterprise")
    department = db.Column(db.String(120), default="Enterprise Intelligence")
    tenant_id = db.Column(db.String(80), default="demo-tenant", index=True)
    reset_token = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "organization": self.organization,
            "department": self.department,
            "tenant_id": self.tenant_id,
        }
