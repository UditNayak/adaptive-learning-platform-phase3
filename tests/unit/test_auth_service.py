from app.services.auth_service import AuthService


def test_signup_success(db):
    service = AuthService(db)

    user = service.signup(
        name="Test",
        email="test@example.com",
        password="password"
    )

    assert user.email == "test@example.com"


def test_signup_duplicate(db):
    service = AuthService(db)

    service.signup("Test", "dup@example.com", "pass")

    try:
        service.signup("Test", "dup@example.com", "pass")
        assert False
    except ValueError:
        assert True