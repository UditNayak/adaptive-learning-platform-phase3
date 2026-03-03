import streamlit as st
from state.session_manager import init_session
from pages.login import render_login_page
from pages.dashboard import render_dashboard

st.set_page_config(
    page_title="Adaptive Learning",
    layout="wide"
)

init_session()

if st.session_state.get("user"):
    render_dashboard()
else:
    render_login_page()