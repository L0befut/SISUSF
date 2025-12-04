# =============================================================================
# app/main.py
# =============================================================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from views.login_dialog import LoginDialog
from views.main_window import MainWindow
from db.create_tables import create_all_tables
from db.manage_data import create_seed_data
from config.settings import settings
from controllers.auth_controller import auth
import traceback

class SisUSFApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(settings.APP_NAME)
        self.app.setApplicationVersion(settings.VERSION)
        
        # Aplicar estilo global
        self.apply_global_style()
        
    def apply_global_style(self):
        """Aplica estilo global à aplicação"""
        style = """
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 12px;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        
        QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
            padding: 5px;
            border: 1px solid #bdc3c7;
            border-radius: 3px;
        }
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
            border-color: #3498db;
        }
        
        QTableWidget {
            gridline-color: #ecf0f1;
            selection-background-color: #3498db;
            selection-color: white;
            alternate-background-color: #f8f9fa;
        }
        
        QTableWidget::item {
            padding: 5px;
        }
        
        QHeaderView::section {
            background-color: #34495e;
            color: white;
            padding: 8px;
            border: none;
            font-weight: bold;
        }
        
        QTabWidget::pane {
            border: 1px solid #bdc3c7;
            top: -1px;
        }
        
        QTabBar::tab {
            background: #ecf0f1;
            border: 1px solid #bdc3c7;
            padding: 8px 16px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background: white;
            border-bottom-color: white;
        }
        
        QTabBar::tab:hover {
            background: #d5dbdb;
        }
        """
        self.app.setStyleSheet(style)
    
    def create_splash_screen(self):
        """Cria tela de splash"""
        # Criar uma imagem simples para o splash
        pixmap = QPixmap(400, 300)
        pixmap.fill(QColor("#3498db"))
        
        # Adicionar texto
        painter = QPainter(pixmap)
        painter.setPen(QColor("white"))
        
        # Título
        title_font = QFont("Arial", 24, QFont.Bold)
        painter.setFont(title_font)
        painter.drawText(50, 100, "SISUSF")
        
        # Subtítulo
        subtitle_font = QFont("Arial", 14)
        painter.setFont(subtitle_font)
        painter.drawText(50, 130, "Sistema de Saúde da Família")
        
        # Versão
        version_font = QFont("Arial", 10)
        painter.setFont(version_font)
        painter.drawText(50, 200, f"Versão {settings.VERSION}")
        painter.drawText(50, 220, "Carregando sistema...")
        
        painter.end()
        
        # Criar splash screen
        splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
        splash.setMask(pixmap.mask())
        
        return splash
    
    def initialize_database(self):
        """Inicializa o banco de dados"""
        try:
            print("🔧 Inicializando banco de dados...")
            
            # Criar tabelas
            if not create_all_tables():
                raise Exception("Erro ao criar tabelas")
            
            # Criar dados iniciais
            create_seed_data()
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na inicialização do banco: {e}")
            QMessageBox.critical(
                None, 
                "Erro de Banco de Dados",
                f"Não foi possível inicializar o banco de dados:\n\n{str(e)}\n\nVerifique se o PostgreSQL está rodando e as configurações estão corretas."
            )
            return False
    
    def show_login(self):
        """Exibe tela de login"""
        login_dialog = LoginDialog()
        
        if login_dialog.exec_() == LoginDialog.Accepted:
            return True
        else:
            return False
    
    def show_main_window(self):
        """Exibe janela principal"""
        self.main_window = MainWindow()
        self.main_window.show()
        return self.main_window
    
    def run(self):
        """Executa a aplicação"""
        try:
            # Mostrar splash screen
            splash = self.create_splash_screen()
            splash.show()
            self.app.processEvents()
            
            # Simular carregamento
            QTimer.singleShot(1000, lambda: None)
            self.app.processEvents()
            
            # Inicializar banco de dados
            splash.showMessage("Inicializando banco de dados...", Qt.AlignBottom, QColor("white"))
            self.app.processEvents()
            
            if not self.initialize_database():
                splash.close()
                return 1
            
            # Login
            splash.showMessage("Carregando interface...", Qt.AlignBottom, QColor("white"))
            self.app.processEvents()
            
            QTimer.singleShot(500, lambda: None)
            self.app.processEvents()
            
            splash.close()
            
            if not self.show_login():
                return 0  # Usuário cancelou login
            
            # Mostrar janela principal
            self.show_main_window()
            
            # Executar loop principal
            return self.app.exec_()
            
        except Exception as e:
            print(f"❌ Erro crítico na aplicação: {e}")
            print(traceback.format_exc())
            
            QMessageBox.critical(
                None,
                "Erro Crítico",
                f"Ocorreu um erro crítico na aplicação:\n\n{str(e)}\n\nA aplicação será encerrada."
            )
            return 1

def main():
    """Função principal"""
    try:
        # Criar e executar aplicação
        app = SisUSFApplication()
        return app.run()
        
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        print(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())