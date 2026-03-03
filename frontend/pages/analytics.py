import streamlit as st
from api.client import get_user_analytics


def render_analytics_page():

    user = st.session_state.user
    user_id = user["id"]

    st.title("Learning Analytics")

    response = get_user_analytics(user_id)

    if response.status_code != 200:
        st.error("Failed to load analytics")
        return

    data = response.json()

    # -----------------------------
    # Summary Section
    # -----------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Topics", data["total_topics"])

    with col2:
        st.metric("Total Points", data["total_points"])

    with col3:
        st.metric("Quizzes Attempted", data["total_quizzes_attempted"])

    with col4:
        st.metric("Overall Accuracy", f"{data['overall_accuracy_percentage']}%")

    st.markdown("---")

    # -----------------------------
    # Topic-wise Section
    # -----------------------------
    st.subheader("Topic Performance")

    if not data["topics"]:
        st.info("No quiz activity yet. Start learning!")
        return

    for topic in data["topics"]:

        with st.container():

            st.markdown(f"### {topic['topic_name']}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"**Current Level:** {topic['current_level']}")

            with col2:
                st.markdown(f"**Points:** {topic['total_points']}")

            with col3:
                st.markdown(
                    f"**Accuracy:** {topic['accuracy_percentage']}%"
                )

            st.progress(topic["accuracy_percentage"] / 100)

            st.markdown(
                f"Quizzes Attempted: {topic['quizzes_attempted']} | "
                f"Correct: {topic['quizzes_correct']}"
            )

            st.markdown("---")