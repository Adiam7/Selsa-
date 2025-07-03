import pytest
from accounts.models import User
from accounts.services import register_user

@pytest.mark.django_db
def test_register_user():
    data = {"email": "test@example.com", "username": "testuser", "password": "strongpass123"}
    user = register_user(data)
    assert user.email == "test@example.com"
    assert user.check_password("strongpass123")