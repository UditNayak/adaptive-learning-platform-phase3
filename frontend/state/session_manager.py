import streamlit as st


def init_session():
    defaults = {
        "user": None,
        "selected_chat_id": None,
        "page": "chat",
        "loading": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def login_user(user_data: dict):
    st.session_state["user"] = user_data
    st.session_state["page"] = "chat"


def logout_user():
    st.session_state.clear()