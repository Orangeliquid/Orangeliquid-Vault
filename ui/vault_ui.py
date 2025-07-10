import streamlit as st
from cryptography.fernet import Fernet
import time
from collections import defaultdict

from app.models.schemas import VaultEntryCreate
from app.crud_vault import create_entry, get_all_entries
from app.encryption import encrypt_field, decrypt_entry
from app.utils.generator import generate_password
from app.models.password_options import PasswordOptions
from app.utils.entry_helpers import get_flattened_entries, render_entry_button
from app.utils.strength import evaluate_strength, STRENGTH_LABELS


def create_new_entry_form():
    st.subheader("Add a New Vault Entry")

    if "form_password" not in st.session_state:
        st.session_state["form_password"] = ""

    def generate_password_callback():
        opts = PasswordOptions(
            length=st.session_state.get("gen_length", 16),
            include_numbers=st.session_state.get("gen_digits", True),
            include_symbols=st.session_state.get("gen_symbols", True),
        )
        generated_pw = generate_password(opts)
        st.session_state["form_password"] = generated_pw
        st.success("Password generated and filled!")
        st.rerun()

    form_suffix = st.session_state.get("form_suffix", "")

    with st.form(f"create_entry_{form_suffix}"):
        service = st.text_input(label="Service", placeholder="Youtube", key="form_service")
        username = st.text_input(label="Username", placeholder="Myusername123", key="form_username")
        email = st.text_input(label="Email (optional)", placeholder="johndoe123@provider.com", key="form_email")

        notes = st.text_input(
            label="Notes (optional)",
            placeholder="Very detailed notes on my account",
            key="form_notes"
        )

        password = st.text_input(
            label="Password",
            type="password",
            value=st.session_state["form_password"],
            key="password_input",
        )

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

                password_strength_val = evaluate_strength(password=password)

                fernet = Fernet(key)

                encrypted_service = encrypt_field(service.strip().lower(), fernet)
                encrypted_username = encrypt_field(username, fernet)
                encrypted_password = encrypt_field(password, fernet)
                encrypted_email = encrypt_field(email, fernet) if email else None
                encrypted_notes = encrypt_field(notes, fernet) if notes else None
                encrypted_strength_rating = encrypt_field(str(password_strength_val), fernet)

                entry_data = VaultEntryCreate(
                    service=encrypted_service,
                    username=encrypted_username,
                    password_encrypted=encrypted_password,
                    email=encrypted_email,
                    notes=encrypted_notes,
                    strength_rating=encrypted_strength_rating
                )

                create_entry(entry_data)
                st.success("Entry saved successfully!")
                time.sleep(1.5)
                st.session_state["form_suffix"] = str(time.time())
                st.session_state["reset_form"] = True
                st.rerun()

            except Exception as e:
                st.error(f"Error saving entry: {e}")

    # Outside the form, so reactive outside form submit cycle
    if st.checkbox("Generate Random Password", key="generate_random_password"):
        st.slider(label="Length", min_value=8, max_value=32, value=16, key="gen_length")
        st.checkbox(label="Include Digits", value=True, key="gen_digits")
        st.checkbox(label="Include Symbols", value=True, key="gen_symbols")
        if st.button("Generate Password"):
            generate_password_callback()
            st.rerun()


def view_entries():
    st.session_state["reset_form"] = True
    st.write("")

    key = st.session_state.get("key")
    if not key:
        st.error("Encryption key is missing. Please log in again.")
        return

    fernet = Fernet(key)
    entries = get_all_entries()

    if not entries:
        st.info("No entries yet.")
        return

    if "selected_entry_index" not in st.session_state:
        st.session_state.selected_entry_index = 0

    if "results_found_count" not in st.session_state:
        st.session_state.results_found_count = None

    service_groups = defaultdict(list)
    for i, entry in enumerate(entries):
        decrypted = decrypt_entry(entry, fernet)
        service_groups[decrypted["service"]].append((i, decrypted))

    entry_search = st.text_input(label="", label_visibility="hidden", placeholder="Search All Entries")
    entry_search_lower = entry_search.lower()  # lowercase entry_search for easier matching

    entry_search_matches = []
    for i, decrypted in get_flattened_entries(service_groups):
        username = decrypted["username"]
        service = decrypted["service"]
        email = decrypted.get("email", "")

        username_l = username.lower()
        service_l = service.lower()
        email_l = email.lower() if email else ""

        if username_l.startswith(entry_search_lower):
            hit = username
        elif service_l.startswith(entry_search_lower):
            hit = service.title()
        elif email_l.startswith(entry_search_lower):
            hit = email
        else:
            continue

        entry_search_matches.append((service, username, i, hit))

    st.session_state.results_found_count = len(entry_search_matches)

    if "results_found_count" in st.session_state and entry_search:
        st.write(f"{st.session_state.results_found_count} results for '{entry_search}'")

    col1, col2 = st.columns([3, 4], gap="large")

    with col1:
        with st.container(height=500):

            if entry_search:
                for service, username, i, value_hit in entry_search_matches:
                    render_entry_button(service, username, i, value_hit)

            else:
                sort_option = st.selectbox("Sort by", ["A-Z", "Z-A", "Most Recent"], key="sort_option")

                if sort_option == "Most Recent":
                    flattened = get_flattened_entries(service_groups)
                    flattened.sort(key=lambda x: x[1].get("created_at", ""), reverse=True)
                    flattened = flattened[:10]

                    for i, decrypted in flattened:
                        render_entry_button(decrypted["service"], decrypted["username"], i)

                else:
                    sorted_services = sorted(service_groups.items(), reverse=(sort_option == "Z-A"))
                    for service, entry_list in sorted_services:
                        st.markdown(f"### <span style='color:#FFA500'>{service.title()}</span>", unsafe_allow_html=True)
                        for i, decrypted in entry_list:
                            if st.button(decrypted["username"], key=f"entry_button_{i}"):
                                st.session_state.selected_entry_index = i

    with col2:
        selected_index = st.session_state.selected_entry_index
        selected_entry = decrypt_entry(entries[selected_index], fernet)

        st.markdown(f"### <span style='color:#FFA500'>{selected_entry['service'].title()}</span>", unsafe_allow_html=True)
        st.markdown(f"**Username:** {selected_entry['username']}")

        # Password field with toggle
        pw_col1, pw_col2 = st.columns([6, 1])
        with pw_col2:
            show_password = st.checkbox("👁", key=f"show_password_{selected_index}")

        with pw_col1:
            display_pw = selected_entry["password"] if show_password else "●●●●●●●●"
            st.code(display_pw, language="text")

            strength_label, strength_color = STRENGTH_LABELS[int(selected_entry["strength_rating"])]
            st.markdown(
                f"<span style='color:{strength_color}; font-size: 15px; font-style: italic;'>{strength_label}</span>",
                unsafe_allow_html=True
            )

        if selected_entry["email"]:
            st.markdown(f"**Email:** {selected_entry['email']}")
        if selected_entry["notes"]:
            st.markdown(f"**Notes:** {selected_entry['notes']}")
        st.markdown(f"**Created At:** {selected_entry['created_at']}")
