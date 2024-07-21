import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.switch_page_button import switch_page
from utils import *

st.set_page_config(initial_sidebar_state="collapsed")
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

email = open("./creds.txt").read()
info = display_everything(email=email)

total_money = find_full_savings(email)
st.write(info, total_money)