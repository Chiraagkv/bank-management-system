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
st.markdown("# User information")
email = open("./creds.txt").read()
info = display_everything(email=email)
attributes = [
    "User ID",
    "Name",
    "Account password",
    "Date of Birth",
    "Gender",
    "Address",
    "Email ID",
    "Primary Contact Number",
    "Secondary Contact Number",
    "Credit Score",
    "Aadhar Number",
    "PAN Number",
    "Account Pin",
]
for n, i in enumerate(info):
    if i:
        st.markdown(f"#### **{attributes[n]}**: \n{i}")
        # st.divider()
        # st.write(f"\t{i}")

total_money = find_full_savings(email)

if st.button("Go to actions page", type="primary"):
    switch_page("usr_actions")
