import streamlit as st
from state.session_manager import logout_user


def render_dashboard():

    st.title("Dashboard")

    user = st.session_state.user

    st.write(f"Welcome, {user['name']}")

    if st.button("Logout"):
        logout_user()
        st.rerun()

    st.info("Chat and analytics UI will be implemented in next phase.")