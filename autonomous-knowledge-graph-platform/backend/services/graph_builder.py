from config.database import db
from backend.models.entity_model import Entity
from backend.models.relation_model import Relation
from backend.models.enterprise_model import GraphVersion
from backend.services import nlp_service


def build_graph_for_document(document):
    extracted = nlp_service.extract_entities(document.content)
    created_entities = []
    for item in extracted:
        # Canonical IDs help link the same entity across multiple documents.
        entity = Entity(
            name=item["name"],
            label=item["label"],
            attributes_json=item.get("attributes", {}),
            canonical_id=f"{item['label']}:{item['name'].strip().lower()}",
            document_id=document.id,
        )
        db.session.add(entity)
        created_entities.append(entity)
    db.session.flush()

    for idx in range(len(created_entities) - 1):
        db.session.add(Relation(
            source_entity_id=created_entities[idx].id,
            target_entity_id=created_entities[idx + 1].id,
            relation_type="CO_OCCURS_WITH",
            confidence=0.68,
            evidence=document.summary[:240],
            source_document_id=document.id,
        ))
    latest = GraphVersion.query.order_by(GraphVersion.version.desc()).first()
    db.session.add(GraphVersion(
        version=(latest.version + 1 if latest else 1),
        change_type="document_ingestion",
        summary=f"Added {len(created_entities)} entities from {document.filename}",
        document_id=document.id,
    ))
    db.session.commit()
    return created_entities
