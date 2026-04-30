from datetime import datetime
from backend.services.analytics_service import executive_insights


def build_executive_report():
    insight = executive_insights()
    return {
        "title": "Executive Knowledge Intelligence Report",
        "generated_at": datetime.utcnow().isoformat(),
        "summary": insight["headline"],
        "recommendations": insight["recommendations"],
        "roi_estimate": insight["roi_estimate"],
        "sections": [
            {"name": "Risk Overview", "content": f"Current risk score is {insight['risk_score']} with {insight['confidence']}% confidence."},
            {"name": "Decision Support", "content": "Focus on dependency-heavy suppliers and unresolved incident clusters."},
            {"name": "Next Actions", "content": "Export audit evidence, validate entities, and schedule the next ingestion run."},
        ],
    }
