import streamlit as st


def render_quiz_block(quiz_data: dict):

    st.markdown("### Quiz")

    st.markdown(f"**Question:** {quiz_data['question']}")

    selected_option = st.radio(
        "Choose an option:",
        list(quiz_data["options"].keys()),
        format_func=lambda x: f"{x}. {quiz_data['options'][x]}"
    )

    return selected_option