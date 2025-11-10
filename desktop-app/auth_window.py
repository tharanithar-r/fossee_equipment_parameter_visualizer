from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from api_client import APIClient
from main_window import MainWindow
from theme_manager import ThemeManager

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.theme_manager = ThemeManager()
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Login')
        self.setGeometry(100, 100, 400, 350)
        
        layout = QVBoxLayout()
        
        # Header with title and theme toggle
        header_layout = QHBoxLayout()
        
        title = QLabel('Chemical Equipment Visualizer')
        title.setAlignment(Qt.AlignLeft)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Theme toggle button
        self.theme_btn = QPushButton('☀️ Light' if self.theme_manager.current_theme == 'light' else '🌙 Dark')
        self.theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_btn)
        
        layout.addLayout(header_layout)
        
        # Tabs for Login/Register
        tabs = QTabWidget()
        tabs.addTab(self.create_login_tab(), 'Login')
        tabs.addTab(self.create_register_tab(), 'Register')
        layout.addWidget(tabs)
        
        self.setLayout(layout)
    
    def create_login_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Username
        layout.addWidget(QLabel('Username:'))
        self.login_username = QLineEdit()
        layout.addWidget(self.login_username)
        
        # Password
        layout.addWidget(QLabel('Password:'))
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.login_password)
        
        # Login Button
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_register_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Username
        layout.addWidget(QLabel('Username:'))
        self.register_username = QLineEdit()
        layout.addWidget(self.register_username)
        
        # Email
        layout.addWidget(QLabel('Email:'))
        self.register_email = QLineEdit()
        layout.addWidget(self.register_email)
        
        # Password
        layout.addWidget(QLabel('Password:'))
        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.register_password)
        
        # Register Button
        register_btn = QPushButton('Register')
        register_btn.clicked.connect(self.handle_register)
        layout.addWidget(register_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def handle_login(self):
        username = self.login_username.text()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return
        
        try:
            self.api_client.login(username, password)
            QMessageBox.information(self, 'Success', 'Logged in successfully')
            self.open_main_window()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Login failed: {str(e)}')
    
    def handle_register(self):
        username = self.register_username.text()
        email = self.register_email.text()
        password = self.register_password.text()
        
        if not username or not email or not password:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return
        
        try:
            self.api_client.register(username, email, password)
            QMessageBox.information(self, 'Success', 'Account created successfully. Please login.')
            self.register_username.clear()
            self.register_email.clear()
            self.register_password.clear()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Registration failed: {str(e)}')
    
    def apply_theme(self):
        """Apply current theme to the window"""
        self.setStyleSheet(self.theme_manager.get_stylesheet())
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        new_theme = self.theme_manager.toggle_theme()
        self.theme_btn.setText('☀️ Light' if new_theme == 'light' else '🌙 Dark')
        self.apply_theme()
    
    def open_main_window(self):
        self.main_window = MainWindow(self.api_client, self.theme_manager)
        self.main_window.show()
        self.close()
