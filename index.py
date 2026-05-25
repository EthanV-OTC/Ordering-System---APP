from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shitty lil Uber-Eats ahh ordering sustem")
        self.resize(1920,1080)
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

    def setup_navbar(self):
        self.btn_login = QPushButton("Login")
        btn_home = QPushButton("Home")
        btn_store = QPushButton("Store 1")

        self.btn_login.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        btn_store.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        self.navbar.addWidget(self.btn_login)
        self.navbar.addWidget(btn_home)
        self.navbar.addWidget(btn_store)
        self.navbar.addStretch()

    def create_Home(self):
        page = QWidget()
        layout = QVBoxLayout()
        
        self.logged_in_label = QLabel("The user is logged in")
        self.logged_in_label.setVisible(False) 

        label = QLabel("This is the Home Page")
        layout.addWidget(label)
        layout.addWidget(self.logged_in_label) 

        page.setLayout(layout)
        return page

    def create_Login(self):
        page = QWidget()
        layout = QVBoxLayout()
        self.loginbutton = QPushButton("Click here to Login")
        self.loginbutton.clicked.connect(self.login_is_clicked) 
        layout.addWidget(self.loginbutton)

        label = QLabel("This is the Second Page")
        layout.addWidget(label)
        
        page.setLayout(layout)
        return page

    def login_is_clicked(self):
        self.is_logged_in = True
        print("User is now logged in!")
        
        self.logged_in_label.setVisible(True)     
        self.btn_login.setVisible(False)
        self.stacked_widget.setCurrentIndex(0) 

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