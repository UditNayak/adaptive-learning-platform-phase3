import streamlit as st


def init_session():
    if "user" not in st.session_state:
        st.session_state["user"] = None

    if "selected_chat_id" not in st.session_state:
        st.session_state["selected_chat_id"] = None

    if "page" not in st.session_state:
        st.session_state["page"] = "chat"


def login_user(user_data: dict):
    st.session_state["user"] = user_data
    st.session_state["page"] = "chat"


def logout_user():
    st.session_state.clear()