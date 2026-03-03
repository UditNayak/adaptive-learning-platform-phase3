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