import streamlit as st
import time

from app import auth
from app.database import init_db


def set_master_password() -> bool:
    st.header("Set a Master Password")

    pw1 = st.text_input("Enter new master password", type="password")
    pw2 = st.text_input("Confirm master password", type="password")

    if st.button("Save Password"):
        if not pw1 or not pw2:
            st.error("Please enter and confirm master password.")
            return False

        if pw1 != pw2:
            st.error("Passwords do not match.")
            return False

        hashed = auth.hash_password(pw1)
        auth.save_master_password_hash(hashed)

        init_db()

        st.success("Master password set!")
        time.sleep(2)  # allow user to see that the password was set correctly

        st.rerun()

    return False


def login() -> bool:
    st.header("Login")

    with st.form("login", enter_to_submit=True):
        password = st.text_input(label="Enter Master Password", placeholder="Master Password", type="password")

        if st.form_submit_button("Save"):
            stored_hash = auth.load_master_password_hash()

            if stored_hash is None:
                st.error("No master password found. Please set one first.")
                return False

            if auth.verify_password(password, stored_hash):
                salt = auth.get_or_create_salt()
                key = auth.derive_key(password, salt)
                st.session_state["key"] = key
                st.session_state["authenticated"] = True
                st.success("Login Successful!")

                time.sleep(1)  # allow user some time to see they logged in successfully before reloading page

                st.rerun()
            else:
                st.error("Incorrect password.")
                return False

    return False
