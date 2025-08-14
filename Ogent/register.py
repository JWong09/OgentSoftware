
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from Database.db import register_user

class RegisterPage(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        self.switch_to_login = switch_to_login

        self.setObjectName("registerPage")

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
        self.title = QLabel("Register")
        self.title.setObjectName("loginTitle")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Set Username")
        self.username.setObjectName("loginUsername")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Set Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setObjectName("loginPassword")

        self.confirm = QLineEdit()
        self.confirm.setPlaceholderText("Confirm Password")
        self.confirm.setEchoMode(QLineEdit.Password)
        self.confirm.setObjectName("loginPassword")

        register_btn = QPushButton("Register")
        register_btn.setObjectName("loginButton")
        register_btn.setCursor(QCursor(Qt.PointingHandCursor))
        register_btn.clicked.connect(self.handle_register)

        back_btn = QPushButton("Back to Login")
        back_btn.setFlat(True)
        back_btn.setCursor(QCursor(Qt.PointingHandCursor))
        back_btn.setObjectName("guestButton")
        back_btn.clicked.connect(self.switch_to_login)

        back_layout = QHBoxLayout()
        back_layout.addStretch()
        back_layout.addWidget(back_btn)

        form_center = QVBoxLayout()
        form_center.addWidget(self.title)
        form_center.addSpacing(10)
        form_center.addWidget(self.username)
        form_center.addWidget(self.password)
        form_center.addWidget(self.confirm)
        form_center.addLayout(back_layout)
        form_center.addWidget(register_btn)
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

    def handle_register(self):
        username = self.username.text()
        password = self.password.text()
        confirm = self.confirm.text()

        if not username or not password or not confirm:
            QMessageBox.warning(self, "Missing Fields", "Please fill all fields.")
            return
        if password != confirm:
            QMessageBox.warning(self, "Password Mismatch", "Passwords do not match.")
            return

        success = register_user(username, password)
        if success:
            QMessageBox.information(self, "Success", "Account Created! Please login.")
            self.switch_to_login()
        else:
            QMessageBox.warning(self, "Error", "Username already taken.")

    def clear_fields(self):
        self.username.clear()
        self.password.clear()
        self.confirm.clear()
        self.username.setFocus()