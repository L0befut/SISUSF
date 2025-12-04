# =============================================================================
# views/consulta_paciente.py
# =============================================================================

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from controllers.paciente_controller import paciente_controller
from utils.formatters import Formatters
from datetime import datetime

class ConsultaPacienteWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_pacientes = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("Consulta de Pacientes")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
                margin: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Barra de busca
        search_layout = QHBoxLayout()
        
        search_label = QLabel("Buscar paciente:")
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite nome, CPF ou CNS...")
        self.search_input.textChanged.connect(self.on_search_changed)
        self.search_input.returnPressed.connect(self.search_pacientes)
        search_layout.addWidget(self.search_input)
        
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search_pacientes)
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        search_layout.addWidget(search_button)
        
        layout.addLayout(search_layout)
        
        # Tabela de resultados
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Nome", "CPF", "CNS", "Data Nasc.", "Telefone", "Ações"
        ])
        
        # Configurar tabela
        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Nome
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # CPF
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # CNS
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Data
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Telefone
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Ações
        
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        
        # Status
        self.status_label = QLabel("Digite no campo de busca para pesquisar pacientes")
        self.status_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def on_search_changed(self):
        """Busca automática conforme o usuário digita"""
        query = self.search_input.text().strip()
        if len(query) >= 3:  # Buscar a partir de 3 caracteres
            QTimer.singleShot(500, self.search_pacientes)  # Delay para evitar muitas buscas
    
    def search_pacientes(self):
        """Busca pacientes"""
        query = self.search_input.text().strip()
        
        if not query:
            self.table.setRowCount(0)
            self.status_label.setText("Digite no campo de busca para pesquisar pacientes")
            return
        
        # Buscar
        self.status_label.setText("Buscando...")
        pacientes = paciente_controller.search_pacientes(query)
        
        # Atualizar tabela
        self.current_pacientes = pacientes
        self.update_table(pacientes)
        
        # Status
        if pacientes:
            self.status_label.setText(f"{len(pacientes)} paciente(s) encontrado(s)")
        else:
            self.status_label.setText("Nenhum paciente encontrado")
    
    def update_table(self, pacientes):
        """Atualiza a tabela com os pacientes"""
        self.table.setRowCount(len(pacientes))
        
        for row, paciente in enumerate(pacientes):
            # Nome
            nome_item = QTableWidgetItem(paciente.nome)
            nome_item.setFlags(nome_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, nome_item)
            
            # CPF
            cpf_item = QTableWidgetItem(Formatters.format_cpf(paciente.cpf))
            cpf_item.setFlags(cpf_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, cpf_item)
            
            # CNS
            cns_item = QTableWidgetItem(Formatters.format_cns(paciente.cns))
            cns_item.setFlags(cns_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 2, cns_item)
            
            # Data de nascimento e idade
            data_nasc = paciente.data_nascimento.strftime("%d/%m/%Y")
            idade = paciente.idade
            data_item = QTableWidgetItem(f"{data_nasc} ({idade} anos)")
            data_item.setFlags(data_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 3, data_item)
            
            # Telefone
            telefone = ""
            if paciente.celular:
                telefone = Formatters.format_phone(paciente.celular)
            elif paciente.telefone:
                telefone = Formatters.format_phone(paciente.telefone)
            
            telefone_item = QTableWidgetItem(telefone)
            telefone_item.setFlags(telefone_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 4, telefone_item)
            
            # Botões de ação
            actions_widget = self.create_action_buttons(paciente.id, row)
            self.table.setCellWidget(row, 5, actions_widget)
    
    def create_action_buttons(self, paciente_id, row):
        """Cria botões de ação para cada linha"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        
        # Botão Ver
        view_button = QPushButton("Ver")
        view_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        view_button.clicked.connect(lambda: self.view_paciente(paciente_id))
        layout.addWidget(view_button)
        
        # Botão Editar
        edit_button = QPushButton("Editar")
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        edit_button.clicked.connect(lambda: self.edit_paciente(paciente_id))
        layout.addWidget(edit_button)
        
        # Botão Consulta
        consult_button = QPushButton("Consulta")
        consult_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        consult_button.clicked.connect(lambda: self.new_consulta(paciente_id))
        layout.addWidget(consult_button)
        
        widget.setLayout(layout)
        return widget
    
    def view_paciente(self, paciente_id):
        """Visualizar dados do paciente"""
        result = paciente_controller.get_paciente_by_id(paciente_id)
        
        if result["success"]:
            paciente = result["paciente"]
            
            # Criar dialog de visualização
            dialog = PacienteViewDialog(paciente, self)
            dialog.exec_()
        else:
            QMessageBox.critical(self, "Erro", result["message"])
    
    def edit_paciente(self, paciente_id):
        """Editar paciente"""
        QMessageBox.information(self, "Info", f"Editar paciente ID: {paciente_id}\nFuncionalidade em desenvolvimento")
    
    def new_consulta(self, paciente_id):
        """Nova consulta para paciente"""
        QMessageBox.information(self, "Info", f"Nova consulta para paciente ID: {paciente_id}\nFuncionalidade em desenvolvimento")

class PacienteViewDialog(QDialog):
    """Dialog para visualizar dados completos do paciente"""
    
    def __init__(self, paciente, parent=None):
        super().__init__(parent)
        self.paciente = paciente
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"Paciente: {self.paciente.nome}")
        self.setGeometry(150, 150, 600, 500)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Scroll area
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Dados pessoais
        pessoais_group = QGroupBox("Dados Pessoais")
        pessoais_layout = QFormLayout()
        
        pessoais_layout.addRow("Nome:", QLabel(self.paciente.nome))
        if self.paciente.nome_social:
            pessoais_layout.addRow("Nome social:", QLabel(self.paciente.nome_social))
        pessoais_layout.addRow("CPF:", QLabel(Formatters.format_cpf(self.paciente.cpf)))
        pessoais_layout.addRow("CNS:", QLabel(Formatters.format_cns(self.paciente.cns)))
        if self.paciente.rg:
            pessoais_layout.addRow("RG:", QLabel(self.paciente.rg))
        
        data_nasc = self.paciente.data_nascimento.strftime("%d/%m/%Y")
        pessoais_layout.addRow("Data nascimento:", QLabel(f"{data_nasc} ({self.paciente.idade} anos)"))
        pessoais_layout.addRow("Sexo:", QLabel("Masculino" if self.paciente.sexo.value == "M" else "Feminino"))
        
        if self.paciente.estado_civil:
            pessoais_layout.addRow("Estado civil:", QLabel(self.paciente.estado_civil.value.replace('_', ' ').title()))
        if self.paciente.escolaridade:
            pessoais_layout.addRow("Escolaridade:", QLabel(self.paciente.escolaridade.value.replace('_', ' ').title()))
        if self.paciente.profissao:
            pessoais_layout.addRow("Profissão:", QLabel(self.paciente.profissao))
        
        pessoais_group.setLayout(pessoais_layout)
        scroll_layout.addWidget(pessoais_group)
        
        # Contato
        contato_group = QGroupBox("Contato")
        contato_layout = QFormLayout()
        
        if self.paciente.telefone:
            contato_layout.addRow("Telefone:", QLabel(Formatters.format_phone(self.paciente.telefone)))
        if self.paciente.celular:
            contato_layout.addRow("Celular:", QLabel(Formatters.format_phone(self.paciente.celular)))
        if self.paciente.email:
            contato_layout.addRow("Email:", QLabel(self.paciente.email))
        
        contato_group.setLayout(contato_layout)
        scroll_layout.addWidget(contato_group)
        
        # Endereço
        if self.paciente.endereco:
            endereco_group = QGroupBox("Endereço")
            endereco_layout = QFormLayout()
            
            endereco = self.paciente.endereco
            if endereco.cep:
                endereco_layout.addRow("CEP:", QLabel(Formatters.format_cep(endereco.cep)))
            if endereco.logradouro:
                logradouro_completo = endereco.logradouro
                if endereco.numero:
                    logradouro_completo += f", {endereco.numero}"
                if endereco.complemento:
                    logradouro_completo += f" - {endereco.complemento}"
                endereco_layout.addRow("Logradouro:", QLabel(logradouro_completo))
            if endereco.bairro:
                endereco_layout.addRow("Bairro:", QLabel(endereco.bairro))
            if endereco.cidade:
                cidade_uf = endereco.cidade
                if endereco.uf:
                    cidade_uf += f"/{endereco.uf}"
                endereco_layout.addRow("Cidade/UF:", QLabel(cidade_uf))
            if endereco.ponto_referencia:
                endereco_layout.addRow("Ponto referência:", QLabel(endereco.ponto_referencia))
            
            endereco_group.setLayout(endereco_layout)
            scroll_layout.addWidget(endereco_group)
        
        # Dados clínicos
        clinicos_group = QGroupBox("Dados Clínicos")
        clinicos_layout = QFormLayout()
        
        if self.paciente.peso:
            clinicos_layout.addRow("Peso:", QLabel(f"{self.paciente.peso} kg"))
        if self.paciente.altura:
            clinicos_layout.addRow("Altura:", QLabel(f"{self.paciente.altura} m"))
        if self.paciente.imc:
            clinicos_layout.addRow("IMC:", QLabel(f"{self.paciente.imc}"))
        if self.paciente.tipo_sanguineo:
            clinicos_layout.addRow("Tipo sanguíneo:", QLabel(self.paciente.tipo_sanguineo))
        if self.paciente.alergias:
            clinicos_layout.addRow("Alergias:", QLabel(self.paciente.alergias))
        if self.paciente.medicamentos_uso_continuo:
            clinicos_layout.addRow("Medicamentos contínuos:", QLabel(self.paciente.medicamentos_uso_continuo))
        if self.paciente.observacoes_medicas:
            clinicos_layout.addRow("Observações médicas:", QLabel(self.paciente.observacoes_medicas))
        
        clinicos_group.setLayout(clinicos_layout)
        scroll_layout.addWidget(clinicos_group)
        
        # Informações do sistema
        sistema_group = QGroupBox("Informações do Sistema")
        sistema_layout = QFormLayout()
        
        sistema_layout.addRow("Cadastrado em:", QLabel(self.paciente.created_at.strftime("%d/%m/%Y %H:%M")))
        if self.paciente.created_by:
            sistema_layout.addRow("Cadastrado por:", QLabel(self.paciente.created_by))
        if self.paciente.updated_at != self.paciente.created_at:
            sistema_layout.addRow("Última atualização:", QLabel(self.paciente.updated_at.strftime("%d/%m/%Y %H:%M")))
            if self.paciente.updated_by:
                sistema_layout.addRow("Atualizado por:", QLabel(self.paciente.updated_by))
        
        sistema_group.setLayout(sistema_layout)
        scroll_layout.addWidget(sistema_group)
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(scroll)
        
        # Botão fechar
        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)