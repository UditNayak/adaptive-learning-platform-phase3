import streamlit as st
from api.client import create_chat, get_conversation, get_chat_detail
from components.chat_bubble import render_chat_bubble
from components.explanation_block import render_explanation
from components.quiz_block import render_quiz_block


def render_chat_page():

    user = st.session_state.user
    user_id = user["id"]

    selected_chat_id = st.session_state.selected_chat_id

    # -------------------------
    # NEW CHAT FORM
    # -------------------------
    if not selected_chat_id:

        st.title("Start a New Chat")

        topic_name = st.text_input("Topic Name")
        topic_description = st.text_area("Description (Optional)")
        knowledge_level = st.selectbox(
            "Your Knowledge Level",
            ["BEGINNER", "INTERMEDIATE", "PRO"]
        )

        if st.button("Start Learning"):

            response = create_chat(
                user_id,
                topic_name,
                topic_description,
                knowledge_level
            )

            if response.status_code == 200:
                chat = response.json()
                st.session_state.selected_chat_id = chat["id"]
                st.rerun()
            else:
                st.error("Failed to create chat")

        return

    # -------------------------
    # LOAD SESSION DETAIL
    # -------------------------
    detail_response = get_chat_detail(selected_chat_id)

    if detail_response.status_code != 200:
        st.error("Failed to load chat details")
        return

    chat_detail = detail_response.json()

    # Header Section
    st.title(chat_detail.get("title") or chat_detail.get("topic_name"))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Topic:** {chat_detail.get('topic_name')}")

        if chat_detail.get("topic_description"):
            st.markdown(f"**Description:** {chat_detail.get('topic_description')}")

        st.markdown(
            f"**Initial Level:** {chat_detail.get('initial_knowledge_level')}"
        )

    with col2:
        st.markdown(
            f"**Current Level:** {chat_detail.get('current_level')}"
        )

    st.markdown("---")

    # -------------------------
    # LOAD CONVERSATION
    # -------------------------
    response = get_conversation(selected_chat_id, user_id)

    if response.status_code != 200:
        st.error("Failed to load conversation")
        return

    conversation = response.json()

    for item in conversation:

        if item["message_type"] == "EXPLANATION":
            render_explanation(item["content"], item.get("metadata_json"))

        elif item["message_type"] == "QUIZ":
            render_chat_bubble(item["role"], item["content"])

            if item.get("quiz_data"):
                render_quiz_block(item["quiz_data"])

        else:
            render_chat_bubble(item["role"], item["content"])