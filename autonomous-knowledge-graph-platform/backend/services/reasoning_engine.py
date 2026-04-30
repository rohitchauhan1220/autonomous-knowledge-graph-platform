from backend.models.document_model import Document
from backend.models.query_model import QueryLog
from backend.services.openai_service import OpenAIService
from backend.services.gemini_service import GeminiService
from backend.services.semantic_search import search
from config.database import db


class ReasoningEngine:
    def __init__(self):
        self.openai = OpenAIService()
        self.gemini = GeminiService()

    def answer(self, question, user_id=None):
        results = search(question, limit=5)
        docs = results["documents"]
        context = "\n".join(f"{doc['filename']}: {doc.get('summary') or ''}" for doc in docs)
        answer = self.openai.answer(question, context) or self.gemini.generate_insight(question, context)
        if not answer:
            answer = self._offline_answer(question, docs)
        sources = [{"document": doc["filename"], "id": doc["id"]} for doc in docs]
        log = QueryLog(question=question, answer=answer, sources_json=sources, user_id=user_id)
        db.session.add(log)
        db.session.commit()
        return {"answer": answer, "sources": sources, "search_results": results}

    def _offline_answer(self, question, docs):
        if not docs:
            try:
                count = Document.query.count()
            except RuntimeError:
                count = 0
            return f"No direct source matched the query. The graph currently contains {count} documents; ingest more data or broaden the terms."
        names = ", ".join(doc["filename"] for doc in docs[:3])
        return f"Based on matched enterprise sources ({names}), the likely answer is connected to the highlighted documents and their extracted entities. Enable OpenAI or Gemini keys for deeper natural-language reasoning."
