import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *

st.set_page_config(initial_sidebar_state="collapsed")
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

st.markdown("# Login")
email = st.text_input("Email Address", placeholder="your.name@mail.com")
password = st.text_input("Password", placeholder="password", type="password")
if st.button("Log-in", type="primary"):
    if check_user_password(email, password):
        open("D:\\bank\\creds.txt", "w").write(email)
        switch_page("usr_landing")

    else:
        st.write("wrong password or email id")
