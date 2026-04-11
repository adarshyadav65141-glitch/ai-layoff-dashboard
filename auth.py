from dotenv import load_dotenv
import os
import streamlit as st
import sqlite3

# 🔥 DB connection
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

def login_register():

    menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

    # 🔐 LOGIN
    if menu == "Login":

        with st.form("login_form"):
            st.subheader("🔑 Login")

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            submit = st.form_submit_button("Login")

        if submit:
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, password)
            )

            result = cursor.fetchone()

            if result:
                st.session_state.page = "dashboard"
                st.success("✅ Login Successful")
                st.rerun()
            else:
                st.error("❌ Wrong Username or Password")
        else:
            st.stop()

    # 📝 REGISTER
    elif menu == "Register":

        with st.form("register_form"):
            st.subheader("📝 Register")

            new_user = st.text_input("Username")
            new_pass = st.text_input("Password", type="password")

            submit_reg = st.form_submit_button("Register")

        if submit_reg:
            try:
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (new_user, new_pass)
                )
                conn.commit()
                st.success("✅ Registered Successfully")
            except:
                st.error("❌ Username already exists")
        else:
            st.stop()
            load_dotenv()