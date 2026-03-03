import streamlit as st
from api.client import submit_quiz


def render_quiz_block(quiz_data: dict, user_id: str):

    quiz_id = quiz_data["quiz_id"]

    st.markdown("---")
    st.markdown("### Quiz")

    st.markdown(f"**Difficulty:** {quiz_data['difficulty']}")
    st.markdown(f"**Points:** {quiz_data['points']}")
    st.markdown(f"**Question:** {quiz_data['question']}")

    hint_key = f"show_hint_{quiz_id}"

    if hint_key not in st.session_state:
        st.session_state[hint_key] = False

    selected_option = st.radio(
        "Choose an option:",
        list(quiz_data["options"].keys()),
        format_func=lambda x: f"{x}. {quiz_data['options'][x]}",
        key=f"quiz_option_{quiz_id}"
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
        if st.button("Show Hint", key=f"hint_btn_{quiz_id}"):
            st.session_state[hint_key] = True

    with col2:
        if st.button("Submit Answer", key=f"submit_{quiz_id}"):

            with st.spinner("Submitting answer..."):
                response = submit_quiz(
                    quiz_id,
                    user_id,
                    selected_option
                )

            if response.status_code == 200:
                st.success("Answer submitted")
                st.rerun()
            else:
                st.error("Failed to submit answer")

    if st.session_state[hint_key]:
        st.info(quiz_data["hint"])