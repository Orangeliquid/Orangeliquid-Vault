import streamlit as st

from ui import auth_ui
from app import auth

st.set_page_config(page_title="Orangeliquid Vault")

st.title("Orangeliquid Vault")


def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        if auth.load_master_password_hash() is None:
            auth_ui.set_master_password()
        else:
            auth_ui.login()

    else:
        st.success("Welcome back!")
        st.write("You are now logged in and can access your vault.")

        if st.button("Log out"):
            st.session_state.clear()
            st.rerun()


if __name__ == '__main__':
    main()
