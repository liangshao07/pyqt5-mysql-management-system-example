import os

import pandas as pd
import pymysql

def get_connection():
    return pymysql.connect(host="localhost", port=3306, database="TextbookOrder", user='root', password='root')

def get_student_credentials():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select StudentUsername, StudentPassword from Student")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    account_list = [row[0] for row in rows]
    password_list = [row[1] for row in rows]
    return account_list, password_list

def get_admin_credentials():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select Username, Password from Administrator")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    account_list = [row[0] for row in rows]
    password_list = [row[1] for row in rows]
    return account_list, password_list

def get_textbooks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select TextbookID, TextbookName, Price, Author, Publisher from Textbook")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_student_orders(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"select StudentName from Student where StudentUsername = '{username}'")
    student_name = cur.fetchone()[0]
    cur.execute(f"select OrderID, StudentName, TextbookName, Price from Student_Order_View where StudentName = '{student_name}'")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def update_student_password(username, new_password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"update Student set StudentPassword = '{new_password}' where StudentUsername = '{username}'")
    conn.commit()
    cur.close()
    conn.close()

def place_order(student_id, book_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"insert into `Order`(StudentID, TextbookID) values ({student_id}, {book_id})")
    conn.commit()
    cur.close()
    conn.close()

def delete_order(order_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"delete from `Order` where OrderID = {order_id}")
    conn.commit()
    cur.close()
    conn.close()

def get_college_orders(college_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc('pCollege', args=(college_id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_major_orders(major_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc('pMajor', args=(major_id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_book_orders():
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc('pOderBook')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_book_orders_out():
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc('pOderBook')
    data = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]  # 获取字段名称
    # 使用 pandas.DataFrame
    df = pd.DataFrame(data, columns=column_names)
    filename = os.path.join('/Users/liang/Downloads', "data_Order_Book.csv")  # 指定导出路径
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    cur.close()
    conn.close()

def update_admin_password(username, new_password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"update Administrator set Password = '{new_password}' where Username = '{username}'")
    conn.commit()
    cur.close()
    conn.close()

def backup_database(backup_path):
    user = 'root'
    password = 'root'
    database = 'TextbookOrder'
    backup_filename = os.path.join(backup_path, f"{database}.sql")
    os.system(f"mysqldump -u{user} -p{password} {database} > {backup_filename}")

def recover_database(sql_file_path):
    user = 'root'
    password = 'root'
    database = 'TextbookOrder'
    os.system(f"mysql -u{user} -p{password} {database} < {sql_file_path}")