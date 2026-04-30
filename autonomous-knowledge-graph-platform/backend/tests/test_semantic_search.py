from backend.app import create_app
from backend.models.document_model import Document
from backend.models.entity_model import Entity
from backend.services.semantic_search import search
from config.database import db


def make_app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.drop_all()
        db.create_all()
    return app


def test_semantic_search_matches_question_terms_across_document_fields():
    app = make_app()
    with app.app_context():
        db.session.add(Document(
            filename="supplier_risk_report.txt",
            source_type="text",
            summary="Atlas Logistics reported a 14% delivery delay risk.",
            content="Orion Cloud depends on Atlas Logistics for west region fulfillment.",
            classification="Supply Chain Intelligence",
            keywords_json=["supplier", "delivery", "risk"],
        ))
        db.session.commit()

        results = search("Which suppliers have delivery risk?")

    assert [doc["filename"] for doc in results["documents"]] == ["supplier_risk_report.txt"]


def test_semantic_search_matches_entities_with_plural_question_terms():
    app = make_app()
    with app.app_context():
        db.session.add(Entity(
            name="Atlas Logistics",
            label="Supplier",
            canonical_id="Supplier:atlas logistics",
        ))
        db.session.commit()

        results = search("Which suppliers are risky?")

    assert [entity["name"] for entity in results["entities"]] == ["Atlas Logistics"]


def test_semantic_search_returns_source_documents_for_entity_only_matches():
    app = make_app()
    with app.app_context():
        document = Document(
            filename="entity_source.txt",
            source_type="text",
            summary="Operational intelligence source.",
            content="General source content.",
        )
        db.session.add(document)
        db.session.flush()
        db.session.add(Entity(
            name="Delivery Risk",
            label="Risk",
            canonical_id="Risk:delivery risk",
            document_id=document.id,
        ))
        db.session.commit()

        results = search("Which documents contain delivery risk?")

    assert [doc["filename"] for doc in results["documents"]] == ["entity_source.txt"]
