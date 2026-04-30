# User-Friendly Code Overview

## Main Entry Points

- `backend/app.py`: Flask app factory, route registration, middleware, and static frontend serving.
- `run_dev.py`: Simple local development runner.
- `backend/database/seed_data.py`: Creates demo users, graph data, integrations, and scheduled ingestion jobs.
- `frontend/dashboard.html`: Main executive command center.

## Backend Flow

1. A user logs in through `/api/auth/login`.
2. The frontend stores the JWT token in browser local storage.
3. A document is uploaded through `/api/ingestion/upload`.
4. The backend parses, normalizes, classifies, summarizes, and extracts keywords.
5. Entities and relationships are created by `backend/services/graph_builder.py`.
6. Graph versions are stored for timeline/history features.
7. The query assistant searches documents and generates source-backed answers.

## Important Service Files

- `nlp_service.py`: Offline NER, keyword extraction, document classification, and clustering helpers.
- `reasoning_engine.py`: Source-backed answer generation with OpenAI/Gemini fallback support.
- `analytics_service.py`: Executive insights, risk heatmap, ROI estimate, and system health.
- `report_service.py`: Executive report payload generation.

## How To Explain The Project

This project is not only a CRUD dashboard. It demonstrates a full enterprise intelligence pipeline:

`Data ingestion -> NLP processing -> Knowledge graph construction -> Reasoning -> Explainable dashboard -> Admin governance`

The code is intentionally modular so each piece can later become its own microservice.
