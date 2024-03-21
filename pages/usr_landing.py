import streamlit as st
from utils import *

email = open("D:\\bank\\creds.txt").read()
st.set_page_config(initial_sidebar_state="collapsed")
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

st.markdown("# User Landing Page")

option = st.selectbox(
    "Choose your action", ("See info", "check bank schemes", "do transactions")
)
if option == "See info":
    info = display_everything(email)[1:]
    info_dict = {
        "name": info[0],
        "password": info[1],
        "DOB": info[2],
        "Gender": info[3],
        "Address": info[4],
        "Email address": info[5],
        "Primary Phone number": info[6],
        "Secondary Phone number": info[7],
        "Credit Score": info[8],
    }
    st.write(info_dict.items())
elif option == "check bank schemes":
    st.write(display_schemes())