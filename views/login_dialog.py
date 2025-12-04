# =============================================================================
# views/login_dialog.py
# =============================================================================

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from controllers.auth_controller import auth

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("SISUSF - Login")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Logo/Título
        title = QLabel("SISUSF")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin: 20px;
            }
        """)
        
        subtitle = QLabel("Sistema de Saúde da Família")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        
        # Formulário
        form_layout = QFormLayout()
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("seuemail@exemplo.com")
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Sua senha")
        self.password_input.setStyleSheet(self.email_input.styleSheet())
        
        form_layout.addRow("E-mail:", self.email_input)
        form_layout.addRow("Senha:", self.password_input)
        
        # Botões
        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton("Entrar")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.login_button)
        
        # Conectar eventos
        self.login_button.clicked.connect(self.handle_login)
        cancel_button.clicked.connect(self.reject)
        self.password_input.returnPressed.connect(self.handle_login)
        
        # Adicionar ao layout
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Foco inicial
        self.email_input.setFocus()
    
    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Atenção", "Preencha email e senha.")
            return
        
        # Desabilitar botão durante login
        self.login_button.setEnabled(False)
        self.login_button.setText("Entrando...")
        
        # Processar login
        result = auth.login(email, password, "127.0.0.1")
        
        if result["success"]:
            self.accept()
        else:
            QMessageBox.critical(self, "Erro", result["message"])
            self.login_button.setEnabled(True)
            self.login_button.setText("Entrar")
            self.password_input.clear()
            self.password_input.setFocus()