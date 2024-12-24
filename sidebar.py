import streamlit as st


def add_sidebar(image_path):
    with st.sidebar:
        st.markdown("---")
        st.image(image_path, use_container_width=True)
        st.markdown("---")
