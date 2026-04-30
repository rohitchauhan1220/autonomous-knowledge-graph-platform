from datetime import datetime
from backend.models.document_model import Document
from backend.models.entity_model import Entity
from backend.models.relation_model import Relation
from backend.models.query_model import QueryLog


def executive_insights():
    """Generates deterministic boardroom metrics for offline presentation demos."""
    risk_entities = Entity.query.filter_by(label="Risk").count()
    total_docs = max(Document.query.count(), 1)
    risk_score = min(95, 40 + risk_entities * 8)
    return {
        "risk_score": risk_score,
        "confidence": 86,
        "headline": "Supplier and incident dependencies are the strongest intelligence signals.",
        "recommendations": [
            "Prioritize suppliers with delivery risk and high dependency edges.",
            "Review open incidents connected to renewal commitments.",
            "Schedule weekly graph refresh and executive report export.",
        ],
        "roi_estimate": {
            "manual_hours_saved": total_docs * 3,
            "estimated_cost_saving": total_docs * 2500,
        },
    }


def system_health():
    return {
        "status": "operational",
        "checked_at": datetime.utcnow().isoformat(),
        "api_latency_ms": 42,
        "ingestion_queue": 0,
        "documents": Document.query.count(),
        "entities": Entity.query.count(),
        "relations": Relation.query.count(),
        "queries": QueryLog.query.count(),
    }


def risk_heatmap():
    labels = ["Supply Chain", "IT Incidents", "Compliance", "Customer Success", "Procurement"]
    return [{"area": label, "risk": 45 + idx * 9, "trend": "up" if idx % 2 == 0 else "stable"} for idx, label in enumerate(labels)]
