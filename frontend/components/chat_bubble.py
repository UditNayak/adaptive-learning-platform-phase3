import streamlit as st
from components.feedback_block import render_feedback_buttons


def render_chat_bubble(message_id, role: str, content: str):

    if role == "USER":
        st.markdown(
            f"""
            <div style='display:flex; justify-content:flex-end;'>
                <div style='
                    background-color:#2563eb;
                    color:white;
                    padding:10px 15px;
                    border-radius:15px;
                    max-width:70%;
                    margin:5px 0;
                '>
                    {content}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        with st.chat_message("assistant"):
            st.markdown(content)
            render_feedback_buttons(message_id)