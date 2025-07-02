import streamlit as st
from cryptography.fernet import Fernet
import time

from app.models.schemas import VaultEntryCreate
from app.crud_vault import create_entry, get_all_entries
from app.encryption import encrypt_field, decrypt_entry


def create_new_entry_form():
    st.subheader("Add a New Vault Entry")

    form_suffix = st.session_state.get("form_suffix", "")
    with st.form(f"create_entry_{form_suffix}"):
        service = st.text_input("Service", placeholder="Youtube", key="form_service")
        username = st.text_input("Username", placeholder="Myusername123", key="form_username")
        password = st.text_input("Password", type="password", key="form_password")
        email = st.text_input("Email (optional)", placeholder="johndoe123@provider.com", key="form_email")
        notes = st.text_input("Notes (optional)", placeholder="Very detailed notes on my account", key="form_notes")

        col1, spacer, col2 = st.columns([1, 6, 1])

        with col1:
            save_entry = st.form_submit_button("Save")
        with col2:
            cancel = st.form_submit_button("Cancel")

        if cancel:
            st.session_state["show_create_form"] = False
            st.rerun()

        if save_entry:
            if not service or not username or not password:
                st.error("Service, username, and password are required.")
                return

            try:
                key = st.session_state.get("key")
                if key is None:
                    st.error("Encryption key not found. Please log in again.")
                    return

                fernet = Fernet(key)

                # We decode at the end to change the encrypted bytes into a string for storage
                encrypted_service = encrypt_field(service, fernet)
                encrypted_username = encrypt_field(username, fernet)
                encrypted_password = encrypt_field(password, fernet)
                encrypted_email = encrypt_field(email, fernet) if email else None
                encrypted_notes = encrypt_field(notes, fernet) if notes else None

                entry_data = VaultEntryCreate(
                    service=encrypted_service,
                    username=encrypted_username,
                    password_encrypted=encrypted_password,
                    email=encrypted_email,
                    notes=encrypted_notes,
                )

                create_entry(entry_data)
                st.success("Entry saved successfully!")
                time.sleep(1.5)
                st.session_state["form_suffix"] = str(time.time())
                st.session_state["reset_form"] = True
                st.rerun()

            except Exception as e:
                st.error(f"Error saving entry: {e}")


def view_entries():
    key = st.session_state.get("key")
    if not key:
        st.error("Encryption key is missing. Please log in again.")
        return

    fernet = Fernet(key)
    entries = get_all_entries()

    if not entries:
        st.info("No entries yet.")
        return

        # Initialize selection
    if "selected_entry_index" not in st.session_state:
        st.session_state.selected_entry_index = 0

    # Layout with two columns
    col1, col2 = st.columns([2, 5], gap="large")

    # --- LEFT COLUMN: Entry titles ---
    with col1:
        st.write("### Entries")
        for i, entry in enumerate(entries):
            decrypted = decrypt_entry(entry, fernet)
            label = (
                f"{decrypted['service']}"
                f"{decrypted['username']}"
            )
            if st.button(label, key=f"entry_button_{i}"):
                st.session_state.selected_entry_index = i

    # --- RIGHT COLUMN: Entry details ---
    with col2:
        selected_index = st.session_state.selected_entry_index
        selected_entry = decrypt_entry(entries[selected_index], fernet)

        st.write(f"### {selected_entry['service']}")
        st.markdown(f"**Username:** {selected_entry['username']}")

        # Password field with toggle
        pw_col1, pw_col2 = st.columns([6, 1])
        with pw_col2:
            show_password = st.checkbox("👁", key=f"show_password_{selected_index}")
        with pw_col1:
            display_pw = selected_entry["password"] if show_password else "●●●●●●●●"
            st.code(display_pw, language="text")

        if selected_entry["email"]:
            st.markdown(f"**Email:** {selected_entry['email']}")
        if selected_entry["notes"]:
            st.markdown(f"**Notes:** {selected_entry['notes']}")
        st.markdown(f"**Created At:** {selected_entry['created_at']}")
