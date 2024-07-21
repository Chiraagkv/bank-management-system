from datetime import date
import mysql.connector
from mysql.connector import Error


def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            auth_plugin="mysql_native_password",
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection = create_connection("localhost", "root", "xxxxxxx")
cursor = connection.cursor()
cursor.execute("use bank")


def list_schemes(scheme_type):
    try:
        cursor.execute(
            f"SELECT * FROM schemes WHERE scheme_type = '{scheme_type[:-1]}';"
        )
        a = list(cursor.fetchall())
        # print(cursor.fetchall())
        return a
    except Error as e:
        print(f"The error '{e}' occurred")


def check_user_password(email, password):
    cursor.execute(f"SELECT password FROM users where users.email = '{email}';")
    pwd = cursor.fetchone()
    if pwd[0] == password:
        return True
    else:
        return False


def check_employee_password(id, password):
    cursor.execute(
        f"SELECT employee_password FROM employees where employees.employee_id = {id};"
    )
    pwd = list(cursor.fetchone())
    print(pwd)
    if pwd[0] == password:
        return True
    else:
        return False


def display_everything(email):
    cursor.execute(f'SELECT * FROM users WHERE email = "{email}";')
    a = list(cursor.fetchone())
    return a


def update_user_info(info_dict, email):
    for i in info_dict.keys():
        cursor.execute(
            f'UPDATE users SET {i}="{info_dict[i]}" WHERE email = "{email}";'
        )
        connection.commit()
    cursor.execute(f"SELECT * FROM users where email = '{email}';")
    for i in cursor:
        print(i)


def add_investment(sch_id, email, amt):
    cursor.execute(f'SELECT user_id FROM users WHERE email = "{email}"')
    user_id = cursor.fetchone()[0]
    print(user_id)
    cursor.execute(
        f"INSERT INTO investments(user_id, scheme_id, start_date, amount) VALUES({user_id}, {sch_id},DATE(NOW()),{amt});"
    )
    connection.commit()


def add_user(name, email, pwd, dob, gen, addr, num, pin):
    cursor.execute(
        f'INSERT INTO users(username, password, birth_date, gender, address, primary_contact_number, email, pin) VALUES("{name}", "{pwd}", "{dob}","{gen}", "{addr}", "{num}", "{email}", {pin});'
    )
    connection.commit()


def check_deposit_type(acc_id):
    cursor.execute(f"SELECT scheme_id from investments where investment_id={acc_id}")
    sch_id = cursor.fetchone()[0]
    cursor.execute(f"SELECT scheme_subtype from schemes where scheme_id = {sch_id};")
    a = cursor.fetchone()[0]
    if a == "SB":
        return "savings"
    else:
        return "fixed"


def change_balance(acc_id, amt):
    if amt < 0:
        cursor.execute(f"SELECT amount from investments where investment_id = {acc_id}")
        balance = cursor.fetchone()[0]
        if abs(amt) < balance:
            cursor.execute(
                f"UPDATE investments SET amount = amount + {amt} where investment_id = {acc_id}"
            )
            connection.commit()
            return "good"
        else:
            return False
    else:
        cursor.execute(
            f"UPDATE investments SET amount = amount + {amt} where investment_id = {acc_id}"
        )
        connection.commit()
        return "good"

def show_investments(email):
    cursor.execute(f"SELECT user_id from users where email = '{email}'")
    usr_id = int(cursor.fetchone()[0])
    cursor.execute(f"SELECT * from investments where user_id= {usr_id}")
    return cursor.fetchall(), usr_id

def find_days(d1, d2):
    a = d1[-1] - d2[-1]
    b = d1[1] - d2[1]
    c = d1[0] - d2[0]
    return a + 12*b + 365*c

def find_full_savings(email):
    cursor.execute(f"SELECT user_id from users where email = '{email}'")
    usr_id = int(cursor.fetchone()[0])
    cursor.execute(f"SELECT amount, schemes.scheme_id, start_date from investments join schemes on investments.scheme_id=schemes.scheme_id where user_id={usr_id} and scheme_type='deposit'")
    invs = cursor.fetchall()
    tot = 0
    for i in invs:
        scheme_id = int(i[1])
        cursor.execute(f"SELECT interest_rate/100 from schemes where scheme_id={scheme_id}")
        interest = float(cursor.fetchone()[0])
        money = float(i[0])
        start_date = str(i[2])
        current_date = str(date.today())
        a = (int(current_date[0:4]), int(current_date[5:7]), int(current_date[8:])) 
        b = (int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:]))
        no_years = find_days(a, b)/365
        amt = money*((1+(interest/12))**(12*no_years))
        tot+= amt
        print(a, b, no_years)
    return tot
