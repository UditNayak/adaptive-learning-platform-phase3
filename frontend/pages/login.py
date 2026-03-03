import streamlit as st
from api.client import signup, login, parse_error
from state.session_manager import login_user


def render_login_page():

    st.title("Adaptive Learning Platform")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Login")

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            response = login(email, password)

            if response.status_code == 200:
                login_user(response.json())
                st.rerun()
            else:
                st.error(parse_error(response))

    with tab2:
        st.subheader("Create Account")

        name = st.text_input("Name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Sign Up"):
            response = signup(name, email, password)

            if response.status_code == 200:
                st.success("Account created successfully. Please login.")
            else:
                st.error(parse_error(response))