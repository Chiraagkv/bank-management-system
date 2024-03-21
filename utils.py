import mysql.connector
from mysql.connector import Error


def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name, user=user_name, passwd=user_password
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection = create_connection("localhost", "root", "chinchira9*")

cursor = connection.cursor()
cursor.execute("use bank")


def list_schemes(scheme_type):
    try:
        cursor.execute(
            f"SELECT * FROM schemes WHERE schemes.scheme_type = '{scheme_type}'"
        )
        a = list(cursor)
        return a
    except Error as e:
        print(f"The error '{e}' occurred")


def check_user_password(email, password):
    cursor.execute(f"SELECT password FROM users where users.email = '{email}'")
    pwd = list(cursor)[0]
    if pwd[0] == password:
        return True
    else:
        return False


def check_employee_password(id, password):
    cursor.execute(
        f"SELECT employee_password FROM employees where employees.employee_id = {id}"
    )
    pwd = list(cursor)[0]
    if pwd[0] == password:
        return True
    else:
        return False


def display_everything(email):
    cursor.execute(f'SELECT * FROM users WHERE email = "{email}"')
    a = list(cursor)[0]
    return a


def display_schemes():
    cursor.execute(f"SELECT * FROM schemes")
    a = list(cursor)[0]
    return a