URL = "/api/v1/user"

NAME = "Akaash Potla"
EMAIL = "akaash@gmail.com"
PASSWORD = "1Password!"

class TestUserCreation:
    
    def test_create_user_success(self, client):
        payload = {
            "name" : NAME,
            "email" : EMAIL,
            "password" : PASSWORD
        }
        response = client.post(URL, json = payload)
        assert response.status_code == 201
        data = response.json()

        assert "id" in data
        assert data["name"] == payload["name"]
        assert data["email"] == payload["email"]
        assert "password" not in data

    def test_name_missing(self, client):
        payload = {
            "email" : EMAIL,
            "password" : PASSWORD
        }
        response = client.post(URL, json = payload)
        assert response.status_code == 422

    def test_name_empty_string(self, client):
        payload = {
            "name" : "",
            "email" : EMAIL,
            "password" : PASSWORD
        }
        response = client.post(URL, json = payload)
        assert response.status_code == 422

    def test_name_too_long(self, client):
        payload = {
            "name" : "a" * 256,
            "email" : EMAIL,
            "password" : PASSWORD
        }
        response = client.post(URL, json = payload)
        assert response.status_code == 422

    def test_email_missing(self, client):
        payload = {
            "name" : NAME,
            "password" : PASSWORD
        }
        response = client.post(URL, json = payload)
        assert response.status_code == 422

    def test_email_empty_string(self, client):
        payload = {
            "name" : NAME,
            "email" : "",
            "password" : PASSWORD
        }
        response = client.post(URL, json = payload)
        assert response.status_code == 422

    def test_email_non_email_string(self, client):
        payload = {
            "name" : NAME,
            "email" : "akaashpotla123",
            "password" : PASSWORD
        }
        response = client.post(URL, json = payload)
        assert response.status_code == 422

    def test_missing_password(self, client):
        payload = {
            "name" : NAME,
            "email" : EMAIL
        }
        response = client.post(URL, json = payload)
        assert response.status_code == 422

    def test_short_password(self, client):
        payload = {
            "name" : NAME,
            "email" : EMAIL,
            "password" : "Apple1!"
        }
        response = client.post(URL, json = payload)
        assert response.status_code == 422

    def test_long_password(self, client):
        payload = {
            "name" : NAME,
            "email" : EMAIL,
            "password" : "1Password!kvjnscknaoisdjcffwkenvwivejnkdsjncjksndkjcvbsidbvjkskdjnvkjsdv"
        }
        response = client.post(URL, json = payload)
        assert response.status_code == 422

    def test_password_without_uppercase(self, client):
        payload = {
            "name" : NAME,
            "email" : EMAIL,
            "password" : "1password!"
        }
        response = client.post(URL, json = payload)
        assert response.status_code == 422

    def test_password_without_special_character(self, client):
        payload = {
            "name" : NAME,
            "email" : EMAIL,
            "password" : "1Password"
        }
        response = client.post(URL, json = payload)
        assert response.status_code == 422

    def test_password_without_number(self, client):
        payload = {
            "name" : NAME,
            "email" : EMAIL,
            "password" : "Password!"
        }
        response = client.post(URL, json = payload)
        assert response.status_code == 422