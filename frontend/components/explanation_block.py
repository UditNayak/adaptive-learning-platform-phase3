import streamlit as st


def render_explanation(content: str, metadata_json: dict | None):

    with st.chat_message("assistant"):
        st.markdown(content)

        if metadata_json and "references" in metadata_json:
            st.markdown("#### References")

            for ref in metadata_json["references"]:
                st.markdown(f"- [{ref['title']}]({ref['url']})")