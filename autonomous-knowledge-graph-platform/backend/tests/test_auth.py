from backend.models.user_model import User


def test_password_hashing():
    user = User(name="A", email="a@example.com")
    user.set_password("Secret123")
    assert user.check_password("Secret123")
    assert not user.check_password("wrong")
