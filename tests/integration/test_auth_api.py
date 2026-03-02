def test_signup_api(client):

    response = client.post("/auth/signup", json={
        "name": "User",
        "email": "user@test.com",
        "password": "pass"
    })

    assert response.status_code == 200
    assert response.json()["email"] == "user@test.com"