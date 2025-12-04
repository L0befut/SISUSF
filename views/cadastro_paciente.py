# =============================================================================
# views/cadastro_paciente.py
# =============================================================================

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from controllers.paciente_controller import paciente_controller
from utils.validators import Validators
from utils.formatters import Formatters
from models.paciente import Sexo, EstadoCivil, Escolaridade
from datetime import datetime

class CadastroPacienteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Cadastro de Paciente")
        self.setGeometry(100, 100, 800, 600)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Scroll area para o formulário
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Criar abas
        tab_widget = QTabWidget()
        
        # Aba Dados Pessoais
        tab_widget.addTab(self.create_dados_pessoais_tab(), "Dados Pessoais")
        
        # Aba Endereço
        tab_widget.addTab(self.create_endereco_tab(), "Endereço")
        
        # Aba Dados Clínicos
        tab_widget.addTab(self.create_dados_clinicos_tab(), "Dados Clínicos")
        
        scroll_layout.addWidget(tab_widget)
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(scroll)
        
        # Botões
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        
        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_paciente)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def create_dados_pessoais_tab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # Nome completo
        self.nome_input = QLineEdit()
        self.nome_input.setMaxLength(200)
        layout.addRow("Nome completo *:", self.nome_input)
        
        # Nome social
        self.nome_social_input = QLineEdit()
        self.nome_social_input.setMaxLength(200)
        layout.addRow("Nome social:", self.nome_social_input)
        
        # CPF
        self.cpf_input = QLineEdit()
        self.cpf_input.setMaxLength(14)
        self.cpf_input.setInputMask("999.999.999-99")
        layout.addRow("CPF *:", self.cpf_input)
        
        # CNS
        self.cns_input = QLineEdit()
        self.cns_input.setMaxLength(18)
        self.cns_input.setInputMask("999 9999 9999 9999")
        layout.addRow("CNS *:", self.cns_input)
        
        # RG
        self.rg_input = QLineEdit()
        self.rg_input.setMaxLength(20)
        layout.addRow("RG:", self.rg_input)
        
        # Data de nascimento
        self.data_nascimento_input = QDateEdit()
        self.data_nascimento_input.setCalendarPopup(True)
        self.data_nascimento_input.setDate(QDate.currentDate().addYears(-30))
        layout.addRow("Data de nascimento *:", self.data_nascimento_input)
        
        # Sexo
        self.sexo_combo = QComboBox()
        self.sexo_combo.addItem("Masculino", Sexo.MASCULINO)
        self.sexo_combo.addItem("Feminino", Sexo.FEMININO)
        layout.addRow("Sexo *:", self.sexo_combo)
        
        # Telefone
        self.telefone_input = QLineEdit()
        self.telefone_input.setInputMask("(99) 9999-9999")
        layout.addRow("Telefone:", self.telefone_input)
        
        # Celular
        self.celular_input = QLineEdit()
        self.celular_input.setInputMask("(99) 99999-9999")
        layout.addRow("Celular:", self.celular_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setMaxLength(150)
        layout.addRow("Email:", self.email_input)
        
        # Estado civil
        self.estado_civil_combo = QComboBox()
        self.estado_civil_combo.addItem("Selecione...", None)
        for estado in EstadoCivil:
            self.estado_civil_combo.addItem(estado.value.replace('_', ' ').title(), estado)
        layout.addRow("Estado civil:", self.estado_civil_combo)
        
        # Escolaridade
        self.escolaridade_combo = QComboBox()
        self.escolaridade_combo.addItem("Selecione...", None)
        for escolaridade in Escolaridade:
            self.escolaridade_combo.addItem(escolaridade.value.replace('_', ' ').title(), escolaridade)
        layout.addRow("Escolaridade:", self.escolaridade_combo)
        
        # Profissão
        self.profissao_input = QLineEdit()
        self.profissao_input.setMaxLength(100)
        layout.addRow("Profissão:", self.profissao_input)
        
        widget.setLayout(layout)
        return widget
    
    def create_endereco_tab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # CEP
        self.cep_input = QLineEdit()
        self.cep_input.setInputMask("99999-999")
        layout.addRow("CEP:", self.cep_input)
        
        # Logradouro
        self.logradouro_input = QLineEdit()
        self.logradouro_input.setMaxLength(200)
        layout.addRow("Logradouro:", self.logradouro_input)
        
        # Número
        self.numero_input = QLineEdit()
        self.numero_input.setMaxLength(10)
        layout.addRow("Número:", self.numero_input)
        
        # Complemento
        self.complemento_input = QLineEdit()
        self.complemento_input.setMaxLength(100)
        layout.addRow("Complemento:", self.complemento_input)
        
        # Bairro
        self.bairro_input = QLineEdit()
        self.bairro_input.setMaxLength(100)
        layout.addRow("Bairro:", self.bairro_input)
        
        # Cidade
        self.cidade_input = QLineEdit()
        self.cidade_input.setMaxLength(100)
        layout.addRow("Cidade:", self.cidade_input)
        
        # UF
        self.uf_combo = QComboBox()
        ufs = ["", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
               "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", 
               "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        self.uf_combo.addItems(ufs)
        layout.addRow("UF:", self.uf_combo)
        
        # Ponto de referência
        self.ponto_referencia_input = QLineEdit()
        self.ponto_referencia_input.setMaxLength(200)
        layout.addRow("Ponto de referência:", self.ponto_referencia_input)
        
        widget.setLayout(layout)
        return widget
    
    def create_dados_clinicos_tab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # Peso
        self.peso_input = QDoubleSpinBox()
        self.peso_input.setRange(0.0, 300.0)
        self.peso_input.setSuffix(" kg")
        self.peso_input.setDecimals(1)
        layout.addRow("Peso:", self.peso_input)
        
        # Altura
        self.altura_input = QDoubleSpinBox()
        self.altura_input.setRange(0.0, 2.5)
        self.altura_input.setSuffix(" m")
        self.altura_input.setDecimals(2)
        layout.addRow("Altura:", self.altura_input)
        
        # Tipo sanguíneo
        self.tipo_sanguineo_combo = QComboBox()
        tipos = ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        self.tipo_sanguineo_combo.addItems(tipos)
        layout.addRow("Tipo sanguíneo:", self.tipo_sanguineo_combo)
        
        # Alergias
        self.alergias_input = QTextEdit()
        self.alergias_input.setMaximumHeight(80)
        layout.addRow("Alergias:", self.alergias_input)
        
        # Medicamentos de uso contínuo
        self.medicamentos_input = QTextEdit()
        self.medicamentos_input.setMaximumHeight(80)
        layout.addRow("Medicamentos uso contínuo:", self.medicamentos_input)
        
        # Observações médicas
        self.observacoes_input = QTextEdit()
        self.observacoes_input.setMaximumHeight(100)
        layout.addRow("Observações médicas:", self.observacoes_input)
        
        widget.setLayout(layout)
        return widget
    
    def save_paciente(self):
        """Salva o paciente"""
        try:
            # Validações básicas
            if not self.nome_input.text().strip():
                QMessageBox.warning(self, "Atenção", "Nome é obrigatório!")
                return
            
            cpf = Formatters.clean_string(self.cpf_input.text())
            if not cpf or not Validators.validate_cpf(cpf):
                QMessageBox.warning(self, "Atenção", "CPF inválido!")
                return
            
            cns = Formatters.clean_string(self.cns_input.text())
            if not cns or not Validators.validate_cns(cns):
                QMessageBox.warning(self, "Atenção", "CNS inválido!")
                return
            
            # Preparar dados
            data = {
                'nome': self.nome_input.text().strip().upper(),
                'nome_social': self.nome_social_input.text().strip().upper() or None,
                'cpf': cpf,
                'cns': cns,
                'rg': self.rg_input.text().strip() or None,
                'data_nascimento': self.data_nascimento_input.date().toPyDate(),
                'sexo': self.sexo_combo.currentData(),
                'telefone': Formatters.clean_string(self.telefone_input.text()) or None,
                'celular': Formatters.clean_string(self.celular_input.text()) or None,
                'email': self.email_input.text().strip().lower() or None,
                'estado_civil': self.estado_civil_combo.currentData(),
                'escolaridade': self.escolaridade_combo.currentData(),
                'profissao': self.profissao_input.text().strip().upper() or None,
                'peso': self.peso_input.value() if self.peso_input.value() > 0 else None,
                'altura': self.altura_input.value() if self.altura_input.value() > 0 else None,
                'tipo_sanguineo': self.tipo_sanguineo_combo.currentText() or None,
                'alergias': self.alergias_input.toPlainText().strip() or None,
                'medicamentos_uso_continuo': self.medicamentos_input.toPlainText().strip() or None,
                'observacoes_medicas': self.observacoes_input.toPlainText().strip() or None,
            }
            
            # Dados do endereço
            if any([
                self.cep_input.text().strip(),
                self.logradouro_input.text().strip(),
                self.bairro_input.text().strip(),
                self.cidade_input.text().strip(),
                self.uf_combo.currentText()
            ]):
                data['endereco'] = {
                    'cep': Formatters.clean_string(self.cep_input.text()) or None,
                    'logradouro': self.logradouro_input.text().strip().upper() or None,
                    'numero': self.numero_input.text().strip() or None,
                    'complemento': self.complemento_input.text().strip().upper() or None,
                    'bairro': self.bairro_input.text().strip().upper() or None,
                    'cidade': self.cidade_input.text().strip().upper() or None,
                    'uf': self.uf_combo.currentText() or None,
                    'ponto_referencia': self.ponto_referencia_input.text().strip().upper() or None,
                }
            
            # Salvar
            self.save_button.setEnabled(False)
            self.save_button.setText("Salvando...")
            
            result = paciente_controller.create_paciente(data)
            
            if result["success"]:
                QMessageBox.information(self, "Sucesso", result["message"])
                self.accept()
            else:
                QMessageBox.critical(self, "Erro", result["message"])
        
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro interno: {str(e)}")
        
        finally:
            self.save_button.setEnabled(True)
            self.save_button.setText("Salvar")