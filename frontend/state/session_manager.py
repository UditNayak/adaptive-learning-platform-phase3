import streamlit as st


def init_session():
    if "user" not in st.session_state:
        st.session_state["user"] = None


def login_user(user_data: dict):
    st.session_state["user"] = user_data


def logout_user():
    st.session_state["user"] = None