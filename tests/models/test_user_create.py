URL = "/api/v1/user"

def test_create_user_success(client):
    payload = {
        "name" : "Akaash Potla",
        "email" : "akaash@gmail.com",
        "password" : "1Password!"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "password" not in data

def test_name_missing(client):
    payload = {
        "email" : "akaash@gmail.com",
        "password" : "1Password!"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 422

def test_name_empty_string(client):
    payload = {
        "name" : "",
        "email" : "akaash@gmail.com",
        "password" : "1Password!"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 422

def test_name_too_long(client):
    payload = {
        "name" : "a" * 256,
        "email" : "akaash@gmail.com",
        "password" : "1Password!"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 422

def test_email_missing(client):
    payload = {
        "name" : "Akaash Potla",
        "password" : "1Password!"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 422

def test_email_empty_string(client):
    payload = {
        "name" : "Akaash Potla",
        "email" : "",
        "password" : "1Password!"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 422

def test_email_non_email_string(client):
    payload = {
        "name" : "Akaash Potla",
        "email" : "akaashpotla123",
        "password" : "1Password!"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 422

def test_missing_password(client):
    payload = {
        "name" : "Akaash Potla",
        "email" : "akaash@gmail.com"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 422

def test_short_password(client):
    payload = {
        "name" : "Akaash Potla",
        "email" : "akaash@gmail.com",
        "password" : "Apple1!"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 422

def test_long_password(client):
    payload = {
        "name" : "Akaash Potla",
        "email" : "akaash@gmail.com",
        "password" : "1Password!kvjnscknaoisdjcffwkenvwivejnkdsjncjksndkjcvbsidbvjkskdjnvkjsdv"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 422

def test_password_without_uppercase(client):
    payload = {
        "name" : "Akaash Potla",
        "email" : "akaash@gmail.com",
        "password" : "1password!"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 422

def test_password_without_special_character(client):
    payload = {
        "name" : "Akaash Potla",
        "email" : "akaash@gmail.com",
        "password" : "1Password"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 422

def test_password_without_number(client):
    payload = {
        "name" : "Akaash Potla",
        "email" : "akaash@gmail.com",
        "password" : "Password!"
        }
    response = client.post(URL, json = payload)
    assert response.status_code == 422