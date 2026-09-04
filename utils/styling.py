import streamlit as st


def apply_custom_style():
    st.markdown("""
        <style>
        div[data-testid="stMetric"] {
            background-color: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 15px;
        }
        div[data-testid="stDataFrame"] {
            border-radius: 8px;
            overflow: hidden;
        }
        .stButton > button {
            border-radius: 8px;
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        h1, h2, h3 {
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)


def apply_page_accent(color):
    """Sets both the page's accent color AND a subtly-tinted background
    gradient derived from that same color, so each page feels distinct
    while staying dark enough for readable tables/text."""
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(
                160deg,
                color-mix(in srgb, {color} 22%, #0E1117) 0%,
                #0E1117 55%
            );
        }}
        div[data-testid="stMetric"] {{ border-left: 4px solid {color}; }}
        .stButton > button {{ background-color: {color}; color: white; border: none; }}
        </style>
    """, unsafe_allow_html=True)