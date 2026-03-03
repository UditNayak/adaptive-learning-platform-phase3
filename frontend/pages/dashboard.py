import streamlit as st
from components.sidebar import render_sidebar
from pages.chat import render_chat_page


def render_dashboard():

    render_sidebar()

    if st.session_state.page == "analytics":
        st.title("Analytics Page (Coming in F4)")
        return

    render_chat_page()