import requests

BACKEND_URL = "http://backend:8000"


def signup(name: str, email: str, password: str):
    return requests.post(
        f"{BACKEND_URL}/auth/signup",
        json={
            "name": name,
            "email": email,
            "password": password
        }
    )


def login(email: str, password: str):
    return requests.post(
        f"{BACKEND_URL}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )


def get_user_chats(user_id: str):
    return requests.get(
        f"{BACKEND_URL}/chat/user/{user_id}"
    )


def get_chat_detail(chat_session_id: str):
    return requests.get(
        f"{BACKEND_URL}/chat/{chat_session_id}"
    )


def create_chat(user_id, topic_name, topic_description, knowledge_level):
    return requests.post(
        f"{BACKEND_URL}/chat/create",
        json={
            "user_id": user_id,
            "topic_name": topic_name,
            "topic_description": topic_description,
            "knowledge_level": knowledge_level
        }
    )


def get_conversation(chat_session_id, user_id):
    return requests.get(
        f"{BACKEND_URL}/chat/{chat_session_id}/conversation/{user_id}"
    )


def parse_error(response):
    try:
        data = response.json()

        if isinstance(data, dict) and "detail" in data:
            detail = data["detail"]

            if isinstance(detail, list):
                return detail[0].get("msg", "Invalid input")

            if isinstance(detail, str):
                return detail

        return "Something went wrong"

    except Exception:
        return "Unexpected error"