from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt, QSettings, pyqtSignal
from PyQt5.QtGui import QPixmap
import sys, os

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rando lil Uber-Eats ahh ordering sustem")
        self.resize(1920,1080)

        self.settings = QSettings("Company", "UberEatsClone")

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



        layout.addWidget(self.McDonaldslabel, 0, 0)
        layout.addWidget(self.Bklabel, 0, 1)
        layout.addWidget(self.burgerfuellabel, 0, 2)
        return page


    def create_pizza(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

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
        return page


    def create_chicken(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

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
        return page


    def create_sandwich(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

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
        return page
    


    def create_mcdonalds(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

        self.Label = QLabel("This is the Mcdonalds Store Page")

        layout.addWidget(self.Label)
        return page

    def create_burgerking(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

        self.Label = QLabel("This is the BugerKing Store Page")

        layout.addWidget(self.Label)
        return page

    def create_burgerfuel(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

        self.Label = QLabel("This is the BurgerFuel Store Page")

        layout.addWidget(self.Label)
        return page
        
    def create_dominoes(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

        self.Label = QLabel("This is the Dominoes Store Page")

        layout.addWidget(self.Label)
        return page
                
    def create_pizzahut(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

        self.Label = QLabel("This is the PizzaHut Store Page")

        layout.addWidget(self.Label)
        return page
        
    def create_pizzagods(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

        self.Label = QLabel("This is the PizzaGods Store Page")

        layout.addWidget(self.Label)
        return page
        
    def create_kfc(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

        self.Label = QLabel("This is the KFC Store Page")

        layout.addWidget(self.Label)
        return page
        
    def create_subway(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

        self.Label = QLabel("This is the Subway Store Page")

        layout.addWidget(self.Label)
        return page
        
    def create_sale(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

        self.Label = QLabel("This is the Sales Page")

        layout.addWidget(self.Label)
        return page

    def create_checkout(self):
        page = QWidget()
        layout = QGridLayout()
        page.setLayout(layout)

        self.Label = QLabel("This is the Checkout Page")

        layout.addWidget(self.Label)
        return page
        

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())