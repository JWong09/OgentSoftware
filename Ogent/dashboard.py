import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QPushButton, QLabel, QComboBox, QInputDialog, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from Database.db import get_user_id, add_profile, get_profiles, update_profile_name, delete_profile, get_profile_settings

class DashboardPage(QWidget):
    def __init__(self, logout_callback, username="Guest"):
        super().__init__()
        self.logout_callback = logout_callback
        self.username = username
        self.user_id = get_user_id(username)
        self.setWindowTitle("O-Gent Software")
        self.setFixedSize(1000, 650)
        self.setObjectName("dashboardPage")

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        sidebar = self.build_sidebar()
        main_layout.addLayout(sidebar, 2)

        camera_input = self.build_camera_input()
        main_layout.addWidget(camera_input, 3)

        self.setLayout(main_layout)

    def build_sidebar(self):
        layout = QVBoxLayout()

        # TOP SECTION: User Info + Logout
        user_info_layout = QHBoxLayout()
        user_label = QLabel(f"Logged in as: {self.username}")
        user_label.setStyleSheet("font-weight: bold;")
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("color: red;")
        logout_btn.clicked.connect(self.logout_user)
        user_info_layout.addWidget(user_label)
        user_info_layout.addStretch()
        user_info_layout.addWidget(logout_btn)
        layout.addLayout(user_info_layout)

        # PROFILE SECTION
        profile_box = QGroupBox("PROFILE")
        profile_layout = QVBoxLayout()

        self.profile_combo = QComboBox()

        profile_layout.addWidget(self.profile_combo)
        self.load_profiles()
        self.profile_combo.currentIndexChanged.connect(self.load_profile_settings)
        

        icons = [
            ("icons/plus.svg", self.add_profile_dialog),
            ("icons/edit.svg", self.edit_profile_dialog),
            ("icons/trash-2.svg", self.delete_profile_dialog)
        ]

        profile_buttons_layout = QHBoxLayout()
        for icon_path, handler in icons:
            btn = QPushButton()
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(24, 24))
            btn.clicked.connect(handler)
            profile_buttons_layout.addWidget(btn)

        profile_layout.addLayout(profile_buttons_layout)
        profile_box.setLayout(profile_layout)
        layout.addWidget(profile_box)

        # DEVICE SETTINGS SECTION
        device_settings_box = QGroupBox("DEVICE SETTINGS")
        device_settings_layout = QVBoxLayout()

        # Right Click Action
        right_click_layout = QHBoxLayout()
        right_label = QLabel("Right Click:")
        right_btn = QPushButton("Set Action")
        right_btn.clicked.connect(self.set_right_click_action)
        right_click_layout.addWidget(right_label)
        right_click_layout.addWidget(right_btn)

        self.right_status = QLabel("")
        self.right_status.setStyleSheet("color: green; font-style: italic;")

        # Left Click Action
        left_click_layout = QHBoxLayout()
        left_label = QLabel("Left Click:")
        left_btn = QPushButton("Set Action")
        left_btn.clicked.connect(self.set_left_click_action)
        left_click_layout.addWidget(left_label)
        left_click_layout.addWidget(left_btn)

        self.left_status = QLabel("")
        self.left_status.setStyleSheet("color: green; font-style: italic;")

        device_settings_layout.addLayout(right_click_layout)
        device_settings_layout.addWidget(self.right_status)
        device_settings_layout.addLayout(left_click_layout)
        device_settings_layout.addWidget(self.left_status)

        device_settings_box.setLayout(device_settings_layout)
        layout.addWidget(device_settings_box)

        layout.addStretch()
        self.load_profile_settings()
        return layout

    def build_camera_input(self):
        camera_box = QGroupBox("CAMERA INPUT")
        camera_layout = QVBoxLayout()

        self.camera_label = QLabel("Camera Feed")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setObjectName("camera_label")
        self.camera_label.setStyleSheet("background-color: #d0d0d0; border: 1px solid #aaa;")
        self.camera_label.setFixedSize(600, 500)

        camera_layout.addWidget(self.camera_label)
        camera_box.setLayout(camera_layout)
        return camera_box

    def set_left_click_action(self):
        self.left_status.setText("Waiting for user action...")

    def set_right_click_action(self):
        self.right_status.setText("Waiting for user action...")

    def logout_user(self):
        print("Logging out...")
        self.close()
        self.logout_callback()

    def load_profiles(self):
        self.profile_combo.clear()
        profiles = get_profiles(self.user_id)
        self.profiles = {name: pid for pid, name in profiles}
        self.profile_combo.addItems(self.profiles.keys())

    def add_profile_dialog(self):
        name, ok = QInputDialog.getText(self, "Add profile", "Enter Profile name:")
        if ok and name:
            add_profile(self.user_id, name, "Left Blink", "Right Blink")
            self.load_profiles()
            index = self.profile_combo.findText(name)
            if index != -1:
                self.profile_combo.setCurrentIndex(index)
            

    def edit_profile_dialog(self):
        current_name = self.profile_combo.currentText()
        if not current_name:
            return
        new_name, ok = QInputDialog.getText(self, "Rename Profile", f"Rename '{current_name}' to:")
        if ok and new_name:
            profile_id = self.profiles.get(current_name)
            update_profile_name(profile_id, new_name)
            self.load_profiles()
            index = self.profile_combo.findText(new_name)
            self.profile_combo.setCurrentIndex(index)

        

    def delete_profile_dialog(self):
        current_name = self.profile_combo.currentText()
        if not current_name:
            return
        confirm = QMessageBox.question(self, "Delete Profile", f"Are you sure you want to delete '{current_name}'?")
        if confirm == QMessageBox.Yes:
            profile_id = self.profiles.get(current_name)
            delete_profile(profile_id)
            self.load_profiles()

    def load_profile_settings(self):
        current_name = self.profile_combo.currentText()
        if not current_name:
            return

        profile_id = self.profiles.get(current_name)
        if profile_id is None:
            return

        settings = get_profile_settings(profile_id)
        if settings:
            left_action, right_action = settings
            self.left_status.setText(left_action if left_action else "No Action Set")
            self.right_status.setText(right_action if right_action else "No Action Set")
        
# Test Launch
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = DashboardPage(username="Jae")  # or "Guest"
    dashboard.show()
    sys.exit(app.exec_())