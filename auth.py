import sqlite3
import streamlit as st
def get_connection():
    return sqlite3.connect("data.db", check_same_thread=False)

def login_register():

    conn = get_connection()   # 🔥 हर बार नया connection
    cursor = conn.cursor()

    menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

    # LOGIN
    if menu == "Login":
        st.subheader("🔑 Login")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button("Login")

        if submitted:
            cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, password)
            )

            result = cursor.fetchone()

            if result:
                st.session_state.page = "dashboard"
                st.session_state.logged_in = True
                st.success("✅ Login Successful")
                st.rerun()
            else:
                st.error("❌ Wrong Username or Password")

    # REGISTER
    elif menu == "Register":
        st.subheader("📝 Register")

        with st.form("register_form"):
            new_user = st.text_input("Username")
            new_pass = st.text_input("Password", type="password")

            submitted = st.form_submit_button("Register")

        if submitted:
            try:
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (new_user, new_pass)
                )
                conn.commit()
                st.success("✅ Registered Successfully")
            except:
                st.error("❌ Username already exists")