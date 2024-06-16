import streamlit as st
from utils import *
import pandas as pd

email = open("./creds.txt").read()
st.set_page_config(initial_sidebar_state="collapsed")
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

st.markdown("# User Landing Page")

option = st.selectbox(
    "Choose your action",
    (
        "Edit info",
        "check bank schemes",
        "Make transactions",
        "Take a Loan",
        "Create a Deposit",
        "Check Your Plans",
    ),
)
if option == "Edit info":
    info = display_everything(email)
    info_dict = {
        "username": info[1],
        "password": info[2],
        "birth_date": info[3],
        "gender": info[4],
        "address": info[5],
        "email": info[6],
        "Primary_contact_number": info[7],
        "Secondary_contact_number": info[8],
        "Pin": info[-1],
    }
    new_info = {}
    for i in info_dict.items():
        a = st.text_input(i[0], placeholder=i[1])
        new_info[i[0]] = a
    for i in new_info.items():
        if i[1]:
            info_dict[i[0]] = i[1]
    if st.button("Done"):
        update_user_info(info_dict, email)

elif option == "check bank schemes":
    schemetype = st.radio("**Select loan or deposit**", ["Loans", "Deposits"])
    all_schemes = list_schemes(schemetype)
    table = {
        "Scheme ID": [all_schemes[i][0] for i in range(len(all_schemes))],
        "Scheme Name": [all_schemes[i][1] for i in range(len(all_schemes))],
        "scheme Type": [all_schemes[i][2] for i in range(len(all_schemes))],
        "scheme Subtype": [all_schemes[i][3] for i in range(len(all_schemes))],
        "Interest Rate": [all_schemes[i][4] for i in range(len(all_schemes))],
        "Tenure (Months)": [all_schemes[i][5] for i in range(len(all_schemes))],
    }
    df = pd.DataFrame(table)
    st.table(df)

elif option == "Take a Loan":
    loans = list_schemes("Loans")
    opt = st.radio("**Select loan**", loans)[0]
    print(opt)
    amount = st.text_input("Enter principal amount")
    if amount:
        info = display_everything(email)
        print(info)
        pin = st.text_input("Enter account pin", type="password")
        if int(info[-1]) == int(pin):
            add_investment(opt, email, float(amount))
            st.write("Loan has been requested. We will look into it soon.")
        elif pin and int(pin) != info[-1]:
            st.write("Wrong pin. Try again.")
        else:
            st.write("")

elif option == "Create a Deposit":
    deps = list_schemes("Deposits")
    opt = st.radio("**Select Deposit type**", deps)[0]
    print(opt)
    amount = st.text_input("Enter principal amount")
    if amount:
        info = display_everything(email)
        pin = st.text_input("Enter account pin", type="password")
        if info[-1] == int(pin):
            add_investment(opt, email, float(amount))
            st.write("Deposit will be approved soon")
        elif pin and int(pin) != info[-1]:
            st.write("Wrong pin. Try again.")
        else:
            st.write("")

elif option == "Make transactions":
    usr_acc_id = st.text_input(
        "Enter account id (Check 'Check your plans' page to find appropriate savings account)"
    )
    rec_acc_id = st.text_input("Enter receiver's account_id")
    amount = st.text_input("Enter amount to be transferred")
    pin = st.text_input("Enter account pin", type="password")
    if st.button("Make Payment"):
        if (
            check_deposit_type(int(usr_acc_id)) + check_deposit_type(int(rec_acc_id))
            == "savingssavings"
            and amount
        ):
            info = display_everything(email)
            if info[-1] == int(pin):
                a = change_balance(int(usr_acc_id), -int(amount))
                if a:
                    change_balance(int(rec_acc_id), int(amount))
                else:
                    st.write("Balance insufficient")
            else:
                st.write("Wrong password")
