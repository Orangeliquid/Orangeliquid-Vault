import streamlit as st

from ui import auth_ui, vault_ui
from app import auth

st.set_page_config(page_title="Orangeliquid Vault", page_icon="assets/orange_alien.ico")


def main():
    st.markdown(
        "<h1 style='color:#FFA500; text-align: center; '>ORANGELIQUID VAULT</h1>",
        unsafe_allow_html=True
    )

# ----------------------- Auth logic --------------------------------------------------------
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        if auth.load_master_password_hash() is None:
            auth_ui.set_master_password()
        else:
            auth_ui.login()
        return  # Stop here if not logged in

# --------------------- Session State Management ------------------------------------
    if st.session_state.get("reset_form"):
        for key in [
            "form_service",
            "form_username",
            "form_password",
            "form_email",
            "form_notes",
            "generate_random_password",
            "password_input",
        ]:
            st.session_state.pop(key, None)
            print(f"Del called on key: {key}")
        st.session_state["reset_form"] = False

    if "show_create_form" not in st.session_state:
        st.session_state["show_create_form"] = False

    if "show_entries" not in st.session_state:
        st.session_state["show_entries"] = False

# ------------------Column and Button Create -------------------------------------------------------------------
    create_col, view_col, logout_col = st.columns([3, 3, 1])

    with create_col:
        if st.button("Create New Entry"):
            st.session_state["show_create_form"] = True
            st.session_state["show_entries"] = False
            st.rerun()

    with view_col:
        if st.button("View All Entries"):
            st.session_state["show_create_form"] = False
            st.session_state["show_entries"] = True
            st.rerun()

    with logout_col:
        if st.button("Log out"):
            st.session_state.clear()
            st.rerun()

# ------------------ Function Calling Logic Based On States ---------------------------------------
    if st.session_state["show_create_form"]:
        vault_ui.create_new_entry_form()
    elif st.session_state["show_entries"]:
        vault_ui.view_entries()


if __name__ == '__main__':
    # To start:
    # cd Orangeliquid-Vault
    # - run -> uv run streamlit run main.py
    # - set master password
    # - .secret_key file is created
    # - vault.db is created via init
    # - once signed in .vault_salt is created
    # - program is ready of use
    #
    # To start fresh:
    # - delete .secret_key file
    # - delete .vault_salt
    # - delete vault.db
    # cd Orangeliquid-Vault
    # - run -> uv run streamlit run main.py
    main()
