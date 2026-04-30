# API Documentation

Base URL: `http://localhost:5000/api`

## Auth

### POST `/auth/signup`
Creates an enterprise user.

Body:
```json
{"name":"Analyst","email":"analyst@example.com","password":"Password@123","role":"analyst","organization":"Demo Enterprise"}
```

### POST `/auth/login`
Returns a JWT access token.

### POST `/auth/forgot-password`
Generates a demo reset token. In production, send the token through email.

### POST `/auth/reset-password`
Updates the password using a reset token.

### GET `/auth/me`
Requires bearer token. Returns the current user.

## Ingestion

### POST `/ingestion/upload`
Multipart form:

- `file`: pdf, docx, csv, txt, eml, or json
- `source_type`: `pdf`, `email`, `ticket`, `csv`, `database`, or `text`

Returns the processed document and created entity count.

### POST `/ingestion/bulk-upload`
Multipart form with `files` array. Processes multiple enterprise files in one request.

### GET `/ingestion/documents`
Returns recent ingested documents.

## Graph

### GET `/graph/snapshot`
Returns Cytoscape-compatible nodes and edges.

### GET `/graph/traverse/<entity_id>`
Returns direct relationships for an entity.

### GET `/graph/versions`
Returns graph version history.

### GET/POST `/graph/annotations/<entity_id>`
Lists or creates collaborative graph-node annotations.

## Query

### GET `/query/search?q=supplier`
Returns matching documents and entities.

### POST `/query/ask`
Body:
```json
{"question":"Which suppliers have delivery risk?"}
```
Returns answer, source traces, and matched evidence.

### GET `/query/suggestions`
Returns demo-ready natural language query prompts.

### GET `/query/history`
Returns recent enterprise assistant queries.

## Dashboard

### GET `/dashboard/metrics`
Returns counts and KPI values.

### GET `/dashboard/activity`
Returns recent documents and recent queries.

### GET `/dashboard/executive-summary`
Returns AI-style business recommendations and ROI estimate.

### GET `/dashboard/heatmap`
Returns risk heatmap data.

### GET `/dashboard/health`
Returns system health and operational monitoring data.

### GET `/dashboard/report`
Returns an executive report payload for PDF/Excel export extensions.

## Admin

### GET `/admin/users`
Admin role required.

### GET `/admin/audit-logs`
Admin role required.

### GET/POST `/admin/integrations`
Admin role required. Lists or configures integration records.

### GET/POST `/admin/scheduled-ingestion`
Admin role required. Lists or creates scheduled ingestion jobs.
