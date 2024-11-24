import os
import pandas as pd
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
import sys
from UI.SMainWindow import *
from UI.AMainWindow import *
from UI.LoginUI import *
import pymysql

user_now = ''


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = None # pycharm 智能添加的，出 bug 删掉
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        # 点击学生登录按钮(pushButton_S_login)，跳转学生登录界面(page_S_login)-0
        self.ui.pushButton_S_login.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        # 点击管理员登录按钮(pushButton_A_login)，跳转管理员登录界面(page_A_login)-1
        self.ui.pushButton_A_login.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        # 学生登录跳转到学生界面
        self.ui.pushButton_S_sure.clicked.connect(self.login_in_s_window)
        # 管理员登录跳转到管理员界面
        self.ui.pushButton_A_sure.clicked.connect(self.login_in_a_window)
        self.show()

    def login_in_s_window(self):
        account = self.ui.lineEdit_S_account.text()
        password = self.ui.lineEdit_S_password.text()
        print(account,password)
        account_list = []
        password_list = []
        conn = pymysql.connect(host="localhost", port=3306,
                               database="TextbookOrder",
                               user='root',
                               password='root')
        cur = conn.cursor()
        cur.execute("select StudentUsername,StudentPassword from Student")
        rows = cur.fetchall()
        cur.close()
        print(rows)
        for row in rows:
            account_list.append(row[0])
            password_list.append(row[1])
        print(account_list,password_list)
        print(account_list, password_list)
        for i in range(len(account_list)):
            if len(account) == 0 or len(password) == 0:
                self.ui.stackedWidget.setCurrentIndex(1)
            elif account == account_list[i] and password == password_list[i]:
                global user_now
                user_now = account
                self.window = SMainWindow()
                self.close()
            else:
                self.ui.stackedWidget.setCurrentIndex(2)

    def login_in_a_window(self):
        '''
        管理员登录
        :return:
        '''
        account = self.ui.lineEdit_A_account.text()
        password = self.ui.lineEdit_A_password.text()
        account_list = []
        password_list = []
        print(account, password)
        conn = pymysql.connect(host="localhost", port=3306,
                               database="TextbookOrder",
                               user='root',
                               password='root')
        cur = conn.cursor()
        cur.execute("select Username,Password from Administrator")
        rows = cur.fetchall()
        print(rows)
        for row in rows:
            account_list.append(row[0])
            password_list.append(row[1])

        conn.close()
        print(account_list, password_list)
        for i in range(len(account_list)):
            if len(account) == 0 or len(password) == 0:
                self.ui.stackedWidget.setCurrentIndex(1)
            elif account == account_list[i] and password == password_list[i]:
                global user_now
                user_now = account
                self.window = AMainWindow()
                self.close()
            else:
                self.ui.stackedWidget.setCurrentIndex(2)

class SMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login = None   # pycharm add if bug comment
        self.ui = Ui_SMainWindow()
        self.ui.setupUi(self)
        # 退出登录按钮
        self.ui.pushButton_login_out.clicked.connect(self.login_out)
        # 点击，跳转
        self.ui.pushButton_S_shopping.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        # 点击，跳转
        self.ui.pushButton_S_order.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        # 点击修改密码，跳转修改密码界面
        self.ui.pushButton_S_update_pw.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        # 修改密码
        self.ui.pushButton_S_M_sure.clicked.connect(self.change_password)
        # 订购界面
        # 订购确认按钮
        self.ui.pushButton_S_M_order_sure.clicked.connect(self.order_book)
        # 展示书籍列表
        self.model = QStandardItemModel(5, 4)   # 创建模型
        self.model.setHorizontalHeaderLabels(['书号','书名', '价格', '作者', '出版社']) # 创建横表头
        # 测试数据
        # data = (
        #     ('谜语治国', 1566.0, '万寿帝君·嘉靖', '大明王朝 1566'),
        #     ('从零开始学解谜', 77.0, '吕芳', '司礼监'),
        #     ('御龙术', 9999.0, '严嵩', '内阁'),
        #     ('清流的自我修养', 99.0, '徐阶', '内阁'))
        # 数据库连接，获取数据，并处理
        conn = pymysql.connect(host="localhost", port=3306,
                               database="TextbookOrder",
                               user='root',
                               password='root')
        cur = conn.cursor()
        cur.execute("select TextbookID,TextbookName,Price,Author,Publisher from Textbook")  # 查询书籍
        data = cur.fetchall()
        # 遍历data 列表，添加到模型中
        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QStandardItem(str(data[row][col]))
                self.model.setItem(row, col, item)
        # UI 已经创建 QTableView，现在设置模型到 QTableView，并进行基础设置
        self.ui.tableView_S_M_bookList.setModel(self.model)
        # 设置表头自适应宽度
        self.ui.tableView_S_M_bookList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 隐藏垂直表头（行号）
        self.ui.tableView_S_M_bookList.verticalHeader().setVisible(False)
        # 我的订单列表
        # 1. 下方查询我的订单
        self.model2 = QStandardItemModel(4, 4)  # 创建模型
        self.model2.setHorizontalHeaderLabels(['订单号','姓名', '书名', '价格'])
        cur2 = conn.cursor()
        print(user_now)
        cur2.execute(f"select StudentName from Student where StudentUsername = '{user_now}' ")
        student_name = cur2.fetchall()
        # print(student_name[0][0])
        cur3 = conn.cursor()
        cur3.execute(f"select OrderID,StudentName,TextbookName,Price from Student_Order_View where StudentName = '{student_name[0][0]}'")
        conn.close()
        data2 = cur3.fetchall()
        # print(data)
        # print(data2)
        for row in range(len(data2)):
            for col in range(len(data2[row])):
                item = QStandardItem(str(data2[row][col]))
                self.model2.setItem(row, col, item)

        self.ui.tableView_2.setModel(self.model2)
        self.ui.tableView_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 隐藏垂直表头（行号）
        self.ui.tableView_2.verticalHeader().setVisible(False)
        # 2. 上方删除
        self.ui.pushButton_S_M_order_sure_update.clicked.connect(self.update_order_student)
        self.show()

    def login_out(self):
        '''
        退出登录
        :return:
        '''
        global user_now
        self.close()
        self.login = LoginWindow()
        user_now = ''

    def change_password(self):
        '''
        修改密码
        :return:
        '''
        global user_now
        password_old = self.ui.lineEdit_S_M_password.text()
        password_new = self.ui.lineEdit_S_M_new_password.text()
        if len(password_old) == 0 or len(password_new) == 0 or len(self.ui.lineEdit_S_M_new_password_sure.text()) == 0:
            self.ui.stackedWidget_2.setCurrentIndex(1)
        elif self.ui.lineEdit_S_M_new_password_sure.text() == password_new:
            self.ui.stackedWidget_2.setCurrentIndex(3)
            # 更新密码
            conn = pymysql.connect(host="localhost", port=3306,
                                   database="TextbookOrder",
                                   user='root',
                                   password='root')
            cur = conn.cursor()
            cur.execute(f"update Student set StudentPassword = '{password_new}' where StudentUsername = '{user_now}'")
            conn.commit()
            conn.close()
        else:
            self.ui.stackedWidget_2.setCurrentIndex(2)

    def order_book(self):
        book = self.ui.lineEdit_S_M_bookID.text()
        student = self.ui.lineEdit_S_M_studentID.text()
        # 连接数据库
        conn = pymysql.connect(host="localhost", port=3306,
                               database="TextbookOrder",
                               user='root',
                               password='root')
        cur = conn.cursor()
        cur.execute(f"insert into `Order`(StudentID, TextbookID) values ({student}, {book}) ")
        conn.commit()
        conn.close()
        # 清除输入框
        self.ui.lineEdit_S_M_studentID.clear()
        self.ui.lineEdit_S_M_bookID.clear()

    def update_order_student(self):
        order_id = self.ui.lineEdit_S_M_order_update.text()
        print(order_id)
        # 连接数据库
        conn = pymysql.connect(host="localhost", port=3306,
                               database="TextbookOrder",
                               user='root',
                               password='root')
        cur = conn.cursor()
        cur.execute(f"delete from `Order` where OrderID = {order_id}")
        conn.commit()

        # 1. 下方查询我的订单————简单粗暴，用于删除后，重新加载显示
        self.model2 = QStandardItemModel(4, 4)  # 创建模型
        self.model2.setHorizontalHeaderLabels(['订单号', '姓名', '书名', '价格'])
        cur2 = conn.cursor()
        print(user_now)
        cur2.execute(f"select StudentName from Student where StudentUsername = '{user_now}' ")
        student_name = cur2.fetchall()
        print(student_name[0][0])
        cur3 = conn.cursor()
        cur3.execute(f"select OrderID,StudentName,TextbookName,Price from Student_Order_View where StudentName = '{student_name[0][0]}'")
        data2 = cur3.fetchall()
        # print(data)
        # print(data2)
        for row in range(len(data2)):
            for col in range(len(data2[row])):
                item = QStandardItem(str(data2[row][col]))
                self.model2.setItem(row, col, item)

        self.ui.tableView_2.setModel(self.model2)
        self.ui.tableView_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 隐藏垂直表头（行号）
        self.ui.tableView_2.verticalHeader().setVisible(False)

        conn.close()
        # 清除输入框
        self.ui.lineEdit_S_M_studentID.clear()
        self.ui.lineEdit_S_M_bookID.clear()

class AMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login = None   # pycharm add if bug comment
        self.ui = Ui_AMainWindow()
        self.ui.setupUi(self)
        # 退出登录
        self.ui.pushButton_A_login_out.clicked.connect(self.login_out_a)
        # 左边导航栏页跳转
        self.ui.pushButton_A_college.clicked.connect(lambda : self.ui.stackedWidget_A.setCurrentIndex(0))
        self.ui.pushButton_A_major.clicked.connect(lambda : self.ui.stackedWidget_A.setCurrentIndex(1))
        self.ui.pushButton_A_book.clicked.connect(lambda : self.ui.stackedWidget_A.setCurrentIndex(2))
        self.ui.pushButton_A_backup_recover.clicked.connect(lambda : self.ui.stackedWidget_A.setCurrentIndex(3))
        self.ui.pushButton_A_update.clicked.connect(lambda : self.ui.stackedWidget_A.setCurrentIndex(4))
        # 修改密码
        self.ui.pushButton_A_M_sure.clicked.connect(self.change_password_a)
        # 学院订购情况
        self.ui.pushButton_A_M_college_sure.clicked.connect(self.order_college)
        # 专业订购情况
        self.ui.pushButton_A_M_major_sure.clicked.connect(self.order_major)
        # 书籍订购情况
        self.ui.pushButton_A_M_out.clicked.connect(self.order_book_out)
        self.model_a_out = QStandardItemModel(1, 2)
        self.model_a_out.setHorizontalHeaderLabels(['书号', '订购数量'])  # 创建横表头
        conn = pymysql.connect(host="localhost", port=3306,
                               database="TextbookOrder",
                               user='root',
                               password='root')
        cursor = conn.cursor()
        cursor.callproc('pOderBook')
        # 获取存储过程的结果
        data = cursor.fetchall()
        # print(data)
        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QStandardItem(str(data[row][col]))
                self.model_a_out.setItem(row, col, item)
        # UI 已经创建 QTableView，现在设置模型到 QTableView，并进行基础设置
        self.ui.tableView_A_M_book_out.setModel(self.model_a_out)
        # 设置表头自适应宽度
        self.ui.tableView_A_M_book_out.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 隐藏垂直表头（行号）
        self.ui.tableView_A_M_book_out.verticalHeader().setVisible(False)
        conn.close()

        # 备份与恢复数据库
        self.ui.pushButton_A_M_backup.clicked.connect(self.backup_data)
        self.ui.pushButton_A_M_recover.clicked.connect(self.recover_data)

        self.show()

    def login_out_a(self):
        '''
        退出登录
        :return:
        '''
        global user_now
        self.close()
        self.login = LoginWindow()
        user_now = ''

    def change_password_a(self):
        '''
        修改密码
        :return:
        '''
        global user_now
        password_old = self.ui.lineEdit_A_M_password.text()
        password_new = self.ui.lineEdit_A_M_new_password.text()
        if len(password_old) == 0 or len(password_new) == 0 or len(self.ui.lineEdit_A_M_new_password_sure.text()) == 0:
            self.ui.stackedWidget_A_2.setCurrentIndex(1)
        elif self.ui.lineEdit_A_M_new_password_sure.text() == password_new:
            self.ui.stackedWidget_A_2.setCurrentIndex(3)
            conn = pymysql.connect(host="localhost", port=3306,
                                   database="TextbookOrder",
                                   user='root',
                                   password='root')
            # 更新密码
            cur = conn.cursor()
            cur.execute(f"update Administrator set Password = '{password_new}' where Username = '{user_now}'")
            conn.commit()
            conn.close()
        else:
            self.ui.stackedWidget_A_2.setCurrentIndex(2)

    def order_college(self):
        self.model_a = QStandardItemModel(2,  2)  # 创建模型
        self.model_a.setHorizontalHeaderLabels(['书号', '订购数量'])  # 创建横表头
        conn = pymysql.connect(host="localhost", port=3306,
                               database="TextbookOrder",
                               user='root',
                               password='root')
        cursor = conn.cursor()
        # 调用存储过程
        collegeid = self.ui.lineEdit_A_M_college.text()
        print(collegeid)
        cursor.callproc('pCollege', args=(collegeid,))
        # 获取存储过程的结果
        data = cursor.fetchall()
        # print(data)
        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QStandardItem(str(data[row][col]))
                self.model_a.setItem(row, col, item)
        # UI 已经创建 QTableView，现在设置模型到 QTableView，并进行基础设置
        self.ui.tableView_A_M_bookList_college.setModel(self.model_a)
        # 设置表头自适应宽度
        self.ui.tableView_A_M_bookList_college.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 隐藏垂直表头（行号）
        self.ui.tableView_A_M_bookList_college.verticalHeader().setVisible(False)
        conn.close()
        self.ui.lineEdit_A_M_college.clear()
    def order_major(self):
        self.model_a_m = QStandardItemModel(2, 2)  # 创建模型
        self.model_a_m.setHorizontalHeaderLabels(['书号', '订购数量'])  # 创建横表头
        conn = pymysql.connect(host="localhost", port=3306,
                               database="TextbookOrder",
                               user='root',
                               password='root')
        cursor = conn.cursor()
        # 调用存储过程
        majorid = self.ui.lineEdit_A_M_major.text()
        print(majorid)
        cursor.callproc('pMajor', args=(majorid,))
        # 获取存储过程的结果
        data = cursor.fetchall()
        print(data)
        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QStandardItem(str(data[row][col]))
                self.model_a_m.setItem(row, col, item)
        # UI 已经创建 QTableView，现在设置模型到 QTableView，并进行基础设置
        self.ui.tableView_A_M_major.setModel(self.model_a_m)
        # 设置表头自适应宽度
        self.ui.tableView_A_M_major.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 隐藏垂直表头（行号）
        self.ui.tableView_A_M_major.verticalHeader().setVisible(False)
        conn.close()
        # 清除输入框
        self.ui.lineEdit_A_M_major.clear()

    def order_book_out(self):
        self.model_a_out = QStandardItemModel(1, 2)
        self.model_a_out.setHorizontalHeaderLabels(['书号', '订购数量'])  # 创建横表头
        conn = pymysql.connect(host="localhost", port=3306,
                               database="TextbookOrder",
                               user='root',
                               password='root')
        cursor = conn.cursor()
        cursor.callproc('pOderBook')
        # 获取存储过程的结果
        data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]  # 获取字段名称
        # 使用 pandas.DataFrame
        df = pd.DataFrame(data, columns=column_names)
        filename = os.path.join('/Users/liang/Downloads', "data_Order_Book.csv")  # 指定导出路径
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        success_msg = QtWidgets.QMessageBox()
        success_msg.setText("导出成功！")
        success_msg.exec()
        conn.close()
    def backup_data(self):
        user='root'
        password='root'
        database='TextbookOrder'
        backup_path = '/Users/liang/Downloads'
        backup_filename = os.path.join(backup_path, f"{database}.sql")
        try:
            os.system(f"mysqldump -u{user} -p{password} {database} > {backup_filename}")
            success_msg = QtWidgets.QMessageBox()
            success_msg.setText(f"数据库备份成功，文件路径为 {backup_path}")
            success_msg.exec()
        except Exception as e:
            error_msg = QtWidgets.QMessageBox()
            error_msg.setText(f"数据库备份失败: {str(e)}")
            error_msg.exec()
    def recover_data(self):
        user='root'
        password='root'
        database='TextbookOrder'
        sql_file_path = '/Users/liang/Downloads/TextbookOrder.sql'
        try:
            os.system(f"mysql -u{user} -p{password} {database} < {sql_file_path}")
            success_msg = QtWidgets.QMessageBox()
            success_msg.setText("数据库恢复成功")
            success_msg.exec()
        except Exception as e:
            error_msg = QtWidgets.QMessageBox()
            error_msg.setText(f"数据库恢复失败: {str(e)}")
            error_msg.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    # window = AMainWindow()
    # window = SMainWindow() # test
    sys.exit(app.exec_())
