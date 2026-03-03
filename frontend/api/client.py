import requests

BACKEND_URL = "http://backend:8000"


def signup(name: str, email: str, password: str):
    response = requests.post(
        f"{BACKEND_URL}/auth/signup",
        json={
            "name": name,
            "email": email,
            "password": password
        }
    )
    return response


def login(email: str, password: str):
    response = requests.post(
        f"{BACKEND_URL}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    return response

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