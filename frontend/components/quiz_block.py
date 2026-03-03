import streamlit as st
from api.client import submit_quiz


def render_quiz_block(quiz_data: dict, user_id: str):

    st.markdown("---")
    st.markdown("### Quiz")

    st.markdown(f"**Difficulty:** {quiz_data['difficulty']}")
    st.markdown(f"**Points:** {quiz_data['points']}")

    st.markdown(f"**Question:** {quiz_data['question']}")

    selected_option = st.radio(
        "Choose an option:",
        list(quiz_data["options"].keys()),
        format_func=lambda x: f"{x}. {quiz_data['options'][x]}",
        key=f"quiz_option_{quiz_data['question']}"
    )

    # Already answered
    if quiz_data.get("selected_option"):
        st.markdown(f"**Your Answer:** {quiz_data['selected_option']}")
        st.markdown(
            f"**Result:** {'Correct' if quiz_data['is_correct'] else 'Incorrect'}"
        )
        st.markdown(f"**Explanation:** {quiz_data['explanation']}")
        return

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Show Hint", key=f"hint_{quiz_data['question']}"):
            st.info(quiz_data["hint"])

    with col2:
        if st.button("Submit Answer", key=f"submit_{quiz_data['question']}"):
            response = submit_quiz(
                quiz_data["quiz_id"],
                user_id,
                selected_option
            )
            if response.status_code == 200:
                st.success("Answer submitted")
                st.rerun()
            else:
                st.error("Failed to submit answer")