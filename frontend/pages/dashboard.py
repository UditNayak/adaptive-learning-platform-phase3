import streamlit as st
from components.sidebar import render_sidebar


def render_dashboard():

    render_sidebar()

    if st.session_state.page == "analytics":
        st.title("Analytics Page (Coming in F4)")
        return

    selected_chat_id = st.session_state.selected_chat_id

    if selected_chat_id:
        st.title("Chat View (Rendering in F3)")
        st.write(f"Selected Chat ID: {selected_chat_id}")
    else:
        st.title("Start a New Chat")
        st.info("New chat form will be implemented in F3.")