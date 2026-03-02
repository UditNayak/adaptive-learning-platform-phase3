def test_create_chat_api(client):

    # Create user first
    response = client.post("/auth/signup", json={
        "name": "User",
        "email": "chat@test.com",
        "password": "pass"
    })

    assert response.status_code == 200

    user = response.json()

    # IMPORTANT:
    # user["id"] returned from API is already correct UUID string.
    # FastAPI + Pydantic will convert it correctly for DB.

    response = client.post("/chat/create", json={
        "user_id": user["id"],
        "topic_name": "Binary Search",
        "topic_description": "Basic understanding",
        "knowledge_level": "BEGINNER"
    })

    assert response.status_code == 200