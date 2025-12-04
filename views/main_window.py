# =============================================================================
# views/main_window.py
# =============================================================================

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime
from controllers.auth_controller import auth
from controllers.relatorio_controller import relatorio_controller
from views.cadastro_paciente import CadastroPacienteDialog
from views.consulta_paciente import ConsultaPacienteWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_dashboard_data()
    
    def init_ui(self):
        self.setWindowTitle("SISUSF - Sistema de Saúde da Família")
        self.setGeometry(100, 100, 1200, 800)
        
        # Menu bar
        self.create_menu_bar()
        
        # Toolbar
        self.create_toolbar()
        
        # Status bar
        self.statusBar().showMessage(f"Usuário: {auth.current_user.nome} - {auth.current_user.tipo.upper()}")
        
        # Widget central
        self.create_central_widget()
        
        # Aplicar estilo
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QMenuBar {
                background-color: #34495e;
                color: white;
                border: none;
            }
            QMenuBar::item {
                padding: 8px 12px;
            }
            QMenuBar::item:selected {
                background-color: #3498db;
            }
            QToolBar {
                background-color: #3498db;
                border: none;
                spacing: 3px;
            }
            QToolButton {
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
            }
            QToolButton:hover {
                background-color: #2980b9;
            }
        """)
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # Menu Cadastro
        cadastro_menu = menubar.addMenu('Cadastro')
        cadastro_menu.addAction('Novo Paciente', self.show_cadastro_paciente, 'Ctrl+N')
        cadastro_menu.addAction('Nova Família', self.show_cadastro_familia)
        cadastro_menu.addSeparator()
        cadastro_menu.addAction('Usuários', self.show_usuarios)
        
        # Menu Atendimento
        atendimento_menu = menubar.addMenu('Atendimento')
        atendimento_menu.addAction('Consulta', self.show_consulta, 'Ctrl+C')
        atendimento_menu.addAction('Agenda', self.show_agenda)
        atendimento_menu.addSeparator()
        atendimento_menu.addAction('Medicamentos', self.show_medicamentos)
        
        # Menu Relatórios
        relatorios_menu = menubar.addMenu('Relatórios')
        relatorios_menu.addAction('Dashboard', self.show_dashboard, 'F5')
        relatorios_menu.addAction('Pacientes', self.show_relatorio_pacientes)
        relatorios_menu.addAction('Consultas', self.show_relatorio_consultas)
        
        # Menu Sistema
        sistema_menu = menubar.addMenu('Sistema')
        sistema_menu.addAction('Backup', self.fazer_backup)
        sistema_menu.addAction('Configurações', self.show_configuracoes)
        sistema_menu.addSeparator()
        sistema_menu.addAction('Sair', self.close, 'Ctrl+Q')
    
    def create_toolbar(self):
        toolbar = self.addToolBar('Principal')
        
        # Ações principais
        toolbar.addAction('Novo Paciente', self.show_cadastro_paciente)
        toolbar.addAction('Buscar', self.show_busca_paciente)
        toolbar.addAction('Consulta', self.show_consulta)
        toolbar.addSeparator()
        toolbar.addAction('Dashboard', self.show_dashboard)
        toolbar.addAction('Relatórios', self.show_relatorios)
        
        # Adicionar busca rápida
        toolbar.addSeparator()
        search_label = QLabel("Busca rápida:")
        search_label.setStyleSheet("color: white; margin-left: 10px;")
        toolbar.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nome, CPF ou CNS...")
        self.search_input.setMaximumWidth(200)
        self.search_input.returnPressed.connect(self.busca_rapida)
        toolbar.addWidget(self.search_input)
    
    def create_central_widget(self):
        """Cria widget central com tabs"""
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # Tab Dashboard
        self.dashboard_tab = self.create_dashboard_tab()
        self.tab_widget.addTab(self.dashboard_tab, "Dashboard")
        
        # Tab Pacientes
        self.pacientes_tab = ConsultaPacienteWidget()
        self.tab_widget.addTab(self.pacientes_tab, "Pacientes")
    
    def create_dashboard_tab(self):
        """Cria aba do dashboard"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("Dashboard - Visão Geral")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin: 20px;
            }
        """)
        layout.addWidget(title)
        
        # Cards com estatísticas
        cards_layout = QHBoxLayout()
        
        # Card Total Pacientes
        self.card_total_pacientes = self.create_stat_card(
            "Total de Pacientes", "0", "#3498db"
        )
        cards_layout.addWidget(self.card_total_pacientes)
        
        # Card Pacientes do Mês
        self.card_pacientes_mes = self.create_stat_card(
            "Novos no Mês", "0", "#2ecc71"
        )
        cards_layout.addWidget(self.card_pacientes_mes)
        
        # Card Consultas Hoje
        self.card_consultas_hoje = self.create_stat_card(
            "Consultas Hoje", "0", "#f39c12"
        )
        cards_layout.addWidget(self.card_consultas_hoje)
        
        # Card Consultas do Mês
        self.card_consultas_mes = self.create_stat_card(
            "Consultas no Mês", "0", "#e74c3c"
        )
        cards_layout.addWidget(self.card_consultas_mes)
        
        layout.addLayout(cards_layout)
        
        # Gráficos e outras informações
        info_layout = QHBoxLayout()
        
        # Lista de consultas de hoje
        consultas_hoje_widget = QGroupBox("Consultas de Hoje")
        consultas_hoje_layout = QVBoxLayout()
        
        self.lista_consultas_hoje = QListWidget()
        self.lista_consultas_hoje.addItem("Carregando...")
        consultas_hoje_layout.addWidget(self.lista_consultas_hoje)
        
        consultas_hoje_widget.setLayout(consultas_hoje_layout)
        info_layout.addWidget(consultas_hoje_widget)
        
        # Informações do sistema
        sistema_widget = QGroupBox("Sistema")
        sistema_layout = QVBoxLayout()
        
        # CORREÇÃO: Cria o QTextEdit ANTES de usar
        self.info_sistema = QTextEdit()
        self.info_sistema.setReadOnly(True)
        self.info_sistema.setMaximumHeight(200)
        self.info_sistema.setText(f"""
