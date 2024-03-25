import streamlit as st
from utils import *
import datetime
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(initial_sidebar_state="collapsed")
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

st.markdown("# User Sign-Up")
name = st.text_input("#### Full Name", placeholder="Full Name")
email = st.text_input("#### Email.id", placeholder="your.email@gmail.com")
pwd = st.text_input(
    "#### Set a strong password", placeholder="password", type="password"
)
birth_date = st.date_input(
    label="#### Date of Birth",
    format="YYYY-MM-DD",
    value=datetime.datetime(2001, 2, 3),
    min_value=datetime.date(1940, 1, 1),
    max_value=datetime.date(
        datetime.date.today().year - 18,
        datetime.date.today().month,
        datetime.date.today().day,
    )
)
gender = "m" if st.radio("#### select gender", ["Male", "Female"]) == "Male" else "f"
address = st.text_area("#### Address (Optional)")
primary_contact_number = st.text_input("#### Primary Contact Number")
pin = st.text_input("#### Pin")

if st.button("Sign-up"):
    if name and email and pwd and address and birth_date and gender and primary_contact_number and pin:
        add_user(name, email, pwd, birth_date, gender, address, primary_contact_number, pin)
        st.write(name, email, pwd, birth_date, gender, address, primary_contact_number, pin, "added")
        switch_page("usr_login")
    else:
        st.write(
            "Name, email, password, DOB, gender, address, pin and primary contact number are mandatory."
        )
