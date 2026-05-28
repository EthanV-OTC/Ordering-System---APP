from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt, QSettings
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shitty lil Uber-Eats ahh ordering sustem")
        self.resize(1920,1080)

        self.settings = QSettings("MyShittyCompany", "UberEatsClone")

        try:
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("style.qss not found, skipping...")

        self.is_logged_in = False

        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(main_container)
        
        self.navbar = QHBoxLayout()
        self.setup_navbar()
        main_layout.addLayout(self.navbar)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        self.Home = self.create_Home()
        self.Login = self.create_Login()
        self.Store1 = self.create_Store1()
        
        self.stacked_widget.addWidget(self.Home)
        self.stacked_widget.addWidget(self.Login)
        self.stacked_widget.addWidget(self.Store1)

        self.btn_logout.setVisible(False)
        self.btn_login.setVisible(True)

        self.load_remembered_credentials()

    def setup_navbar(self):
        self.btn_login = QPushButton("Login")
        self.btn_logout = QPushButton("Logout")
        btn_home = QPushButton("Home")
        btn_store = QPushButton("Store 1")

        self.btn_login.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        btn_store.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_logout.clicked.connect(self.logout_user)

        self.navbar.addWidget(self.btn_login)
        self.navbar.addWidget(self.btn_logout)
        self.navbar.addWidget(btn_home)
        self.navbar.addWidget(btn_store)
        self.navbar.addStretch()

    def create_Home(self):
        page = QWidget()
        layout = QVBoxLayout()
        
        self.logged_in_label = QLabel("The user is logged in")
        self.logged_in_label.setVisible(False) 

        self.logged_out_label = QLabel("The User is logged out")
        self.logged_out_label.setVisible(True)

        label = QLabel("This is the Home Page")
        layout.addWidget(label)
        layout.addWidget(self.logged_in_label) 
        layout.addWidget(self.logged_out_label)
        page.setLayout(layout)
        return page

    def create_Login(self):
        page = QWidget()
        main_layout = QVBoxLayout()
        
        form_widget = QWidget()
        form_widget.setFixedWidth(400)
        layout = QVBoxLayout(form_widget)
        layout.setSpacing(0)

        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("Enter Your Email Here")

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Enter Your Password Here")
        self.login_password.setEchoMode(QLineEdit.Password)

        self.password_status = QLabel("Incorrect email or password!!")
        self.password_status.setStyleSheet("color: red; font-size: 11px;")
        self.password_status.setFrameShape(QLabel.NoFrame)
        self.password_status.setWordWrap(True)
        self.password_status.setVisible(False)

        self.login_rememberme = QCheckBox("Remember Me?")

        self.loginbutton = QPushButton("Click here to Login")
        self.loginbutton.clicked.connect(self.login_is_clicked)         

        layout.addWidget(self.login_email)
        layout.addSpacing(20)                
        layout.addWidget(self.login_password)
        layout.addSpacing(5)
        layout.addWidget(self.password_status)

        layout.addSpacing(15)                
        layout.addWidget(self.login_rememberme)
        layout.addSpacing(6)                 
        layout.addWidget(self.loginbutton)

        main_layout.addWidget(form_widget, alignment=Qt.AlignCenter)
        page.setLayout(main_layout)
        return page

    def logout_user(self):
        self.is_logged_in = False
        print("User is now logged out!")

        self.password_status.setVisible(False)

        self.login_email.clear()
        self.login_password.clear()
        self.login_rememberme.setChecked(False)

        self.logged_out_label.setVisible(True)
        self.logged_in_label.setVisible(False)
        self.btn_login.setVisible(True)
        self.btn_logout.setVisible(False)
        
        self.stacked_widget.setCurrentIndex(0)

    def login_is_clicked(self):
        email_text = self.login_email.text()
        if not (email_text.endswith("@gmail.com") or email_text.endswith("@hotmail.com") or email_text.endswith("@outlook.com")):
            self.password_status.setVisible(True)
            return  

        self.is_logged_in = True
        self.password_status.setVisible(False)
        print("User is now logged in!")

        if self.login_rememberme.isChecked():
            self.settings.setValue("email", self.login_email.text())
            self.settings.setValue("password", self.login_password.text())
            self.settings.setValue("remember", True)
        else:
            self.settings.remove("email")
            self.settings.remove("password")
            self.settings.remove("remember")
        
        self.logged_in_label.setVisible(True)
        self.logged_out_label.setVisible(False)     
        self.btn_login.setVisible(False)
        self.btn_logout.setVisible(True)
        self.stacked_widget.setCurrentIndex(0) 

    def load_remembered_credentials(self):
        is_remembered = self.settings.value("remember", False, type=bool)
        
        if is_remembered:
            saved_email = self.settings.value("email", "")
            saved_password = self.settings.value("password", "")
            
            self.login_email.setText(saved_email)
            self.login_password.setText(saved_password)
            self.login_rememberme.setChecked(True)

    def create_Store1(self):
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("This is the First Store Page")
        layout.addWidget(label)
        page.setLayout(layout)
        return page
            
    def go_to_next_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_previous_page(self):
        self.stacked_widget.setCurrentIndex(0)
    
    def go_to_store1(self):
        self.stacked_widget.setCurrentIndex(2)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())