import streamlit as st
from api.client import get_user_chats
from state.session_manager import logout_user


def render_sidebar():

    st.sidebar.title("Adaptive Learning")

    user = st.session_state.user
    user_id = user["id"]

    if st.sidebar.button("New Chat"):
        st.session_state.selected_chat_id = None
        st.session_state.page = "chat"

    st.sidebar.markdown("### Your Chats")

    response = get_user_chats(user_id)

    if response.status_code == 200:
        chats = response.json()

        for chat in chats:
            chat_title = chat.get("title") or chat.get("topic_name")

            if st.sidebar.button(
                chat_title,
                key=f"chat_{chat['id']}"
            ):
                st.session_state.selected_chat_id = chat["id"]
                st.session_state.page = "chat"

    else:
        st.sidebar.error("Failed to load chats")

    st.sidebar.markdown("---")

    if st.sidebar.button("Analytics"):
        st.session_state.page = "analytics"

    if st.sidebar.button("Logout"):
        logout_user()
        st.rerun()