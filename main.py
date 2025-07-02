import streamlit as st

from ui import auth_ui, vault_ui
from app import auth

st.set_page_config(page_title="Orangeliquid Vault", page_icon="assets/orange_alien.ico")


def main():
    st.title("Orangeliquid Vault")

    # Auth logic
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        if auth.load_master_password_hash() is None:
            auth_ui.set_master_password()
        else:
            auth_ui.login()
        return  # Stop here if not logged in
# end of auth logic

    if st.session_state.get("reset_form"):
        for key in ["form_service", "form_username", "form_password", "form_email", "form_notes"]:
            st.session_state.pop(key, None)
            print(f"Del called on key: {key}")
        st.session_state["reset_form"] = False

    if "show_create_form" not in st.session_state:
        st.session_state["show_create_form"] = False

    if "show_entries" not in st.session_state:
        st.session_state["show_entries"] = False

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

    if st.session_state["show_create_form"]:
        vault_ui.create_new_entry_form()
    elif st.session_state["show_entries"]:
        vault_ui.view_entries()


# Todo - Fix left col entries(make service above username), make entries searchable
# Todo - integrate password generation for user


if __name__ == '__main__':
    main()
