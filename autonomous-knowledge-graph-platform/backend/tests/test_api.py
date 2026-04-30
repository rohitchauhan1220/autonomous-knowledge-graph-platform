from backend.app import create_app
from config.database import db


def test_metrics_endpoint_requires_auth():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    client = app.test_client()
    response = client.get("/api/dashboard/metrics")
    assert response.status_code == 401


def test_signup_login_flow():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.drop_all()
        db.create_all()
    client = app.test_client()
    signup = client.post("/api/auth/signup", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "Password@123"
    })
    assert signup.status_code == 201
    login = client.post("/api/auth/login", json={"email": "test@example.com", "password": "Password@123"})
    assert login.status_code == 200
    assert "access_token" in login.get_json()


def test_signup_rejects_weak_password():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.drop_all()
        db.create_all()
    client = app.test_client()
    signup = client.post("/api/auth/signup", json={
        "name": "Weak User",
        "email": "weak@example.com",
        "password": "password"
    })
    assert signup.status_code == 400
    assert "Password must include" in signup.get_json()["error"]
