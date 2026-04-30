from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.database import db
from config.logging_config import configure_logging
from config.settings import Config
from backend.middleware.error_handler import register_error_handlers
from backend.middleware.rate_limiter import limiter
from backend.middleware.request_logger import register_request_logger
from backend.routes.auth_routes import auth_bp
from backend.routes.ingestion_routes import ingestion_bp
from backend.routes.graph_routes import graph_bp
from backend.routes.query_routes import query_bp
from backend.routes.dashboard_routes import dashboard_bp
from backend.routes.admin_routes import admin_bp


def create_app(test_config=None):
    """Create and configure the Flask application.

    The app factory keeps the project test-friendly and production-ready:
    tests can inject an in-memory database, while deployment can load secrets
    and database URLs from environment variables.
    """
    app = Flask(
        __name__,
        static_folder=str(ROOT / "frontend"),
        static_url_path="",
    )
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(exist_ok=True)

    # Core platform extensions: CORS for frontend access, SQLAlchemy for data,
    # JWT for sessions, and Flask-Limiter for API protection.
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"], expose_headers=["Content-Type", "Authorization"])
    db.init_app(app)
    JWTManager(app)
    limiter.init_app(app)
    configure_logging(app)
    register_error_handlers(app)
    register_request_logger(app)

    # Routes are grouped by enterprise product area for clean maintenance.
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(ingestion_bp, url_prefix="/api/ingestion")
    app.register_blueprint(graph_bp, url_prefix="/api/graph")
    app.register_blueprint(query_bp, url_prefix="/api/query")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    with app.app_context():
        from backend.models import user_model, document_model, entity_model, relation_model, query_model, analytics_model, enterprise_model
        db.create_all()

    @app.get("/")
    def home():
        return send_from_directory(app.static_folder, "index.html")

    @app.get("/<path:path>")
    def static_pages(path):
        return send_from_directory(app.static_folder, path)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
