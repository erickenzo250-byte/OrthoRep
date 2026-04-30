import streamlit as st

# Simple login (upgrade later to DB auth)
USERS = {
    "admin": "admin123",
    "erick": "1234"
}

def login():
    st.sidebar.subheader("Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state["user"] = username
            st.success("Logged in")
        else:
            st.error("Invalid credentials")

def require_login():
    if "user" not in st.session_state:
        login()
        st.stop()
