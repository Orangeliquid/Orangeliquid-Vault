import streamlit as st


def get_flattened_entries(service_groups):
    return [
        (i, decrypted)
        for service, entries in service_groups.items()
        for i, decrypted in entries
    ]


def render_entry_button(service, username, index, value_hit=None):
    st.markdown(f"#### <span style='color:#FFA500'>{service.title()}</span>", unsafe_allow_html=True)
    display_text = value_hit if value_hit else username
    if st.button(display_text, key=f"entry_button_{index}"):
        st.session_state.selected_entry_index = index
