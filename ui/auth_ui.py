import streamlit as st

from app import auth


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
        st.success("Master password set! Please reload and log in.")
        return True

    return False


def login() -> bool:
    st.header("Login")

    password = st.text_input("Enter master password", type="password")

    if st.button("Login"):
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
            return True
        else:
            st.error("Incorrect password.")
            return False

    return False
