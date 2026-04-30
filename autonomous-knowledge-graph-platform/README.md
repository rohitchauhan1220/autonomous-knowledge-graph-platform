# Autonomous Knowledge Graph Platform (AKG) - Enterprise Edition

An enterprise-grade full-stack platform that ingests documents, intelligently extracts entities and relationships, constructs a dynamic knowledge graph, and enables semantic reasoning on source-backed data. Perfect for supply chain analytics, risk management, compliance, and operational intelligence.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Core Features](#core-features)
- [System Architecture](#system-architecture)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [User Interface Guide](#user-interface-guide)
- [API Endpoints Reference](#api-endpoints-reference)
- [Database Schema](#database-schema)
- [Configuration & Deployment](#configuration--deployment)
- [Testing & Quality](#testing--quality)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

### Purpose
The Autonomous Knowledge Graph Platform helps enterprises:
- **Ingest** diverse data sources (documents, emails, tickets, CSVs, structured data)
- **Extract** meaningful entities and relationships using AI and NLP techniques
- **Construct** a queryable knowledge graph that captures business relationships and dependencies
- **Analyze** complex patterns, risks, and insights through interactive visualization
- **Reason** over the graph to answer natural-language semantic queries with source attribution

### Target Use Cases
- Supply chain visibility and risk management
- Enterprise compliance and audit trails
- Customer relationship intelligence
- IT incident and asset management
- Regulatory reporting and documentation
- Cross-functional knowledge discovery

### Technology Stack
- **Backend:** Python 3.8+, Flask, SQLAlchemy ORM, JWT authentication
- **Frontend:** Vanilla JavaScript, HTML5, CSS3 (no framework)
- **Graph Visualization:** Cytoscape.js with dynamic layout algorithms
- **Database:** SQLite (development), PostgreSQL (production-ready)
- **Optional Graph DB:** Neo4j for advanced graph queries and analytics
- **AI/NLP:** OpenAI GPT and Google Gemini adapters with offline rule-based fallback
- **Deployment:** Docker, Docker Compose, Gunicorn, Nginx, AWS/Azure ready

---

## ✨ Core Features

### Authentication & Access Control
- **Multi-user support:** Secure signup, login, logout workflows with JWT tokens
- **Role-based access control (RBAC):** Admin, Analyst, Viewer roles with permission boundaries
- **Password security:** Hashed passwords, forgot-password workflow, session management
- **Multi-tenant ready:** Isolated workspaces per user organization

### Document Ingestion & Processing
- **Multi-format support:** PDFs, DOCX, emails (.eml), CSV, JSON, plain text, and ticket archives
- **Bulk ingestion:** Single-file and batch upload endpoints with progress tracking
- **Metadata extraction:** Automatic title, author, date, language detection
- **Duplicate detection:** Content-based and metadata-based deduplication with collision reporting
- **Data normalization:** Text cleaning, encoding standardization, format unification
- **Quota management:** Per-user and system-wide document storage limits with warnings

### Entity & Relationship Extraction
- **Entity extraction:** Automatic identification of people, organizations, locations, dates, products, concepts
- **Relationship extraction:** Detects links like "depends-on", "reports-to", "contains", "impacts", "references"
- **Confidence scoring:** ML-based confidence levels for each extraction (0-1 scale)
- **Custom entity types:** Admin-configurable entity taxonomies for domain-specific extraction
- **Source attribution:** Every entity and relationship links back to source document and exact text span

### Knowledge Graph Construction
- **Graph versioning:** Track graph evolution over time with snapshot capability
- **Node types:** Hierarchical classification (Primary, Secondary, Tertiary) for entity importance
- **Edge types:** Labeled relationships with directionality and metadata
- **Graph statistics:** Node count, edge density, centrality measures, connected components
- **Visualization:**
  - **Tree layout:** Hierarchical breadth-first display for organizational structures
  - **Force-directed layout:** Cose algorithm for cluster visualization
  - **Node filtering:** Filter by type, keyword, or importance level
  - **Edge labels:** Relationship type labels and directionality indicators
  - **Node numbering:** Automatic sequential numbering for tree/summary views (1-20 nodes per visualization)

### Dashboard & Analytics
- **Executive Summary Dashboard:**
  - KPI cards: Document count, entity count, relationships found, graph connections
  - Recent activity feed: Shows latest document ingestions and query executions
  - Executive AI Insight: AI-generated operational insights with recommended actions and graph navigation
  - Risk Heatmap: Risk severity assessment by area/category with drill-down capability (clickable tiles with details)
  - System Health: Key performance indicators (health checks, processing speed, storage utilization)
- **Activity Management:**
  - View, edit, and delete recent ingested documents and queries
  - Inline edit buttons for metadata updates
  - Permanent delete with confirmation
  - Filter by type, date range, or status

### Semantic Query & Reasoning
- **Natural language query interface:** Type questions in plain English; system returns graph-backed answers
- **Query history:** Log of all user queries with execution time and result count
- **Source attribution:** Every answer includes links to source documents and relevant nodes
- **Query analysis:** Show matching entities, relationships, and inference paths
- **Graph pattern matching:** Find subgraph patterns and motifs

### Graph Visualization Features
- **Interactive Cytoscape rendering:**
  - Zoom and pan controls
  - Auto-fit and center options
  - Node highlighting and selection
  - Tooltip information on hover
  - Click-to-expand subgraph capability
- **Graph Evolution Timeline:** Toggle between multiple graph versions; see changes over time
- **Tree Summary:** Below-graph display showing numbered node list (1-20) with type badges for readability
- **Layout toggle:** Switch between tree (breadth-first) and force-directed layouts on demand
- **Export options:** Save graph as JSON, PNG snapshot, or CSV edge list

### Admin & Settings Panel
- **User management:**
  - View all users with role and status
  - Create new user accounts with email and role assignment
  - Edit user details (name, email, role)
  - Deactivate or delete users with audit trail
- **System integrations:**
  - Configure API keys (OpenAI, Gemini, Neo4j)
  - Enable/disable specific AI providers
  - Toggle offline mode (use rule-based NLP if all AI unavailable)
- **Ingestion settings:**
  - Entity extraction confidence thresholds
  - Relationship extraction minimum scores
  - Duplicate detection sensitivity
- **Scheduled tasks:**
  - Graph optimization jobs
  - Backup scheduling
  - Data retention policies
  - Bulk re-indexing

---

## 🏗️ System Architecture

### Backend Structure (`backend/`)
```
backend/
├── app.py                    # Flask application factory and WSGI entry point
├── wsgi.py                   # Production WSGI configuration for Gunicorn
├── controllers/              # Request handlers by domain
│   ├── admin_controller.py      # User, integration, and settings management
│   ├── analytics_controller.py  # Dashboard metrics, health, activity detail
│   ├── auth_controller.py       # Login, signup, JWT token generation
│   ├── graph_controller.py      # Graph snapshots, versioning, layout algorithms
│   ├── ingestion_controller.py  # Document upload, parsing, duplicate detection
│   ├── query_controller.py      # Semantic query execution and history
│   └── reasoning_controller.py  # AI-powered reasoning and insights
├── routes/                   # Blueprint route registration
│   ├── admin_routes.py          # /api/admin/* endpoints
│   ├── auth_routes.py           # /api/auth/* endpoints
│   ├── dashboard_routes.py      # /api/dashboard/* endpoints
│   ├── graph_routes.py          # /api/graph/* endpoints
│   ├── ingestion_routes.py      # /api/ingestion/* endpoints
│   ├── query_routes.py          # /api/query/* endpoints
│   └── reasoning_routes.py      # /api/reasoning/* endpoints
├── services/                 # Business logic layer (NLP, AI, graph ops)
│   ├── entity_service.py        # Entity extraction and management
│   ├── graph_service.py         # Graph construction and queries
│   ├── nlp_service.py           # Text processing and NLP
│   ├── ai_service.py            # AI adapter (OpenAI, Gemini, fallback)
│   ├── ingestion_service.py     # Document parsing pipeline
│   └── analytics_service.py     # Dashboard metrics calculation
├── models/                   # SQLAlchemy ORM models
│   ├── user_model.py            # User accounts and authentication
│   ├── document_model.py        # Ingested documents and metadata
│   ├── entity_model.py          # Graph entities/nodes
│   ├── relation_model.py        # Graph relationships/edges
│   ├── query_model.py           # Semantic query execution logs
│   ├── graph_model.py           # Graph versions and snapshots
│   ├── analytics_model.py       # Dashboard metrics and heatmap
│   └── enterprise_model.py      # Enterprise-specific data (integrations, config)
├── database/                 # Database layer
│   ├── sql_connector.py         # SQLAlchemy session management
│   ├── neo4j_connector.py       # Optional Neo4j integration
│   ├── seed_data.py             # Demo data initialization script
│   └── migrations/              # Alembic migration files (versioning)
├── middleware/               # Request/response middleware
│   ├── auth_middleware.py       # JWT token validation and user extraction
│   ├── error_handler.py         # Global exception handling and logging
│   ├── rate_limiter.py          # API rate limiting per user
│   └── request_logger.py        # Request/response logging for audit
├── utils/                    # Utility functions and helpers
│   ├── validators.py            # Input validation schemas
│   ├── parsers.py               # File parsing logic for various formats
│   ├── formatters.py            # Response formatting utilities
│   └── decorators.py            # Custom decorators (auth, logging, etc.)
└── tests/                    # Test suite
    ├── test_auth.py             # Authentication flow tests
    ├── test_ingestion.py        # Document ingestion tests
    ├── test_graph.py            # Graph construction tests
    ├── test_query.py            # Query execution tests
    └── test_analytics.py        # Dashboard analytics tests
```

### Frontend Structure (`frontend/`)
```
frontend/
├── index.html               # Landing / home page
├── login.html               # User login form
├── dashboard.html           # Main dashboard (KPIs, activities, insights)
├── graph.html               # Graph visualization and exploration
├── query.html               # Semantic query console
├── admin.html               # Settings/admin panel
├── assets/
│   ├── css/
│   │   ├── style.css            # Global styles, theme, layout
│   │   ├── dashboard.css        # Dashboard-specific styles
│   │   ├── graph.css            # Graph visualization styles
│   │   └── admin.css            # Admin panel styles
│   └── js/
│       ├── main.js              # Common initialization and utilities
│       ├── api_service.js       # API client wrapper (JWT, error handling)
│       ├── dashboard.js         # Dashboard logic (metrics, activity, panels)
│       ├── graph_visualization.js # Cytoscape rendering and interaction
│       ├── query_console.js     # Query input and result display
│       └── admin.js             # Settings and user management UI
└── components/              # Reusable HTML components (modals, cards, etc.)
```

### Configuration (`config/`)
```
config/
├── settings.py              # Global settings (debug, environment)
├── security.py              # Password hashing, JWT config
├── database.py              # SQLAlchemy database URI
├── logging_config.py        # Logging level and format
├── api_keys.py              # External API credentials (from .env)
└── cache_config.py          # Redis/cache settings (optional)
```

### Data & Deployment
```
graph_data/                  # Graph and document storage
├── raw_documents/              # Uploaded files
├── processed_data/             # Extracted entities and relations
├── graph_exports/              # Graph snapshots (JSON, CSV)
├── backups/                    # Database backups
└── sample_datasets/            # Demo files for testing

deployment/                  # Deployment configuration
├── aws/                        # AWS CloudFormation, ECS configs
├── azure/                      # Azure Container Instances templates
├── kubernetes/                 # K8s manifests and Helm charts
├── docker/                     # Dockerfile optimizations
├── nginx/                      # Nginx reverse proxy config
├── gunicorn/                   # Gunicorn WSGI app server config
└── ci_cd/                      # GitHub Actions, GitLab CI workflows

scripts/                     # Automation scripts
├── initial_setup.sh            # First-time environment setup
├── run_dev.py                  # Development server launcher
├── run_dev.sh                  # Bash wrapper for dev server
├── run_tests.sh                # Test execution wrapper
├── model_training.sh           # NLP model training pipeline
├── data_ingestion.sh           # Bulk ingestion orchestration
├── deployment.sh               # Deploy to cloud
└── graph_backup.sh             # Backup graph and docs
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python:** 3.8 or higher
- **pip & virtualenv:** For dependency management
- **Node.js (optional):** For frontend tooling (linting, testing)
- **SQLite3:** Included with Python; or PostgreSQL for production
- **Docker (optional):** For containerized deployment

### Step 1: Clone & Navigate
```bash
cd "c:\Users\Rohit Chauhan\OneDrive\Desktop\Project By Pranshu Chauhan\autonomous-knowledge-graph-platform"
```

### Step 2: Create Virtual Environment
```bash
# On Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1

# On Windows CMD
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create Environment File
```bash
# Copy template
copy .env.example .env

# Edit .env with your configuration:
# SECRET_KEY=your-secret-key-here
# JWT_SECRET_KEY=your-jwt-secret
# OPENAI_API_KEY=sk-... (optional)
# GEMINI_API_KEY=... (optional)
# DATABASE_URL=sqlite:///instance/app.db
```

### Step 5: Initialize Database
```bash
# Create instance directory
mkdir instance

# Run seed script to create demo data
python backend/database/seed_data.py
```

### Step 6: Verify Installation
```bash
# Check Python environment
python -c "import flask, sqlalchemy; print('✓ Dependencies installed')"

# Check if app starts (will print Flask debug info)
python run_dev.py
```

---

## 🏃 Running the Application

### Development Mode
```bash
# Option 1: Using provided script
python run_dev.py

# Option 2: Direct Flask
set FLASK_APP=backend.app
set FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000

# Option 3: On Linux/macOS
export FLASK_APP=backend.app
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

### Access Application
- **URL:** `http://localhost:5000`
- **Default login:**
  - Email: `admin@example.com`
  - Password: `Admin@123`

### Production with Gunicorn
```bash
# Install gunicorn
pip install gunicorn

# Run with Gunicorn (4 workers, port 5000)
gunicorn -w 4 -b 0.0.0.0:5000 backend.wsgi:app
```

### Docker Deployment
```bash
# Build and run with Docker Compose (includes Flask, SQLite, optional Neo4j)
docker-compose up --build

# Access on http://localhost:5000
# Neo4j Browser on http://localhost:7474 (if enabled)

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

---

## 🎨 User Interface Guide

### Dashboard Page (`/dashboard.html`)
**Purpose:** Executive overview of all platform activity, insights, and health.

**Sections:**

1. **Metric Grid (Top)**
   - **Document Count:** Total ingested documents with upload rate
   - **Entity Count:** Nodes in the current knowledge graph
   - **Relationship Count:** Edges extracted and stored
   - **Connections:** Average edges per node (graph density indicator)
   - Click any card → opens detail modal with breakdown and trends

2. **Data Ingestion Panel (Left)**
   - **File selector:** Choose upload source (Text, PDF, Email, Ticket, CSV)
   - **File picker:** Browse and select file(s)
   - **Submit button:** Triggers ingestion pipeline with progress feedback
   - **Status display:** Shows processing steps (uploading, parsing, extracting, storing)
   - Error messages appear inline if upload fails (file too large, unsupported format, etc.)

3. **Recent Activity Panel (Right)**
   - Lists last 10 uploaded documents and executed queries
   - **Each item shows:** Timestamp, type (document/query), name/text, status
   - Click item → opens detail modal with:
     - Full metadata and extracted summary
     - Source content preview (first 500 chars)
     - **Edit button:** Modify document name, source type, or metadata
     - **Delete button:** Permanently remove from graph and database
     - **Open Graph button:** Jump to graph.html to visualize this document's connections

4. **Executive AI Insight Section (Three-Column Panel 1/3)**
   - AI-generated operational headline (e.g., "Supplier Dependency Risk Detected")
   - List of 3-5 actionable insights as clickable bullet points
   - Click insight → opens detail modal showing:
     - Detailed explanation of the signal
     - Why it matters to business operations
     - Recommended next steps (as numbered list)
     - **Open Graph button:** Navigate to graph view with context pre-set

5. **Risk Heatmap Section (Three-Column Panel 2/3)**
   - 4-6 risk tiles colored by severity (green=low, yellow=medium, red=high)
   - Each tile labeled with risk area (e.g., "Supply Chain", "Compliance", "IT Security")
   - Click tile → opens detail modal showing:
     - Risk description and impact assessment
     - Affected entities (list with count)
     - Affected documents (sample list)
     - Risk score (0-100 scale)

6. **System Health Section (Three-Column Panel 3/3)**
   - 4-5 health status items as clickable buttons
   - Status indicators: API response time, Database health, Graph storage usage, Processing queue depth, Cache hit ratio
   - Click item → opens detail modal with:
     - Current value and historical trend (sparkline chart)
     - Threshold and warning level
     - Recommendation if threshold breached

### Graph Page (`/graph.html`)
**Purpose:** Interactive visualization and exploration of the knowledge graph.

**Layout:**

1. **Top Toolbar**
   - **Layout toggle:** Switch between "Tree" (breadth-first, hierarchical) and "Force" (Cose, cluster-based) layouts
   - **Node filter:** Dropdown to filter by entity type (All, Person, Organization, Location, Product, Concept, etc.)
   - **Keyword search:** Search entities by name substring; highlights matching nodes
   - **Zoom controls:** Plus (zoom in), minus (zoom out), fit-all (auto-fit to canvas)

2. **Main Canvas (Central Area)**
   - Cytoscape.js rendering area showing graph nodes and edges
   - **Nodes:** Circles labeled with sequential numbers (1-20 in tree layout) or entity names (in force layout)
   - **Node colors:** Vary by type (orange=Person, blue=Organization, green=Location, etc.)
   - **Edges:** Lines showing relationships with optional label text
   - **Interactions:**
     - Hover over node → shows tooltip (entity name, type, document count)
     - Click node → highlights connected neighbors
     - Drag node → reposition (force layout only)
     - Double-click background → deselect all

3. **Tree Summary (Below Canvas)**
   - Visible in tree layout; shows numbered list of top 20 nodes
   - Format: "1. Entity Name [TYPE]" (e.g., "1. Supplier Risk [Concept]")
   - Left-border indentation for hierarchy
   - Expandable/collapsible sections for node groupings
   - Click entry → highlights corresponding node on canvas

4. **Graph Evolution Timeline (Right Side)**
   - Shows version selector dropdown
   - Options: "Current (v1)", "Version 2", "Version 3" (if available)
   - Change version → reloads graph with that snapshot
   - Displays version timestamp and change summary

### Query Page (`/query.html`)
**Purpose:** Natural-language querying interface with semantic reasoning.

**Layout:**

1. **Query Input**
   - Large text area: "Ask your question in plain English..."
   - Example prompt: "What are the top supplier risks in the current quarter?"
   - Submit button: "Execute Semantic Query" (or Enter key)

2. **Query Results**
   - Shows matched entities, relationships, and inference paths
   - Result cards display:
     - Entity name and type
     - Relevance score (0-100%)
     - Connected entities (list)
     - Source documents (clickable links)

3. **Query History (Right Sidebar)**
   - Lists last 20 executed queries
   - Shows query text, execution time, result count
   - Click item → rerun that query
   - Filter by date range or result type

### Settings/Admin Panel (`/admin.html`)
**Purpose:** System configuration and user management (admin-only access).

**Sections:**

1. **User Management**
   - Table showing all users: Email, Name, Role, Status, Created Date
   - **Add User button** → opens form with fields: Email, Name, Role dropdown, temporary password
   - **Edit button (pencil icon)** → modify user details inline
   - **Delete button (trash icon)** → remove user account permanently
   - Status indicators: Green=active, Gray=inactive

2. **API & Integrations**
   - **OpenAI Configuration:** API key input, model selector (GPT-3.5, GPT-4, etc.), enable/disable toggle
   - **Gemini Configuration:** API key input, model selector, enable/disable toggle
   - **Neo4j Configuration:** URI, username, password, connection test button
   - **Offline Mode Toggle:** Enable rule-based NLP fallback (no AI keys required)

3. **Extraction Settings**
   - **Entity Confidence Threshold:** Slider 0-100% (default 70%)
   - **Relationship Confidence Threshold:** Slider 0-100% (default 60%)
   - **Duplicate Detection Sensitivity:** Slider low/medium/high
   - Save button → updates configuration globally

4. **Scheduled Tasks**
   - List of scheduled jobs: Graph optimization, backups, re-indexing
   - Each job shows: Name, Schedule (hourly/daily/weekly), Last run time, Next run time
   - Edit and delete buttons for each job

---

## 📡 API Endpoints Reference

### Authentication (`/api/auth/`)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| POST | `/api/auth/signup` | Create new user account | Email, password, name | JWT token, user ID |
| POST | `/api/auth/login` | User login | Email, password | JWT token, user info |
| POST | `/api/auth/logout` | Logout (invalidate token) | JWT token | Success message |
| POST | `/api/auth/refresh-token` | Refresh JWT token | Expired token | New JWT token |
| POST | `/api/auth/forgot-password` | Request password reset | Email | Reset link sent (demo) |
| GET | `/api/auth/me` | Get current user info | JWT token (header) | User object |

**Request Headers:** `Authorization: Bearer <jwt_token>` (required for authenticated endpoints)

### Ingestion (`/api/ingestion/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ingestion/upload` | Upload and ingest single document |
| POST | `/api/ingestion/bulk-upload` | Batch upload multiple documents |
| GET | `/api/ingestion/status/{upload_id}` | Poll ingestion progress |
| GET | `/api/ingestion/history` | List all ingested documents for user |
| PUT | `/api/ingestion/documents/{id}` | Update document metadata |
| DELETE | `/api/ingestion/documents/{id}` | Delete document |

**Upload Request:** Multipart form data with fields: `file`, `source_type` (text/pdf/email/csv/json)

**Response:** 
```json
{
  "document_id": "doc_123",
  "filename": "supply_chain_report.pdf",
  "status": "processing",
  "entities_found": 24,
  "relations_found": 18,
  "duplicates_detected": 2
}
```

### Dashboard (`/api/dashboard/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/metrics` | Get KPI dashboard data |
| GET | `/api/dashboard/recent-activity` | List recent documents and queries |
| GET | `/api/dashboard/activity/documents/{id}` | Get document detail (edit modal) |
| GET | `/api/dashboard/activity/queries/{id}` | Get query execution detail |
| PATCH | `/api/dashboard/activity/documents/{id}` | Update document metadata |
| DELETE | `/api/dashboard/activity/documents/{id}` | Delete document from graph |
| PATCH | `/api/dashboard/activity/queries/{id}` | Update query note/tag |
| DELETE | `/api/dashboard/activity/queries/{id}` | Delete query from history |
| GET | `/api/dashboard/executive-summary` | AI-generated insights and headlines |
| GET | `/api/dashboard/health` | System health indicators |
| GET | `/api/dashboard/heatmap` | Risk heatmap data (areas and scores) |

**Dashboard Metrics Response:**
```json
{
  "document_count": 156,
  "entity_count": 2340,
  "relationship_count": 5678,
  "avg_connections": 2.43,
  "processing_rate_docs_per_hour": 12.5
}
```

### Graph (`/api/graph/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/graph/current` | Get current graph snapshot (nodes + edges) |
| GET | `/api/graph/versions` | List graph versions with timestamps |
| GET | `/api/graph/version/{version_id}` | Get specific graph version |
| GET | `/api/graph/nodes` | List all nodes with metadata |
| GET | `/api/graph/nodes/{id}` | Get single node detail |
| GET | `/api/graph/edges` | List all edges (relationships) |
| GET | `/api/graph/edges/{source}/{target}` | Get edge detail |
| GET | `/api/graph/export/json` | Export graph as JSON |
| GET | `/api/graph/export/csv` | Export graph as CSV (edge list) |
| GET | `/api/graph/export/png` | Export graph as PNG image |

**Graph Node Response:**
```json
{
  "id": "node_456",
  "label": "Supplier XYZ",
  "type": "Organization",
  "order": 3,
  "connected_edges": 12,
  "source_documents": ["doc_123", "doc_125"],
  "created_at": "2026-04-15T10:30:00Z"
}
```

### Query (`/api/query/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/query/execute` | Execute semantic query |
| GET | `/api/query/history` | Get user's query history |
| GET | `/api/query/history/{query_id}` | Get query result detail |
| DELETE | `/api/query/history/{query_id}` | Delete query from history |

**Query Execute Request:**
```json
{
  "question": "What are the top 5 supplier risks?",
  "filters": { "type": "Organization", "date_range": "last_30_days" }
}
```

**Query Result Response:**
```json
{
  "query_id": "q_789",
  "matched_entities": [
    { "name": "Supplier ABC", "type": "Organization", "score": 0.95, "source_doc": "doc_123" }
  ],
  "matched_relations": [
    { "source": "Supplier ABC", "edge": "depends-on", "target": "Factory XYZ" }
  ],
  "inference_summary": "3 suppliers show dependency risks...",
  "execution_time_ms": 245
}
```

### Reasoning (`/api/reasoning/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/reasoning/generate-insights` | Generate executive insights |
| POST | `/api/reasoning/analyze-pattern` | Analyze graph patterns (clustering, etc.) |
| POST | `/api/reasoning/predict-risk` | Predict risk events based on graph |

**Generate Insights Response:**
```json
{
  "headline": "Supplier Dependency Risk Detected",
  "insights": [
    "3 key suppliers are single points of failure",
    "Alternate sourcing paths exist but are underutilized"
  ],
  "recommended_actions": ["Review supplier contracts", "Activate contingency plans"]
}
```

### Admin (`/api/admin/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/users` | List all users (admin only) |
| POST | `/api/admin/users` | Create new user (admin only) |
| PUT | `/api/admin/users/{id}` | Update user (admin only) |
| DELETE | `/api/admin/users/{id}` | Delete user (admin only) |
| GET | `/api/admin/config` | Get system configuration |
| PUT | `/api/admin/config` | Update configuration (API keys, thresholds, etc.) |
| GET | `/api/admin/audit-log` | View activity audit trail |

---

## 💾 Database Schema

### User Model
```
users
├── id: Integer (PK)
├── email: String (unique, required)
├── password_hash: String (bcrypt)
├── name: String
├── role: String (admin|analyst|viewer)
├── status: String (active|inactive)
├── created_at: DateTime
├── updated_at: DateTime
└── last_login: DateTime
```

### Document Model
```
documents
├── id: Integer (PK)
├── user_id: Integer (FK → users.id)
├── filename: String
├── source_type: String (pdf|docx|email|csv|json|text)
├── content: Text (raw content)
├── content_hash: String (for duplicate detection)
├── file_size: Integer (bytes)
├── extracted_entities: Integer (count)
├── extracted_relations: Integer (count)
├── status: String (pending|processing|completed|failed)
├── is_duplicate: Boolean
├── parent_document_id: Integer (if duplicate)
├── created_at: DateTime
└── updated_at: DateTime
```

### Entity Model
```
entities
├── id: Integer (PK)
├── graph_id: Integer (FK → graph_versions.id)
├── label: String (entity name)
├── entity_type: String (Person|Organization|Location|Product|Concept)
├── node_type: String (Primary|Secondary|Tertiary)
├── order: Integer (for display ordering, 1-20 in tree view)
├── source_documents: List[Integer] (document IDs)
├── confidence: Float (0-1)
├── metadata: JSON
├── created_at: DateTime
└── updated_at: DateTime
```

### Relation Model
```
relations
├── id: Integer (PK)
├── graph_id: Integer (FK)
├── source_entity_id: Integer (FK → entities.id)
├── target_entity_id: Integer (FK → entities.id)
├── relation_type: String (depends-on|reports-to|contains|impacts|etc.)
├── confidence: Float (0-1)
├── source_document_id: Integer (FK → documents.id)
├── source_text: Text (exact text where relation was found)
├── created_at: DateTime
└── updated_at: DateTime
```

### QueryLog Model
```
query_logs
├── id: Integer (PK)
├── user_id: Integer (FK → users.id)
├── query_text: String (user's question)
├── result_count: Integer
├── execution_time_ms: Integer
├── matched_entities: JSON
├── matched_relations: JSON
├── created_at: DateTime
└── updated_at: DateTime
```

### GraphVersion Model
```
graph_versions
├── id: Integer (PK)
├── version_number: Integer (1, 2, 3, ...)
├── node_count: Integer
├── edge_count: Integer
├── created_at: DateTime
├── snapshot_data: JSON (full graph export)
└── change_summary: Text (what changed from previous)
```

---

## ⚙️ Configuration & Deployment

### Environment Variables (`.env`)

```bash
# Flask & Security
SECRET_KEY=your-random-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
FLASK_ENV=development  # or production
DEBUG=False

# Database
DATABASE_URL=sqlite:///instance/app.db
# For PostgreSQL production:
# DATABASE_URL=postgresql://user:password@localhost:5432/akg_db

# AI & NLP Services
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-pro

# Optional Neo4j
NEO4J_ENABLED=false
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=5000

# Logging
LOG_LEVEL=INFO

# Security
PASSWORD_MIN_LENGTH=8
SESSION_TIMEOUT_MINUTES=30
```

### Docker Compose (`docker-compose.yml`)

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=sqlite:///instance/app.db
    volumes:
      - ./instance:/app/instance
      - ./graph_data:/app/graph_data
    command: python run_dev.py

  # Optional: Neo4j for advanced graph queries
  neo4j:
    image: neo4j:latest
    ports:
      - "7687:7687"
      - "7474:7474"
    environment:
      - NEO4J_AUTH=neo4j/password
    volumes:
      - neo4j_data:/data
volumes:
  neo4j_data:
```

### Gunicorn Production Setup

```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers, logging
gunicorn -w 4 \
  -b 0.0.0.0:5000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --log-level info \
  backend.wsgi:app
```

### Nginx Reverse Proxy (Optional)

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### AWS Deployment (ECS)

1. Push Docker image to ECR
2. Create ECS task definition pointing to ECR image
3. Create ECS service with load balancer
4. Set environment variables in task definition
5. Use RDS PostgreSQL for persistent database

### Azure Deployment (ACI)

1. Push Docker image to Azure Container Registry
2. Create container instance with image from ACR
3. Set environment variables and port mappings
4. Use Azure Database for PostgreSQL

---

## 🧪 Testing & Quality

### Run Tests
```bash
# Run all tests with pytest
pytest backend/tests -v

# Run specific test file
pytest backend/tests/test_auth.py -v

# Run with coverage report
pytest backend/tests --cov=backend --cov-report=html
```

### Test Categories

1. **Authentication Tests** (`test_auth.py`)
   - Signup, login, logout flows
   - JWT token generation and validation
   - Password hashing and security

2. **Ingestion Tests** (`test_ingestion.py`)
   - Document upload (various formats)
   - Entity extraction accuracy
   - Duplicate detection
   - Error handling for unsupported formats

3. **Graph Tests** (`test_graph.py`)
   - Node and edge creation
   - Graph layout rendering
   - Version snapshots
   - Export functionality

4. **Query Tests** (`test_query.py`)
   - Semantic query matching
   - Result ranking
   - Source attribution

5. **Analytics Tests** (`test_analytics.py`)
   - Dashboard metrics calculation
   - Heatmap score generation
   - Health indicator gathering

### Linting & Code Style
```bash
# Install linters
pip install flake8 pylint black

# Check code style
flake8 backend --max-line-length=100

# Auto-format code
black backend --line-length=100
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

**Issue: "Port 5000 already in use"**
```bash
# Find process using port 5000 and kill it
lsof -i :5000  # on macOS/Linux
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess  # on Windows

# Or use different port
flask run --port=5001
```

**Issue: "ModuleNotFoundError: No module named 'flask'"**
```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue: "CORS error when calling API from frontend"**
- Ensure CORS is enabled in `backend/app.py`
- Check that API_URL in `frontend/assets/js/api_service.js` matches backend URL

**Issue: "Graph visualization not showing nodes"**
- Check browser console (F12) for JavaScript errors
- Verify Cytoscape.js is loaded (should see it in Network tab)
- Ensure graph data endpoint returns valid JSON with nodes and edges

**Issue: "Document ingestion fails with 'File too large'"**
- Check maximum upload size in Flask config (default 16MB)
- Modify in `backend/app.py`: `app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024`

**Issue: "AI insights are generic or empty"**
- Verify OpenAI/Gemini API keys are set in `.env`
- Check API key quota hasn't been exhausted
- Review error logs: `tail logs/error.log`
- Fallback to rule-based NLP by setting `OFFLINE_MODE=true`

**Issue: "Database locked" error on SQLite**
- SQLite has limited concurrency; switch to PostgreSQL for production
- In development, restart the app and ensure only one process is running

---

## 📚 Additional Resources

- **Full API Documentation:** See [docs/API_Documentation.md](docs/API_Documentation.md)
- **Architecture Diagram:** See [docs/Architecture_Diagram.md](docs/Architecture_Diagram.md)
- **User Manual:** See [docs/User_Manual.md](docs/User_Manual.md)
- **Admin Guide:** See [docs/Admin_Guide.md](docs/Admin_Guide.md)
- **Deployment Guide:** See [docs/Deployment_Guide.md](docs/Deployment_Guide.md)
- **Business Model:** See [docs/Business_Model.md](docs/Business_Model.md)

---

## 📝 License & Attribution

This is an original project built for enterprise knowledge graph construction and reasoning. All code, documentation, and UI designs are proprietary and created specifically for this platform. External dependencies are open-source libraries used under their respective licenses.

---

## 🤝 Support & Contact

For questions, issues, or feature requests:
- Review existing documentation in `/docs/` folder
- Check troubleshooting section above
- Review logs in `/logs/` directory for detailed error messages

**Last Updated:** April 30, 2026  
**Version:** 1.0.0
