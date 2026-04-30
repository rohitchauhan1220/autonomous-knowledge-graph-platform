from config.database import db


def healthcheck():
    db.session.execute(db.text("SELECT 1"))
    return True
