from PyQt5.QtWidgets import QMainWindow
from UI.LoginUI import Ui_LoginWindow
from s_main_window import SMainWindow
from a_main_window import AMainWindow
from db_utils import get_student_credentials, get_admin_credentials

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = None
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_S_login.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_A_login.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.pushButton_S_sure.clicked.connect(self.login_in_s_window)
        self.ui.pushButton_A_sure.clicked.connect(self.login_in_a_window)
        self.show()

    def login_in_s_window(self):
        account = self.ui.lineEdit_S_account.text()
        password = self.ui.lineEdit_S_password.text()
        account_list, password_list = get_student_credentials()
        for i in range(len(account_list)):
            if len(account) == 0 or len(password) == 0:
                self.ui.stackedWidget.setCurrentIndex(1)
            elif account == account_list[i] and password == password_list[i]:
                self.window = SMainWindow(account)
                self.close()
            else:
                self.ui.stackedWidget.setCurrentIndex(2)

    def login_in_a_window(self):
        account = self.ui.lineEdit_A_account.text()
        password = self.ui.lineEdit_A_password.text()
        account_list, password_list = get_admin_credentials()
        for i in range(len(account_list)):
            if len(account) == 0 or len(password) == 0:
                self.ui.stackedWidget.setCurrentIndex(1)
            elif account == account_list[i] and password == password_list[i]:
                self.window = AMainWindow(account)
                self.close()
            else:
                self.ui.stackedWidget.setCurrentIndex(2)