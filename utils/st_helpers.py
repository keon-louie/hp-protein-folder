import streamlit as st
from streamlit.delta_generator import DeltaGenerator


def centered_title(text: str, container: DeltaGenerator = st):
    container.markdown(
        f"<h2 style='text-align: center;'>{text}</h2>",
        unsafe_allow_html=True)

def centered_subheader(text: str, container: DeltaGenerator = st):
    container.markdown(
        f"<h3 style='text-align: center;'>{text}</h3>",
        unsafe_allow_html=True)

def centered_text(text: str, container: DeltaGenerator = st):
    container.markdown(
        f"<div style='text-align: center;'>{text}</div>",
        unsafe_allow_html=True
    )

def centered_caption(text: str, container: DeltaGenerator = st):
    container.markdown(
        f"<div style='text-align: center; color: grey; font-size: 0.8em;'>{text}</div>",
        unsafe_allow_html=True)

def hide_anchor():
    st.markdown("""
            <style>
            [data-testid="stHeaderActionElements"] {
                display: none !important;
            }
            </style>
            """, unsafe_allow_html=True)

def remove_top_margin():
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def fix_layout():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem !important;
                padding-bottom: 0rem !important;
            }

            footer {
                display: none !important;
            }
            #MainMenu {
                visibility: hidden;
            }
            [data-testid="stHeaderActionElements"] {
                display: none !important;
            }

            .footer-container {
                position: relative;
                width: 100%;
                margin-top: 50px;
                padding: 20px;
                text-align: center;
                background-color: #f9f9f9;
                border-top: 1px solid #e6e6e6;
                box-shadow: 0 0 0 100vmax #f9f9f9;
                clip-path: inset(0 -100vmax 0 -100vmax);
            }

            .footer-row {
                margin-bottom: 8px;
                font-size: 14px;
                color: #444;
            }
            .footer-row a {
                color: #444 !important;
                text-decoration: none;
                margin: 0 8px;
                font-weight: 600;
            }
            .footer-row a:hover {
                color: #d33 !important;
                text-decoration: underline;
            }
            .footer-citation {
                font-size: 12px;
                color: #888;
            }
        </style>
    """, unsafe_allow_html=True)

def border():
    st.markdown("""
            <style>
                header[data-testid="stHeader"] {
                    border-bottom: 0.5px solid #e6e6e6;
                    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                }
            </style>
        """, unsafe_allow_html=True)

def fix_dropdown_cursor():
    st.markdown("""
        <style>
        div[data-baseweb="select"] {
            cursor: pointer !important;
        }
        div[data-baseweb="select"] * {
            cursor: pointer !important;
        }
        div[data-baseweb="select"] input {
            cursor: pointer !important;
        }
        </style>
    """, unsafe_allow_html=True)