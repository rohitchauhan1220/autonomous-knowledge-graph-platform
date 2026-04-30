# Architecture

```text
Browser UI
  |-- Dashboard
  |-- Upload Console
  |-- Cytoscape Graph
  |-- Query Assistant
  |-- Admin Panel
        |
        v
Flask REST API
  |-- Auth Routes -> User Model -> SQLite
  |-- Ingestion Routes -> Parsers -> NLP Service -> Graph Builder
  |-- Query Routes -> Semantic Search -> Reasoning Engine
  |-- Dashboard Routes -> Analytics Models
  |-- Admin Routes -> Audit Logs
        |
        v
Data Layer
  |-- SQLite for MVP metadata
  |-- Neo4j connector for production graph persistence
  |-- graph_data for samples, exports, backups
        |
        v
AI Layer
  |-- OpenAI for extraction, summarization, Q&A
  |-- Gemini for contextual reasoning and insight generation
  |-- Rule-based fallback for offline demos
```

## Scalability Path

- Move ingestion to Celery or cloud queues.
- Store large documents in S3, Azure Blob, or GCS.
- Promote Neo4j as the authoritative graph store.
- Split reasoning, ingestion, and graph services into deployable microservices.
- Add vector search with pgvector, OpenSearch, or managed vector databases.
