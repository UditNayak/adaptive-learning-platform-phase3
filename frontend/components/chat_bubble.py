import streamlit as st


def render_chat_bubble(role: str, content: str):

    if role == "USER":
        with st.chat_message("user"):
            st.markdown(content)
    else:
        with st.chat_message("assistant"):
            st.markdown(content)