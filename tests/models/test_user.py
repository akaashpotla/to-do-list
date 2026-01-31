import pytest
from sqlalchemy.exc import IntegrityError
from app.models import User


class TestUser:
    def test_create_user_success(self, db_session):
        user = User(
        name="Akaash Potla",
        email="akaash@gmail.com",
        password="password"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        assert user.name == "Akaash Potla"
        assert user.email == "akaash@gmail.com"
        assert user.password == "password"
        assert user.id is not None
    def test_user_name_error(self, db_session):
        user = User(
        email="akaash@gmail.com",
        password="password"
        )
        db_session.add(user)
        with pytest.raises(IntegrityError):
            db_session.commit()
    def test_user_email_error(self, db_session):
        user = User(
        name="Akaash Potla",
        password="password"
        )
        db_session.add(user)
        with pytest.raises(IntegrityError):
            db_session.commit()
    def test_user_password_error(self, db_session):
        user = User(
        name="Akaash Potla",
        email="akaash@gmail.com",
    )
        db_session.add(user)
        with pytest.raises(IntegrityError):
            db_session.commit()