Usuário: {auth.current_user.nome}
Perfil: {auth.current_user.tipo.upper()}
Último login: Agora
Versão: 1.0.0
        """)
        sistema_layout.addWidget(self.info_sistema)
        
        sistema_widget.setLayout(sistema_layout)
        info_layout.addWidget(sistema_widget)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_stat_card(self, title: str, value: str, color: str):
        """Cria card de estatística"""
        card = QFrame()
        card.setFrameStyle(QFrame.Box)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 10px;
                margin: 10px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        # Título
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {color};
                font-weight: bold;
                margin: 10px;
            }}
        """)
        
        # Valor
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                color: {color};
                font-weight: bold;
                margin: 10px;
            }}
        """)
        
        # Armazenar referência ao label do valor
        card.value_label = value_label
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        
        card.setLayout(layout)
        return card
    
    def load_dashboard_data(self):
        """Carrega dados do dashboard"""
        result = relatorio_controller.get_dashboard_data()
        
        if result["success"]:
            data = result["data"]
            
            # Atualizar cards
            self.card_total_pacientes.value_label.setText(str(data["total_pacientes"]))
            self.card_pacientes_mes.value_label.setText(str(data["pacientes_mes"]))
            self.card_consultas_hoje.value_label.setText(str(data["consultas_hoje"]))
            self.card_consultas_mes.value_label.setText(str(data["consultas_mes"]))
    
    # Métodos dos menus
    def show_cadastro_paciente(self):
        dialog = CadastroPacienteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_dashboard_data()
    
    def show_cadastro_familia(self):
        QMessageBox.information(self, "Info", "Funcionalidade em desenvolvimento")
    
    def show_usuarios(self):
        QMessageBox.information(self, "Info", "Funcionalidade em desenvolvimento")
    
    def show_consulta(self):
        self.tab_widget.setCurrentWidget(self.pacientes_tab)
    
    def show_agenda(self):
        QMessageBox.information(self, "Info", "Funcionalidade em desenvolvimento")
    
    def show_medicamentos(self):
        QMessageBox.information(self, "Info", "Funcionalidade em desenvolvimento")
    
    def show_dashboard(self):
        self.tab_widget.setCurrentIndex(0)
        self.load_dashboard_data()
    
    def show_relatorio_pacientes(self):
        QMessageBox.information(self, "Info", "Funcionalidade em desenvolvimento")
    
    def show_relatorio_consultas(self):
        QMessageBox.information(self, "Info", "Funcionalidade em desenvolvimento")
    
    def show_busca_paciente(self):
        self.tab_widget.setCurrentWidget(self.pacientes_tab)
        self.pacientes_tab.search_input.setFocus()
    
    def show_relatorios(self):
        QMessageBox.information(self, "Info", "Funcionalidade em desenvolvimento")
    
    def show_configuracoes(self):
        QMessageBox.information(self, "Info", "Funcionalidade em desenvolvimento")
    
    def fazer_backup(self):
        QMessageBox.information(self, "Info", "Funcionalidade em desenvolvimento")
    
    def busca_rapida(self):
        query = self.search_input.text().strip()
        if query:
            self.tab_widget.setCurrentWidget(self.pacientes_tab)
            self.pacientes_tab.search_input.setText(query)
            self.pacientes_tab.search_pacientes()
            self.search_input.clear()
    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Sair',
            "Tem certeza que deseja sair do sistema?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            auth.logout()
            event.accept()
        else:
            event.ignore()