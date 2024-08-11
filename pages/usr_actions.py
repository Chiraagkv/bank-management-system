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

st.markdown("# User Actions Page")
st.markdown("## Choose Your Action")
option = st.selectbox(
    "",
    (
        "Edit info",
        "check bank schemes",
        "Make transactions",
        "Take a Loan",
        "Create a Deposit",
        "Check Your Plans",
        "Pay Your Loans"
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
        out = update_user_info(info_dict, email)
        if out:
            st.write(out)

elif option == "check bank schemes":
    schemetype = st.radio("**Select type of schemes**", ["Loans", "Deposits"])
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
    st.dataframe(df)

elif option == "Take a Loan":
    loans = list_schemes("Loans")
    loan_dict = {
        "Scheme ID": [loans[i][0] for i in range(len(loans))],
        "Scheme Name": [loans[i][1] for i in range(len(loans))],
        "scheme Type": [loans[i][2] for i in range(len(loans))],
        "scheme Subtype": [loans[i][3] for i in range(len(loans))],
        "Interest Rate": [loans[i][4] for i in range(len(loans))],
        "Tenure (Months)": [loans[i][5] for i in range(len(loans))],
    }
    df = pd.DataFrame(loan_dict)
    st.dataframe(df, hide_index=True)
    opt = st.text_input("**Enter scheme id**")
    if opt in [str(loans[i][0]) for i in range(len(loans))]:
        amount = st.text_input("Enter principal amount", value=None)
        if amount:
            a = amount.replace(".", "", 1)
            if a.isnumeric():
                info = display_everything(email)
                print(info)
                pin = st.text_input("Enter account pin", type="password", value=None)
                if pin and pin.isnumeric():
                    if int(info[-1]) == int(pin):
                        out = add_investment(opt, email, float(amount))
                        if not out:
                            st.write("Loan has been requested. We will look into it soon.")
                        else:
                            print(out)
                    elif pin and int(pin) != info[-1]:
                        st.write("Wrong pin. Try again.")
                else:
                    st.write("invalid pin")
            else:
                st.write("Amount has to be a number")
    else:
        print("Invalid Scheme ID")

elif option == "Create a Deposit":
    deps = list_schemes("Deposits")
    dep_dict = {
        "Scheme ID": [deps[i][0] for i in range(len(deps))],
        "Scheme Name": [deps[i][1] for i in range(len(deps))],
        "scheme Type": [deps[i][2] for i in range(len(deps))],
        "scheme Subtype": [deps[i][3] for i in range(len(deps))],
        "Interest Rate": [deps[i][4] for i in range(len(deps))],
        "Tenure (Months)": [deps[i][5] for i in range(len(deps))],
    }
    df = pd.DataFrame(dep_dict)
    st.dataframe(df, hide_index=True)
    opt = st.text_input("**Enter scheme id**", value=None)
    if opt in [str(deps[i][0]) for i in range(len(deps))]:
        amount = st.text_input("Enter principal amount", value=None)
        if amount:
            a = amount.replace(".", "", 1)
            if a.isnumeric():
                info = display_everything(email)
                pin = st.text_input("Enter account pin", type="password", value=None)
                if pin and pin.isnumeric():
                    if info[-1] == int(pin):
                        add_investment(opt, email, float(amount))
                        st.write(
                            "Deposit will be approved soon. PLease visit bank to deposit the above amount"
                        )
                    elif pin and int(pin) != info[-1]:
                        st.write("Wrong pin. Try again.")
                elif pin:
                    st.write("Invalid pin")
            else:
                st.write("amount is not numeric")
    else:
        st.write("Invalid Scheme ID")

elif option == "Make transactions":
    usr_acc_id = st.text_input(
        "Enter account id (Check 'Check your plans' page to find appropriate savings account)",
        value=None,
    )
    rec_acc_id = st.text_input("Enter receiver's account_id", value=None)
    amount = st.text_input("Enter amount to be transferred", value=None)
    pin = st.text_input("Enter account pin", type="password", value=None)
    if st.button("Make Payment"):
        if (
            check_deposit_type(int(usr_acc_id)) + check_deposit_type(int(rec_acc_id))
            == "savingssavings"
            and amount
        ):
            info = display_everything(email)
            if pin and pin.isnumeric():
                if info[-1] == int(pin):
                    a = change_balance(int(usr_acc_id), -int(amount))
                    if a:
                        change_balance(int(rec_acc_id), int(amount))
                    else:
                        st.write("Balance insufficient")
                else:
                    st.write("Wrong password")
elif option == "Check Your Plans":
    invs = show_investments(email)
    st.write(invs)
elif option == "Pay Your Loans":
    loans = show_all_loans(email)
    l = st.radio("Choose loan to pay back", [i for i in loans])
    inv_id = l[0]
    st.write(f"You have {see_due(inv_id)} to repay. Choose your savings account from which you will pay.")

    # change_balance
    usr_acc_id = st.text_input(
        "Enter account id (Check 'Check your plans' page to find appropriate savings account)",
        value=None,
    )
    amount = see_due(inv_id)
    pin = st.text_input("Enter account pin", type="password", value=None)
    if st.button("Make Payment"):
        if (check_deposit_type(int(usr_acc_id))) == "savings" and amount:
            info = display_everything(email)
            if pin and pin.isnumeric():
                if info[-1] == int(pin):
                    a = change_balance(int(usr_acc_id), -int(amount))
                    if a:
                        st.write("Payment successful")
                    else:
                        st.write("Balance insufficient")
                else:
                    st.write("Wrong password")