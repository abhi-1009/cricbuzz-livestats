import os


def get_secret(key, default=None):
    """
    Reads a config value from Streamlit secrets (when deployed on
    Streamlit Cloud) or from environment variables / .env (when
    running locally). Local .env values still work exactly as before.
    """
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)
