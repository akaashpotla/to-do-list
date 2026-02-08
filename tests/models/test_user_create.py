URL = "/api/v1/user"

def test_create_user_success(client):
    payload = {
        "user" : "Akaash Potla",
        "email" : "akaash@gmail.com",
        "password" : "1Password!"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["user"] == payload["Akaash Potla"]
    assert data["email"] == payload["akaash@gmail.com"]
