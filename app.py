import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(initial_sidebar_state="collapsed")
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""

st.markdown(no_sidebar_style, unsafe_allow_html=True)

if st.button("User Log-in"):
    switch_page("usr_login")
if st.button("Employee Log-in"):
    switch_page("emp_login")
if st.button("New User Sign-up"):
    switch_page("usr_signup")
