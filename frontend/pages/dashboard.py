import streamlit as st
from components.sidebar import render_sidebar
from pages.chat import render_chat_page
from pages.analytics import render_analytics_page


def render_dashboard():

    render_sidebar()

    if st.session_state.page == "analytics":
        render_analytics_page()
        return

    render_chat_page()