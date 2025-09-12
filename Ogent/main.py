import sys
import os
from PyQt5.QtWidgets import QApplication, QStackedWidget

from login import LoginPage
from register import RegisterPage
from dashboard import DashboardPage
from Database.db import init_db, show_all_users

init_db()

app = QApplication(sys.argv)

base_dir = os.path.dirname(os.path.abspath(__file__))

style_path = os.path.join(base_dir, "STYLE", "style.qss")

with open(style_path, "r") as f:
    app.setStyleSheet(f.read())

stack = QStackedWidget()
stack.setWindowTitle("Login")

def show_register():
    register.clear_fields()
    stack.setCurrentWidget(register)
    stack.setWindowTitle("Register")
    

def show_login():
    login.clear_fields()
    stack.setCurrentWidget(login)
    stack.setWindowTitle("Login")
    

def show_dashboard(username):
    global dashboard
    stack.removeWidget(dashboard)
    dashboard = DashboardPage(logout_callback=show_login, username=username)
    stack.addWidget(dashboard)
    stack.setCurrentWidget(dashboard)
    stack.setWindowTitle("Dashboard")

login = LoginPage(switch_to_register=show_register, switch_to_dashboard=show_dashboard)
register = RegisterPage(switch_to_login=show_login)
dashboard = DashboardPage(logout_callback=show_login)

stack.addWidget(login)
stack.addWidget(register)


stack.setFixedSize(1000, 650)
stack.show()



# Test
users = show_all_users()
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}")


sys.exit(app.exec())