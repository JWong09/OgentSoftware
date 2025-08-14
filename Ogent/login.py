from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from Database.db import register_user, validate_login

class LoginPage(QWidget):
    def __init__(self, switch_to_register, switch_to_dashboard):
        super().__init__()
        self.switch_to_register = switch_to_register
        self.switch_to_dashboard = switch_to_dashboard

        self.setObjectName("loginPage")

        self.build_ui()

    def build_ui(self):
        layout = QHBoxLayout()
        layout.addWidget(self.build_left_panel(), 1)
        layout.addWidget(self.build_divider())
        layout.addWidget(self.build_right_panel(), 1)
        layout.setSpacing(0)
        self.setLayout(layout)

    def build_left_panel(self):
        branding_label = QLabel("O-gent")
        branding_label.setObjectName("brandingLabel")
        branding_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(branding_label)
        layout.addStretch()

        panel = QWidget()
        panel.setLayout(layout)
        panel.setObjectName("leftPanel")
        return panel

    def build_divider(self):
        divider = QFrame()
        divider.setFixedHeight(325)
        divider.setFixedWidth(1)
        divider.setStyleSheet("QFrame { background-color: white; }")
        divider.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        return divider

    def build_right_panel(self):
        self.title = QLabel("Sign in")
        self.title.setObjectName("loginTitle")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Your Username")
        self.username.setObjectName("loginUsername")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setObjectName("loginPassword")

        login_btn = QPushButton("Login")
        login_btn.setObjectName("loginButton")
        login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        login_btn.clicked.connect(self.handle_login)

        guest_btn = QPushButton("Continue as a Guest")
        guest_btn.setObjectName("guestButton")
        guest_btn.setCursor(QCursor(Qt.PointingHandCursor))
        guest_btn.setFlat(True)
        guest_btn.clicked.connect(self.continue_as_guest)

        register_btn = QPushButton("Don't have an Account?")
        register_btn.setFlat(True)
        register_btn.setCursor(QCursor(Qt.PointingHandCursor))
        register_btn.setObjectName("guestButton")
        register_btn.clicked.connect(self.continue_to_register)

        register_layout = QHBoxLayout()
        register_layout.addStretch()
        register_layout.addWidget(register_btn)

        form_center = QVBoxLayout()
        form_center.addWidget(self.title)
        form_center.addSpacing(10)
        form_center.addWidget(self.username)
        form_center.addWidget(self.password)
        form_center.addLayout(register_layout)
        form_center.addWidget(login_btn)
        form_center.addWidget(guest_btn)
        form_center.setSpacing(10)
        form_center.setAlignment(Qt.AlignVCenter)

        form_layout = QVBoxLayout()
        form_layout.addStretch()
        form_layout.addLayout(form_center)
        form_layout.addStretch()
        form_layout.setContentsMargins(40, 40, 40, 40)

        panel = QWidget()
        panel.setLayout(form_layout)
        panel.setObjectName("rightPanel")
        return panel

    def handle_login(self):
        username = self.username.text()
        password = self.password.text()

        if not username or not password:
            QMessageBox.warning(self, "Missing Fields", "Please enter both username and Password.")
            return
        if validate_login(username, password):
            QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")
            self.switch_to_dashboard(username)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def continue_as_guest(self):
        print("Guest Login Activated")
        self.switch_to_dashboard(username="Guest")

    def continue_to_register(self):
        print("Register")
        self.switch_to_register()

    def clear_fields(self):
        self.username.clear()
        self.password.clear()
        self.username.setFocus()