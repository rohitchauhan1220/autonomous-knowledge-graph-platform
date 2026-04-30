import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(app):
    log_dir = Path(app.root_path).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    handler = RotatingFileHandler(log_dir / "platform.log", maxBytes=1_000_000, backupCount=5)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
