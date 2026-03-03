import streamlit as st
from api.client import send_feedback


def render_feedback_buttons(message_id):

    with st.expander("Give Feedback"):

        feedback_type = st.radio(
            "Was this response helpful?",
            ["Helpful", "Not Helpful"],
            key=f"feedback_type_{message_id}"
        )

        feedback_text = st.text_area(
            "Additional Comments (Optional)",
            key=f"feedback_text_{message_id}"
        )

        if st.button("Submit Feedback", key=f"submit_feedback_{message_id}"):

            is_helpful = True if feedback_type == "Helpful" else False

            response = send_feedback(
                message_id,
                is_helpful,
                feedback_text
            )

            if response.status_code == 200:
                st.success("Feedback submitted successfully")
            else:
                st.error("Failed to submit feedback")