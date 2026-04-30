from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import create_app
from config.database import db
from backend.models.user_model import User
from backend.models.document_model import Document
from backend.models.enterprise_model import IntegrationConfig, ScheduledIngestion
from backend.services.graph_builder import build_graph_for_document


def seed():
    app = create_app()
    with app.app_context():
        if not User.query.filter_by(email="admin@example.com").first():
            admin = User(name="Enterprise Admin", email="admin@example.com", role="admin")
            admin.set_password("Admin@123")
            db.session.add(admin)
        if not User.query.filter_by(email="analyst@example.com").first():
            analyst = User(name="Business Analyst", email="analyst@example.com", role="analyst", department="Supply Chain")
            analyst.set_password("Analyst@123")
            db.session.add(analyst)
        if not Document.query.filter_by(source_hash="seed-supplier-risk-report").first():
            doc = Document(
                filename="supplier_risk_report.txt",
                source_type="text",
                source_hash="seed-supplier-risk-report",
                summary="Atlas Logistics reported a 14% delivery delay risk for Q3 due to port congestion.",
                content="Atlas Logistics reported a 14% delivery delay risk for Q3. Orion Cloud depends on Atlas Logistics for west region fulfillment. Procurement opened escalation ticket INC-2407.",
                classification="Supply Chain Intelligence",
                keywords_json=["supplier", "delivery", "risk", "procurement", "orion"],
            )
            db.session.add(doc)
            db.session.commit()
            build_graph_for_document(doc)
        if not IntegrationConfig.query.first():
            db.session.add(IntegrationConfig(provider="Jira", status="demo-ready", config_json={"workspace": "enterprise-demo"}))
            db.session.add(IntegrationConfig(provider="Slack", status="demo-ready", config_json={"channel": "#risk-intelligence"}))
        if not ScheduledIngestion.query.first():
            db.session.add(ScheduledIngestion(name="Daily supplier intelligence sync", source_type="api", cadence="daily"))
        db.session.commit()
        print("Seed complete. Login: admin@example.com / Admin@123")


if __name__ == "__main__":
    seed()
