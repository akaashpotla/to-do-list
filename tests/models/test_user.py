
from app.models import User


class TestUser:
    def test_create_user(self, db_session):
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
