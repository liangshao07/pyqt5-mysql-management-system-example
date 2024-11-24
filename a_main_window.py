from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from UI.AMainWindow import Ui_AMainWindow
from db_utils import get_college_orders, get_major_orders, get_book_orders, update_admin_password, backup_database, \
    recover_database, get_book_orders_out


class AMainWindow(QMainWindow):
    def __init__(self, user_now):
        super().__init__()
        self.user_now = user_now
        self.login = None
        self.ui = Ui_AMainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_A_login_out.clicked.connect(self.login_out_a)
        self.ui.pushButton_A_college.clicked.connect(lambda: self.ui.stackedWidget_A.setCurrentIndex(0))
        self.ui.pushButton_A_major.clicked.connect(lambda: self.ui.stackedWidget_A.setCurrentIndex(1))
        self.ui.pushButton_A_book.clicked.connect(lambda: self.ui.stackedWidget_A.setCurrentIndex(2))
        self.ui.pushButton_A_backup_recover.clicked.connect(lambda: self.ui.stackedWidget_A.setCurrentIndex(3))
        self.ui.pushButton_A_update.clicked.connect(lambda: self.ui.stackedWidget_A.setCurrentIndex(4))
        self.ui.pushButton_A_M_sure.clicked.connect(self.change_password_a)
        self.ui.pushButton_A_M_college_sure.clicked.connect(self.order_college)
        self.ui.pushButton_A_M_major_sure.clicked.connect(self.order_major)
        self.ui.pushButton_A_M_out.clicked.connect(self.order_book_out)
        self.ui.pushButton_A_M_backup.clicked.connect(self.backup_data)
        self.ui.pushButton_A_M_recover.clicked.connect(self.recover_data)
        self.setup_order_book_list()
        self.show()

    def login_out_a(self):
        from login_window import LoginWindow  # 延迟导入
        self.close()
        self.login = LoginWindow()

    def change_password_a(self):
        password_old = self.ui.lineEdit_A_M_password.text()
        password_new = self.ui.lineEdit_A_M_new_password.text()
        if len(password_old) == 0 or len(password_new) == 0 or len(self.ui.lineEdit_A_M_new_password_sure.text()) == 0:
            self.ui.stackedWidget_A_2.setCurrentIndex(1)
        elif self.ui.lineEdit_A_M_new_password_sure.text() == password_new:
            self.ui.stackedWidget_A_2.setCurrentIndex(3)
            update_admin_password(self.user_now, password_new)
        else:
            self.ui.stackedWidget_A_2.setCurrentIndex(2)

    def order_college(self):
        self.model_a = QStandardItemModel(2, 2)
        self.model_a.setHorizontalHeaderLabels(['书号', '订购数量'])
        collegeid = self.ui.lineEdit_A_M_college.text()
        data = get_college_orders(collegeid)
        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QStandardItem(str(data[row][col]))
                self.model_a.setItem(row, col, item)
        self.ui.tableView_A_M_bookList_college.setModel(self.model_a)
        self.ui.tableView_A_M_bookList_college.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView_A_M_bookList_college.verticalHeader().setVisible(False)
        self.ui.lineEdit_A_M_college.clear()

    def order_major(self):
        self.model_a_m = QStandardItemModel(2, 2)
        self.model_a_m.setHorizontalHeaderLabels(['书号', '订购数量'])
        majorid = self.ui.lineEdit_A_M_major.text()
        data = get_major_orders(majorid)
        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QStandardItem(str(data[row][col]))
                self.model_a_m.setItem(row, col, item)
        self.ui.tableView_A_M_major.setModel(self.model_a_m)
        self.ui.tableView_A_M_major.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView_A_M_major.verticalHeader().setVisible(False)
        self.ui.lineEdit_A_M_major.clear()

    def setup_order_book_list(self):
        self.model_a_out = QStandardItemModel(1, 2)
        self.model_a_out.setHorizontalHeaderLabels(['书号', '订购数量'])
        data = get_book_orders()
        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QStandardItem(str(data[row][col]))
                self.model_a_out.setItem(row, col, item)
        self.ui.tableView_A_M_book_out.setModel(self.model_a_out)
        self.ui.tableView_A_M_book_out.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView_A_M_book_out.verticalHeader().setVisible(False)

    def order_book_out(self):
        get_book_orders_out()
        success_msg = QtWidgets.QMessageBox()
        success_msg.setText("导出成功！")
        success_msg.exec()


    def backup_data(self):
        backup_path = '/Users/liang/Downloads'
        try:
            backup_database(backup_path)
            success_msg = QMessageBox()
            success_msg.setText(f"数据库备份成功，文件路径为 {backup_path}")
            success_msg.exec()
        except Exception as e:
            error_msg = QMessageBox()
            error_msg.setText(f"数据库备份失败: {str(e)}")
            error_msg.exec()

    def recover_data(self):
        sql_file_path = '/Users/liang/Downloads/TextbookOrder.sql'
        try:
            recover_database(sql_file_path)
            success_msg = QMessageBox()
            success_msg.setText("数据库恢复成功")
            success_msg.exec()
        except Exception as e:
            error_msg = QMessageBox()
            error_msg.setText(f"数据库恢复失败: {str(e)}")
            error_msg.exec()