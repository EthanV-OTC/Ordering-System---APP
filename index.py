from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QCheckBox, QDialog, QListWidget
from PyQt5.QtCore import Qt, QSettings, pyqtSignal
from PyQt5.QtGui import QPixmap
import sys, os

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()

class FoodPopup(QDialog):
    def __init__(self, item_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add to Order")
        self.resize(300, 120)
        
        layout = QVBoxLayout()
        
        self.ordermessage = QLabel(f"Would you like to add a {item_name} to your list?")
        layout.addWidget(self.ordermessage)
        
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add to List")
        self.add_btn.clicked.connect(self.accept) 
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.reject) 
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

class MealPopup(QDialog):
    def __init__(self, item_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Make it a Meal?")
        self.resize(300, 120)

        layout = QVBoxLayout()

        self.mealmessage = QLabel(f"Would you like to make your {item_name} become a meal for an extra $5?")
        layout.addWidget(self.mealmessage)

        button_layout = QHBoxLayout()

        self.meal_btn = QPushButton("Make it a meal! (+$5 to your order)")
        self.meal_btn.clicked.connect(self.accept)

        self.close_btn = QPushButton("No, keep it an item.")
        self.close_btn.clicked.connect(self.reject)

        button_layout.addWidget(self.meal_btn)
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rando lil Uber-Eats ahh ordering sustem")
        self.resize(1920,1080)

        self.settings = QSettings("Company", "UberEatsClone")
        self.checkout_list = QListWidget()

        try:
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("style.qss not found, skipping...")

        self.is_logged_in = False
        self.MAIN_MEALS = ["big mac", "whopper", "bacon backfire", "pepperoni pizza (dominoes)", "pepperoni pizza (pizzahut)", "pepperoni pizza (pizzagods)", "medium chicken bucket", "meatball sub"]

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
        self.Register = self.create_Register()
        self.burgers = self.create_burgers()
        self.pizza = self.create_pizza()
        self.chicken = self.create_chicken()
        self.sandwich = self.create_sandwich()
        self.checkout = self.create_checkout()
        
        self.stacked_widget.addWidget(self.Home)
        self.stacked_widget.addWidget(self.Login)
        self.stacked_widget.addWidget(self.burgers)
        self.stacked_widget.addWidget(self.Register)
        self.stacked_widget.addWidget(self.pizza)
        self.stacked_widget.addWidget(self.chicken)
        self.stacked_widget.addWidget(self.sandwich)
        self.stacked_widget.addWidget(self.checkout)


        self.mcdonalds = self.create_mcdonalds()
        self.burgerking = self.create_burgerking()
        self.burgerfuel = self.create_burgerfuel()
        self.dominoes = self.create_dominoes()
        self.pizzahut = self.create_pizzahut()
        self.pizzagods = self.create_pizzagods()
        self.kfc = self.create_kfc()
        self.subway = self.create_subway()
        self.sale = self.create_sale()

        self.stacked_widget.addWidget(self.mcdonalds)
        self.stacked_widget.addWidget(self.burgerking)
        self.stacked_widget.addWidget(self.burgerfuel)
        self.stacked_widget.addWidget(self.dominoes)
        self.stacked_widget.addWidget(self.pizzahut)
        self.stacked_widget.addWidget(self.pizzagods)
        self.stacked_widget.addWidget(self.kfc)
        self.stacked_widget.addWidget(self.subway)
        self.stacked_widget.addWidget(self.sale)

        self.btn_logout.setVisible(False)
        self.btn_login.setVisible(True)

        self.load_remembered_credentials()

    def setup_navbar(self):
        self.btn_login = QPushButton("Login")
        self.btn_logout = QPushButton("Logout")
        btn_home = QPushButton("Home")
        btn_burgers = QPushButton("Burgers")
        btn_pizza = QPushButton("Pizza")
        btn_chicken = QPushButton("Chicken")
        btn_sandwich = QPushButton("Sandwiches")
        self.btn_checkout = QPushButton("Checkout")

        self.btn_login.setObjectName("btn_login")
        self.btn_logout.setObjectName("btn_logout")
        self.btn_checkout.setObjectName("btn_checkout")

        self.btn_login.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Login))
        btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        btn_burgers.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.burgers))
        btn_pizza.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.pizza))
        btn_chicken.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.chicken))
        btn_sandwich.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.sandwich))
        self.btn_checkout.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.checkout))


        self.btn_logout.clicked.connect(self.logout_user)

        self.navbar.addWidget(self.btn_login)
        self.navbar.addWidget(self.btn_logout)
        self.navbar.addWidget(btn_home)
        self.navbar.addWidget(btn_burgers)
        self.navbar.addWidget(btn_pizza)
        self.navbar.addWidget(btn_chicken)
        self.navbar.addWidget(btn_sandwich)
        self.navbar.addStretch()
        self.navbar.addWidget(self.btn_checkout)
        self.navbar.addSpacing(25)

    def create_Home(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # --- McDonald's Logo ---
        McDonaldspath = os.path.join(base_path, "images", "McDonalds-logo.png")
        McDonaldslogo = QPixmap(McDonaldspath)
        self.McDonaldslabel = ClickableLabel()  

        if McDonaldslogo.isNull():
            print(f"Failed to load image at: {McDonaldspath}")
        else:
            self.McDonaldslabel.setPixmap(McDonaldslogo)
            self.McDonaldslabel.setScaledContents(True)        
        self.McDonaldslabel.setFixedSize(250, 250)

        self.McDonaldslabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.mcdonalds))

        # --- Burger King Logo ---
        BKpath = os.path.join(base_path, "images", "BK-logo.png")
        BKlogo = QPixmap(BKpath)
        self.Bklabel = ClickableLabel()

        if BKlogo.isNull():
            print(f"Failed to load image at: {BKpath}")
        else:
            self.Bklabel.setPixmap(BKlogo)
            self.Bklabel.setScaledContents(True)
        self.Bklabel.setFixedSize(250, 250)

        self.Bklabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.burgerking))

        # --- BurgerFuel Logo ---
        burgerfuelpath = os.path.join(base_path, "images", "BurgerFuel-logo.png")
        burgerfuellogo = QPixmap(burgerfuelpath)
        self.burgerfuellabel = ClickableLabel()

        if burgerfuellogo.isNull():
            print(f"Failed to load image at {burgerfuelpath}")
        else:
            self.burgerfuellabel.setPixmap(burgerfuellogo)
            self.burgerfuellabel.setScaledContents(True)
        self.burgerfuellabel.setFixedSize(250, 250)

        self.burgerfuellabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.burgerfuel))

        # --- Dominoes Logo ---
        dominoespath = os.path.join(base_path, "images", "Dominoes-logo.png")
        dominoeslogo = QPixmap(dominoespath)
        self.dominoeslabel = ClickableLabel()

        if dominoeslogo.isNull():
            print(f"Failed to load image at {dominoespath}")
        else:
            self.dominoeslabel.setPixmap(dominoeslogo)
            self.dominoeslabel.setScaledContents(True)
        self.dominoeslabel.setFixedSize(250, 250)

        self.dominoeslabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.dominoes))

        # --- PizzaHut Logo ---
        pizzahutpath = os.path.join(base_path, "images", "PizzaHut-logo.png")
        pizzahutlogo = QPixmap(pizzahutpath)
        self.pizzahutlabel = ClickableLabel()

        if pizzahutlogo.isNull():
            print(f"Failed to load image at {pizzahutpath}")
        else:
            self.pizzahutlabel.setPixmap(pizzahutlogo)
            self.pizzahutlabel.setScaledContents(True)
        self.pizzahutlabel.setFixedSize(250, 250)

        self.pizzahutlabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.pizzahut))

        # --- Pizza Gods Logo ---
        pizzagodspath = os.path.join(base_path, "images", "PizzaGods-logo.png")
        pizzagodslogo = QPixmap(pizzagodspath)
        self.pizzagodslabel = ClickableLabel()

        if pizzagodslogo.isNull():
            print(f"Failed to load image at {pizzagodspath}")
        else:
            self.pizzagodslabel.setPixmap(pizzagodslogo)
            self.pizzagodslabel.setScaledContents(True)
        self.pizzagodslabel.setFixedSize(250, 250)

        self.pizzagodslabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.pizzagods))

        # --- KFC Logo ---
        kfcpath = os.path.join(base_path, "images", "KFC-logo.png")
        kfclogo = QPixmap(kfcpath)
        self.kfclabel = ClickableLabel()

        if kfclogo.isNull():
            print(f"Failed to load image at {kfcpath}")
        else:
            self.kfclabel.setPixmap(kfclogo)
            self.kfclabel.setScaledContents(True)
        self.kfclabel.setFixedSize(250, 250)

        self.kfclabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.kfc))

        # --- Subway Logo ---
        subwaypath = os.path.join(base_path, "images", "Subway-logo.png")
        subwaylogo = QPixmap(subwaypath)
        self.subwaylabel = ClickableLabel()

        if subwaylogo.isNull():
            print(f"Failed to load image at {subwaypath}")
        else:
            self.subwaylabel.setPixmap(subwaylogo)
            self.subwaylabel.setScaledContents(True)
        self.subwaylabel.setFixedSize(250, 250)

        self.subwaylabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.subway))

        # --- Sale Logo ---
        salepath = os.path.join(base_path, "images", "Sale-logo.png")
        salelogo = QPixmap(salepath)
        self.salelabel = ClickableLabel()

        if salelogo.isNull():
            print(f"Failed to load image at {salepath}")
        else:
            self.salelabel.setPixmap(salelogo)
            self.salelabel.setScaledContents(True)
        self.salelabel.setFixedSize(250, 250)

        self.salelabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.sale))

        # Row 1
        layout.addWidget(self.McDonaldslabel, 0, 0)
        layout.addWidget(self.Bklabel, 0, 1)
        layout.addWidget(self.burgerfuellabel, 0, 2)
        
        # Row 2
        layout.addWidget(self.dominoeslabel, 1, 0)
        layout.addWidget(self.pizzahutlabel, 1, 1)
        layout.addWidget(self.pizzagodslabel, 1, 2)

        # Row 3
        layout.addWidget(self.kfclabel, 2, 0)
        layout.addWidget(self.salelabel, 2, 1)
        layout.addWidget(self.subwaylabel, 2 ,2)

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

        self.registerpage_button = QPushButton("Haven't logged in before? Register Here!!")
        self.registerpage_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

        layout.addWidget(self.login_email)
        layout.addSpacing(20)                
        layout.addWidget(self.login_password)
        layout.addSpacing(5)
        layout.addWidget(self.password_status)

        layout.addSpacing(15)                
        layout.addWidget(self.login_rememberme)
        layout.addSpacing(6)                 
        layout.addWidget(self.loginbutton)
        layout.addSpacing(10)
        layout.addWidget(self.registerpage_button)

        main_layout.addWidget(form_widget, alignment=Qt.AlignCenter)
        page.setLayout(main_layout)
        return page

    def create_Register(self):
        page = QWidget()
        main_layout = QVBoxLayout()

        form_widget = QWidget()
        form_widget.setFixedWidth(400)
        layout = QVBoxLayout(form_widget)
        layout.setSpacing(0)

        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("Enter your Email here!")

        self.register_pass = QLineEdit()
        self.register_pass.setPlaceholderText("Enter your Password here!")

        self.register_status = QLabel("Invalid Email!! Please enter one with an '@_____.com' to proceed!!")
        self.register_status.setStyleSheet("color: red; font-size: 11px;")
        self.register_status.setFrameShape(QLabel.NoFrame)
        self.register_status.setWordWrap(True)
        self.register_status.setVisible(False)

        self.register_btn = QPushButton('Click here to Register!')
        self.register_btn.clicked.connect(self.register_is_clicked)

        layout.addWidget(self.register_email)
        layout.addSpacing(10)
        layout.addWidget(self.register_pass)
        layout.addSpacing(6)
        layout.addWidget(self.register_status)
        layout.addSpacing(12)
        layout.addWidget(self.register_btn)

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

        self.btn_login.setVisible(True)
        self.btn_logout.setVisible(False)
        
        self.stacked_widget.setCurrentIndex(0)

    def register_is_clicked(self):
        self.email = self.register_email.text()
        self.password = self.register_pass.text()        
        
        if not (self.email.endswith("@gmail.com") or self.email.endswith("@hotmail.com") or self.email.endswith("@outlook.com")):
            self.register_status.setVisible(True)
            return  
        self.stacked_widget.setCurrentIndex(1)

    def login_is_clicked(self):
        input_email = self.login_email.text()
        input_password = self.login_password.text()

        if not hasattr(self, 'email') or not hasattr(self, 'password'):
            self.password_status.setText("No account found! Please register first.")
            self.password_status.setVisible(True)
            return

        if input_email != self.email or input_password != self.password:
            self.password_status.setText("Incorrect email or password!!")
            self.password_status.setVisible(True)
            return

        self.is_logged_in = True
        self.password_status.setVisible(False)
        print("User is now logged in!")

        if self.login_rememberme.isChecked():
            self.settings.setValue("email", input_email)
            self.settings.setValue("password", input_password)
            self.settings.setValue("remember", True)
        else:
            self.settings.remove("email")
            self.settings.remove("password")
            self.settings.remove("remember")
         
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
            self.email = (saved_email)
            self.password = (saved_password)


    def create_burgers(self):
        page = QWidget()
        
        main_outer_layout = QVBoxLayout()
        page.setLayout(main_outer_layout)

        header_layout = QHBoxLayout()
        
        self.burgers_back_button = QPushButton("← Go Home")
        self.burgers_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        self.burgers_back_button.setFixedWidth(100) 
        
        header_layout.addWidget(self.burgers_back_button)
        header_layout.addStretch()
        
        main_outer_layout.addLayout(header_layout)

        layout = QGridLayout()

        base_path = os.path.dirname(os.path.abspath(__file__))

        # --- McDonald's Logo ---
        McDonaldspath = os.path.join(base_path, "images", "McDonalds-logo.png")
        McDonaldslogo = QPixmap(McDonaldspath)
        self.McDonaldslabel = ClickableLabel()  

        if McDonaldslogo.isNull():
            print(f"Failed to load image at: {McDonaldspath}")
        else:
            self.McDonaldslabel.setPixmap(McDonaldslogo)
            self.McDonaldslabel.setScaledContents(True)        
        self.McDonaldslabel.setFixedSize(250, 250)

        self.McDonaldslabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.mcdonalds))

        # --- Burger King Logo ---
        BKpath = os.path.join(base_path, "images", "BK-logo.png")
        BKlogo = QPixmap(BKpath)
        self.Bklabel = ClickableLabel()

        if BKlogo.isNull():
            print(f"Failed to load image at: {BKpath}")
        else:
            self.Bklabel.setPixmap(BKlogo)
            self.Bklabel.setScaledContents(True)
        self.Bklabel.setFixedSize(250, 250)

        self.Bklabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.burgerking))

        # --- BurgerFuel Logo ---
        burgerfuelpath = os.path.join(base_path, "images", "BurgerFuel-logo.png")
        burgerfuellogo = QPixmap(burgerfuelpath)
        self.burgerfuellabel = ClickableLabel()

        if burgerfuellogo.isNull():
            print(f"Failed to load image at {burgerfuelpath}")
        else:
            self.burgerfuellabel.setPixmap(burgerfuellogo)
            self.burgerfuellabel.setScaledContents(True)
        self.burgerfuellabel.setFixedSize(250, 250)

        self.burgerfuellabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.burgerfuel))

        layout.addWidget(self.McDonaldslabel, 0, 0)
        layout.addWidget(self.Bklabel, 0, 1)
        layout.addWidget(self.burgerfuellabel, 0, 2)
        
        main_outer_layout.addLayout(layout)
        
        return page


    def create_pizza(self):
        page = QWidget()
        
        main_outer_layout = QVBoxLayout()
        page.setLayout(main_outer_layout)

        header_layout = QHBoxLayout()
        
        self.pizza_cat_back_button = QPushButton("← Go Home")
        self.pizza_cat_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        self.pizza_cat_back_button.setFixedWidth(100) 
        
        header_layout.addWidget(self.pizza_cat_back_button)
        header_layout.addStretch()
        
        main_outer_layout.addLayout(header_layout)

        layout = QGridLayout()

        base_path = os.path.dirname(os.path.abspath(__file__))

        # --- Dominoes Logo ---
        dominoespath = os.path.join(base_path, "images", "Dominoes-logo.png")
        dominoeslogo = QPixmap(dominoespath)
        self.dominoeslabel = ClickableLabel()

        if dominoeslogo.isNull():
            print(f"Failed to load image at {dominoespath}")
        else:
            self.dominoeslabel.setPixmap(dominoeslogo)
            self.dominoeslabel.setScaledContents(True)
        self.dominoeslabel.setFixedSize(250, 250)

        self.dominoeslabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.dominoes))

        # --- PizzaHut Logo ---
        pizzahutpath = os.path.join(base_path, "images", "PizzaHut-logo.png")
        pizzahutlogo = QPixmap(pizzahutpath)
        self.pizzahutlabel = ClickableLabel()

        if pizzahutlogo.isNull():
            print(f"Failed to load image at {pizzahutpath}")
        else:
            self.pizzahutlabel.setPixmap(pizzahutlogo)
            self.pizzahutlabel.setScaledContents(True)
        self.pizzahutlabel.setFixedSize(250, 250)

        self.pizzahutlabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.pizzahut))

        # --- Pizza Gods Logo ---
        pizzagodspath = os.path.join(base_path, "images", "PizzaGods-logo.png")
        pizzagodslogo = QPixmap(pizzagodspath)
        self.pizzagodslabel = ClickableLabel()

        if pizzagodslogo.isNull():
            print(f"Failed to load image at {pizzagodspath}")
        else:
            self.pizzagodslabel.setPixmap(pizzagodslogo)
            self.pizzagodslabel.setScaledContents(True)
        self.pizzagodslabel.setFixedSize(250, 250)

        self.pizzagodslabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.pizzagods))

        layout.addWidget(self.dominoeslabel, 0, 0)
        layout.addWidget(self.pizzahutlabel, 0, 1)
        layout.addWidget(self.pizzagodslabel, 0, 2)
        
        main_outer_layout.addLayout(layout)
        
        return page


    def create_chicken(self):
        page = QWidget()
        
        main_outer_layout = QVBoxLayout()
        page.setLayout(main_outer_layout)

        header_layout = QHBoxLayout()
        
        self.chicken_cat_back_button = QPushButton("← Go Home")
        self.chicken_cat_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        self.chicken_cat_back_button.setFixedWidth(100) 
        
        header_layout.addWidget(self.chicken_cat_back_button)
        header_layout.addStretch()
        
        main_outer_layout.addLayout(header_layout)

        layout = QGridLayout()

        base_path = os.path.dirname(os.path.abspath(__file__))

        # --- KFC Logo ---
        kfcpath = os.path.join(base_path, "images", "KFC-logo.png")
        kfclogo = QPixmap(kfcpath)
        self.kfclabel = ClickableLabel()

        if kfclogo.isNull():
            print(f"Failed to load image at {kfcpath}")
        else:
            self.kfclabel.setPixmap(kfclogo)
            self.kfclabel.setScaledContents(True)
        self.kfclabel.setFixedSize(250, 250)

        self.kfclabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.kfc))

        layout.addWidget(self.kfclabel, 0, 0)
        
        main_outer_layout.addLayout(layout)
        
        return page


    def create_sandwich(self):
        page = QWidget()
        
        main_outer_layout = QVBoxLayout()
        page.setLayout(main_outer_layout)

        header_layout = QHBoxLayout()
        
        self.sandwich_cat_back_button = QPushButton("← Go Home")
        self.sandwich_cat_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        self.sandwich_cat_back_button.setFixedWidth(100) 
        
        header_layout.addWidget(self.sandwich_cat_back_button)
        header_layout.addStretch()
        
        main_outer_layout.addLayout(header_layout)

        layout = QGridLayout()

        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # --- Subway Logo ---
        subwaypath = os.path.join(base_path, "images", "Subway-logo.png")
        subwaylogo = QPixmap(subwaypath)
        self.subwaylabel = ClickableLabel()

        if subwaylogo.isNull():
            print(f"Failed to load image at {subwaypath}")
        else:
            self.subwaylabel.setPixmap(subwaylogo)
            self.subwaylabel.setScaledContents(True)
        self.subwaylabel.setFixedSize(250, 250)

        self.subwaylabel.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.subway))

        layout.addWidget(self.subwaylabel, 0, 0)
        
        main_outer_layout.addLayout(layout)
        
        return page

    


    def create_mcdonalds(self):
        page = QWidget()
        
        main_outer_layout = QVBoxLayout()
        page.setLayout(main_outer_layout)

        header_layout = QHBoxLayout()
        
        self.mcdonalds_back_button = QPushButton("← Go Home")
        self.mcdonalds_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        self.mcdonalds_back_button.setFixedWidth(100) 
        
        header_layout.addWidget(self.mcdonalds_back_button)
        header_layout.addStretch()
        
        main_outer_layout.addLayout(header_layout)

        layout = QGridLayout()

        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # --- Big Mac Item ---
        bmprice = f"- $10.50"
        bmdisplay_text = f"Big Mac {bmprice}"
        bm_itemname = "Big Mac"

        bigmac_container = QWidget()
        bm_box = QVBoxLayout(bigmac_container)
        bm_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bigmacpath = os.path.join(base_path, "images", "BigMac.png")
        bigmacphoto = QPixmap(bigmacpath)
        self.bigmaclabel = ClickableLabel()  

        if bigmacphoto.isNull():
            print(f"Failed to load image at: {bigmacpath}")
        else:
            self.bigmaclabel.setPixmap(bigmacphoto)
            self.bigmaclabel.setScaledContents(True)        
        self.bigmaclabel.setFixedSize(250, 250)

        self.bigmac_text_label = QLabel(bmdisplay_text)
        self.bigmac_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bigmac_text_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")


        self.bigmaclabel.clicked.connect(lambda checked=False, name=bm_itemname: self.handle_food_click(name))

        bm_box.addWidget(self.bigmaclabel)
        bm_box.addWidget(self.bigmac_text_label)

        # --- Fries Item ---
        fprice = f"- $4.50"
        fdisplay_text = f"McDonalds Fries {fprice}"
        f_itemname = "McDonalds Fries"

        fries_container = QWidget()
        f_box = QVBoxLayout(fries_container)
        f_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        fpath = os.path.join(base_path, "images", "McFries.png")
        fphoto = QPixmap(fpath)
        self.mcflabel = ClickableLabel()  

        if fphoto.isNull():
            print(f"Failed to load image at: {fpath}")
        else:
            self.mcflabel.setPixmap(fphoto)
            self.mcflabel.setScaledContents(True)        
        self.mcflabel.setFixedSize(250, 250)

        self.mcf_text_label = QLabel(fdisplay_text)
        self.mcf_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mcf_text_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")

        self.mcflabel.clicked.connect(lambda checked=False, name=f_itemname: self.handle_food_click(name))

        f_box.addWidget(self.mcflabel)
        f_box.addWidget(self.mcf_text_label)

        layout.addWidget(bigmac_container, 0, 0) 
        layout.addWidget(fries_container, 0, 1)
        
        main_outer_layout.addLayout(layout)
        main_outer_layout.addStretch()
        
        return page

    def create_burgerking(self):
        page = QWidget()
        
        main_outer_layout = QVBoxLayout()
        page.setLayout(main_outer_layout)

        header_layout = QHBoxLayout()
        
        self.burgerking_back_button = QPushButton("← Go Home")
        self.burgerking_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        self.burgerking_back_button.setFixedWidth(100) 
        
        header_layout.addWidget(self.burgerking_back_button)
        header_layout.addStretch()
        
        main_outer_layout.addLayout(header_layout)

        layout = QGridLayout()

        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # --- Whopper Item ---
        wprice = f"- 12.00"
        wdisplay_text = f"Whopper {wprice}"
        w_itemname = "Whopper"

        whopper_container = QWidget()
        bkw_box = QVBoxLayout(whopper_container)
        bkw_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        whopperpath = os.path.join(base_path, "images", "Whopper.png")
        whopperphoto = QPixmap(whopperpath)
        self.whopperlabel = ClickableLabel()  

        if whopperphoto.isNull():
            print(f"Failed to load image at: {whopperpath}")
        else:
            self.whopperlabel.setPixmap(whopperphoto)
            self.whopperlabel.setScaledContents(True)        
        self.whopperlabel.setFixedSize(250, 250)

        self.whopper_text_label = QLabel(wdisplay_text)
        self.whopper_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.whopper_text_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")

        self.whopperlabel.clicked.connect(lambda checked=False, name=w_itemname: self.handle_food_click(name))

        bkw_box.addWidget(self.whopperlabel)
        bkw_box.addWidget(self.whopper_text_label)

        # --- Fries Item ---
        fprice = f"- $5.50"
        fdisplay_text = f"BK Fries {fprice}"
        f_itemname = "Bk Fries"

        fries_container = QWidget()
        f_box = QVBoxLayout(fries_container)
        f_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        fpath = os.path.join(base_path, "images", "BkFries.png")
        fphoto = QPixmap(fpath)
        self.bkflabel = ClickableLabel()  

        if fphoto.isNull():
            print(f"Failed to load image at: {fpath}")
        else:
            self.bkflabel.setPixmap(fphoto)
            self.bkflabel.setScaledContents(True)        
        self.bkflabel.setFixedSize(250, 250)

        self.bkf_text_label = QLabel(fdisplay_text)
        self.bkf_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bkf_text_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")

        self.bkflabel.clicked.connect(lambda checked=False, name=f_itemname: self.handle_food_click(name))

        f_box.addWidget(self.bkflabel)
        f_box.addWidget(self.bkf_text_label)

        layout.addWidget(whopper_container, 0, 0)  
        layout.addWidget(fries_container, 0, 1)
        
        main_outer_layout.addLayout(layout)
        main_outer_layout.addStretch()
        
        return page



    def create_burgerfuel(self):
        page = QWidget()
        
        main_outer_layout = QVBoxLayout()
        page.setLayout(main_outer_layout)

        header_layout = QHBoxLayout()
        
        self.burgerfuel_back_button = QPushButton("← Go Home")
        self.burgerfuel_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        self.burgerfuel_back_button.setFixedWidth(100) 
        
        header_layout.addWidget(self.burgerfuel_back_button)
        header_layout.addStretch()
        
        main_outer_layout.addLayout(header_layout)

        layout = QGridLayout()

        base_path = os.path.dirname(os.path.abspath(__file__))
        price = f"- $25.00"
        display_text = f"Bacon Backfire {price}"
        itemname = "Bacon Backfire"

        baconbackfire_container = QWidget()
        v_box = QVBoxLayout(baconbackfire_container)
        v_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        baconbackfirepath = os.path.join(base_path, "images", "BaconBackfire.png")
        baconbackfirephoto = QPixmap(baconbackfirepath)
        self.baconbackfirelabel = ClickableLabel()  

        if baconbackfirephoto.isNull():
            print(f"Failed to load image at: {baconbackfirepath}")
        else:
            self.baconbackfirelabel.setPixmap(baconbackfirephoto)
            self.baconbackfirelabel.setScaledContents(True)        
        self.baconbackfirelabel.setFixedSize(250, 250)

        self.baconbackfire_text_label = QLabel(display_text)
        self.baconbackfire_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.baconbackfire_text_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")

        self.baconbackfirelabel.clicked.connect(lambda: self.handle_food_click(itemname))

        v_box.addWidget(self.baconbackfirelabel)
        v_box.addWidget(self.baconbackfire_text_label)

        # --- Fries Item ---
        fprice = f"- $10"
        fdisplay_text = f"BurgerFuel Fries {fprice}"
        f_itemname = "BurgerFuel Fries"

        fries_container = QWidget()
        f_box = QVBoxLayout(fries_container)
        f_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        fpath = os.path.join(base_path, "images", "BkFries.png")
        fphoto = QPixmap(fpath)
        self.bfflabel = ClickableLabel()  

        if fphoto.isNull():
            print(f"Failed to load image at: {fpath}")
        else:
            self.bfflabel.setPixmap(fphoto)
            self.bfflabel.setScaledContents(True)        
        self.bfflabel.setFixedSize(250, 250)

        self.bff_text_label = QLabel(fdisplay_text)
        self.bff_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bff_text_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")

        self.bfflabel.clicked.connect(lambda checked=False, name=f_itemname: self.handle_food_click(name))

        f_box.addWidget(self.bfflabel)
        f_box.addWidget(self.bff_text_label)

        layout.addWidget(baconbackfire_container, 0, 0) 
        layout.addWidget()
        
        main_outer_layout.addLayout(layout)
        
        return page
        
    def create_dominoes(self):
        page = QWidget()
        
        main_outer_layout = QVBoxLayout()
        page.setLayout(main_outer_layout)

        header_layout = QHBoxLayout()
        
        self.dominoes_back_button = QPushButton("← Go Home")
        self.dominoes_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        self.dominoes_back_button.setFixedWidth(100) 
        
        header_layout.addWidget(self.dominoes_back_button)
        header_layout.addStretch()
        
        main_outer_layout.addLayout(header_layout)

        layout = QGridLayout()

        base_path = os.path.dirname(os.path.abspath(__file__))
        price = f"- $15.00"
        display_text = f"Pepperoni Pizza (Dominoes) {price}"
        itemname = "Pepperoni Pizza - (Dominoes)"

        Dpepperoni_container = QWidget()
        v_box = QVBoxLayout(Dpepperoni_container)
        v_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        Dpepperonipath = os.path.join(base_path, "images", "DPepperoniPizza.png")
        Dpepperoniphoto = QPixmap(Dpepperonipath)   
        self.Dpepperonilabel = ClickableLabel()  

        if Dpepperoniphoto.isNull():
            print(f"Failed to load image at: {Dpepperonipath}")
        else:
            self.Dpepperonilabel.setPixmap(Dpepperoniphoto)
            self.Dpepperonilabel.setScaledContents(True)        
        self.Dpepperonilabel.setFixedSize(250, 250)

        self.Dpepperon_text_label = QLabel(display_text)
        self.Dpepperon_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Dpepperon_text_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")

        self.Dpepperonilabel.clicked.connect(lambda: self.handle_food_click(itemname))

        v_box.addWidget(self.Dpepperonilabel)
        v_box.addWidget(self.Dpepperon_text_label)

        layout.addWidget(Dpepperoni_container, 0, 0) 
        
        main_outer_layout.addLayout(layout)
        
        return page

                
    def create_pizzahut(self):
        page = QWidget()
        
        main_outer_layout = QVBoxLayout()
        page.setLayout(main_outer_layout)

        header_layout = QHBoxLayout()
        
        self.p_pizza_back_button = QPushButton("← Go Home")
        self.p_pizza_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        self.p_pizza_back_button.setFixedWidth(100) 
        
        header_layout.addWidget(self.p_pizza_back_button)
        header_layout.addStretch()
        
        main_outer_layout.addLayout(header_layout)

        layout = QGridLayout()

        base_path = os.path.dirname(os.path.abspath(__file__))
        price = f"- $15.00"
        display_text = f"Pepperoni Pizza (pizzahut) {price}"
        itemname = "Pepperoni Pizza (PizzaHut)"

        Ppepperoni_container = QWidget()
        v_box = QVBoxLayout(Ppepperoni_container)
        v_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        Ppepperonipath = os.path.join(base_path, "images", "PPepperoniPizza.png")
        Ppepperoniphoto = QPixmap(Ppepperonipath)
        self.Ppepperonilabel = ClickableLabel()  

        if Ppepperoniphoto.isNull():
            print(f"Failed to load image at: {Ppepperonipath}")
        else:
            self.Ppepperonilabel.setPixmap(Ppepperoniphoto)
            self.Ppepperonilabel.setScaledContents(True)        
        self.Ppepperonilabel.setFixedSize(250, 250)

        self.Ppepperon_text_label = QLabel(display_text)
        self.Ppepperon_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Ppepperon_text_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")

        self.Ppepperonilabel.clicked.connect(lambda: self.handle_food_click(itemname))

        v_box.addWidget(self.Ppepperonilabel)
        v_box.addWidget(self.Ppepperon_text_label)

        layout.addWidget(Ppepperoni_container, 0, 0) 
        
        main_outer_layout.addLayout(layout)
        
        return page


        
    def create_pizzagods(self):
        page = QWidget()
        
        main_outer_layout = QVBoxLayout()
        page.setLayout(main_outer_layout)

        header_layout = QHBoxLayout()
        
        self.pizza_back_button = QPushButton("← Go Home")
        self.pizza_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        self.pizza_back_button.setFixedWidth(100) 
        
        header_layout.addWidget(self.pizza_back_button)
        header_layout.addStretch()
        
        main_outer_layout.addLayout(header_layout)

        layout = QGridLayout()

        base_path = os.path.dirname(os.path.abspath(__file__))
        price = f"- $12.00"
        display_text = f"Pepperoni Pizza (pizzagods) {price}"
        itemname = "Pepperoni Pizza (PizzaGods)"

        Gpepperoni_container = QWidget()
        v_box = QVBoxLayout(Gpepperoni_container)
        v_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        Gpepperonipath = os.path.join(base_path, "images", "GPepperoniPizza.png")
        Gpepperoniphoto = QPixmap(Gpepperonipath)
        self.Gpepperonilabel = ClickableLabel()  

        if Gpepperoniphoto.isNull():
            print(f"Failed to load image at: {Gpepperonipath}")
        else:
            self.Gpepperonilabel.setPixmap(Gpepperoniphoto)
            self.Gpepperonilabel.setScaledContents(True)        
        self.Gpepperonilabel.setFixedSize(250, 250)

        self.Gpepperon_text_label = QLabel(display_text)
        self.Gpepperon_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Gpepperon_text_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")

        self.Gpepperonilabel.clicked.connect(lambda: self.handle_food_click(itemname))

        v_box.addWidget(self.Gpepperonilabel)
        v_box.addWidget(self.Gpepperon_text_label)

        layout.addWidget(Gpepperoni_container, 0, 0) 
        
        main_outer_layout.addLayout(layout)
        
        return page


        
    def create_kfc(self):
        page = QWidget()
        
        main_outer_layout = QVBoxLayout()
        page.setLayout(main_outer_layout)

        header_layout = QHBoxLayout()
        
        self.bucket_back_button = QPushButton("← Go Home")
        self.bucket_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        self.bucket_back_button.setFixedWidth(100) 
        
        header_layout.addWidget(self.bucket_back_button)
        header_layout.addStretch()
        
        main_outer_layout.addLayout(header_layout)

        layout = QGridLayout()

        base_path = os.path.dirname(os.path.abspath(__file__))
        price = f"- $25.00"
        display_text = f"Medium Chicken Bucket {price}"
        itemname = "Medium Chicken Bucket"

        bucketM_container = QWidget()
        v_box = QVBoxLayout(bucketM_container)
        v_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bucketMpath = os.path.join(base_path, "images", "BucketM.png")
        bucketMphoto = QPixmap(bucketMpath)
        self.bucketMlabel = ClickableLabel()  

        if bucketMphoto.isNull():
            print(f"Failed to load image at: {bucketMpath}")
        else:
            self.bucketMlabel.setPixmap(bucketMphoto)
            self.bucketMlabel.setScaledContents(True)        
        self.bucketMlabel.setFixedSize(250, 250)

        self.bucketM_text_label = QLabel(display_text)
        self.bucketM_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bucketM_text_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")

        self.bucketMlabel.clicked.connect(lambda: self.handle_food_click(itemname))

        v_box.addWidget(self.bucketMlabel)
        v_box.addWidget(self.bucketM_text_label)

        layout.addWidget(bucketM_container, 0, 0) 
        
        main_outer_layout.addLayout(layout)
        
        return page


        
    def create_subway(self):
        page = QWidget()
        
        main_outer_layout = QVBoxLayout()
        page.setLayout(main_outer_layout)

        header_layout = QHBoxLayout()
        
        self.subway_back_button = QPushButton("← Go Home")
        self.subway_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        self.subway_back_button.setFixedWidth(100) 
        
        header_layout.addWidget(self.subway_back_button)
        header_layout.addStretch()
        
        main_outer_layout.addLayout(header_layout)

        layout = QGridLayout()

        base_path = os.path.dirname(os.path.abspath(__file__))
        price = f"- $15"
        display_text = f"Meatball Sub {price}"
        itemname = "Meatball Sub"

        meatball_container = QWidget()
        v_box = QVBoxLayout(meatball_container)
        v_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        meatballpath = os.path.join(base_path, "images", "MeatBall.png")
        meatballphoto = QPixmap(meatballpath)
        self.meatballlabel = ClickableLabel()  

        if meatballphoto.isNull():
            print(f"Failed to load image at: {meatballpath}")
        else:
            self.meatballlabel.setPixmap(meatballphoto)
            self.meatballlabel.setScaledContents(True)        
        self.meatballlabel.setFixedSize(250, 250)

        self.meatball_text_label = QLabel(display_text)
        self.meatball_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.meatball_text_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")

        self.meatballlabel.clicked.connect(lambda: self.handle_food_click(itemname))

        v_box.addWidget(self.meatballlabel)
        v_box.addWidget(self.meatball_text_label)

        layout.addWidget(meatball_container, 0, 0) 
        
        main_outer_layout.addLayout(layout)
        
        return page
        
    def create_sale(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

        self.Label = QLabel("This is the Sales Page")

        layout.addWidget(self.Label)
        return page
        
    def handle_food_click(self, item_name):
        popup = FoodPopup(item_name, self)
        
        if popup.exec_() == QDialog.Accepted:
            self.checkout_list.addItem(f"Ordered: {item_name}") 
            
            if item_name.lower() in self.MAIN_MEALS:
                mealpopup = MealPopup(item_name, self)
                if mealpopup.exec_() == QDialog.Accepted:
                    print("Upgraded to a full combo meal! Adding $5.")
                    
                    last_row = self.checkout_list.count() - 1
                    last_item = self.checkout_list.item(last_row)
                    last_item.setText(f"Ordered: {item_name} - MEAL ({item_name} + Fries + Drink)")
                    
                    cart_text = "This is the checkout Page\n\n--- Current Cart Contents ---\n"
                    for row in range(self.checkout_list.count()):
                        item = self.checkout_list.item(row) 
                        cart_text += f"- {item.text()}\n"
                    cart_text += "-----------------------------"
                    self.checkout_label.setText(cart_text)
                    
                else:
                    print("User declined the meal upgrade.")
                    cart_text = "This is the Checkout Page\n\n--- Current Cart Contents ---\n"
                    for row in range(self.checkout_list.count()):
                        item = self.checkout_list.item(row)
                        cart_text += f"- {item.text()}\n" 
                    cart_text += "-----------------------------"                    
                    self.checkout_label.setText(cart_text)
            else:
                cart_text = "This is the Checkout Page\n\n--- Current Cart Contents ---\n"
                for row in range(self.checkout_list.count()):
                    item = self.checkout_list.item(row)
                    cart_text += f"- {item.text()}\n" 
                cart_text += "-----------------------------"                    
                self.checkout_label.setText(cart_text)


    def create_checkout(self):
        page = QWidget()
        
        main_outer_layout = QVBoxLayout()
        page.setLayout(main_outer_layout)

        header_layout = QHBoxLayout()
        
        self.checkout_back_button = QPushButton("← Go Home")
        self.checkout_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Home))
        self.checkout_back_button.setFixedWidth(100) 
        
        header_layout.addWidget(self.checkout_back_button)
        header_layout.addStretch()
        
        main_outer_layout.addLayout(header_layout)

        layout = QGridLayout()

        self.checkout_label = QLabel("This is the Checkout Page\n\nCart is empty.")
        self.checkout_label.setWordWrap(True)

        layout.addWidget(self.checkout_label)
        
        main_outer_layout.addLayout(layout)
        
        return page


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())