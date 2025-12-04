# =============================================================================
# models/consulta.py
# =============================================================================

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from models.base import Base, AuditMixin
import enum

class TipoConsulta(enum.Enum):
    CONSULTA_MEDICA = "consulta_medica"
    CONSULTA_ENFERMAGEM = "consulta_enfermagem"
    VISITA_DOMICILIAR = "visita_domiciliar"
    PROCEDIMENTO = "procedimento"
    VACINACAO = "vacinacao"

class StatusConsulta(enum.Enum):
    AGENDADA = "agendada"
    REALIZADA = "realizada"
    CANCELADA = "cancelada"
    FALTOU = "faltou"

class Consulta(Base, AuditMixin):
    __tablename__ = 'consultas'
    
    id = Column(Integer, primary_key=True)
    
    # Dados da Consulta
    data_hora = Column(DateTime, nullable=False, index=True)
    tipo = Column(Enum(TipoConsulta), nullable=False)
    status = Column(Enum(StatusConsulta), default=StatusConsulta.AGENDADA)
    
    # Relacionamentos corrigidos
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    paciente = relationship("Paciente", backref="consultas")
    profissional_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    profissional = relationship("Usuario", backref="consultas_realizadas")
    
    # Dados Vitais
    pressao_arterial = Column(String(10))  # ex: 120/80
    temperatura = Column(Float)  # °C
    frequencia_cardiaca = Column(Integer)  # bpm
    peso = Column(Float)  # kg
    altura = Column(Float)  # metros
    saturacao_oxigenio = Column(Integer)  # %
    
    # Consulta
    queixa_principal = Column(Text)
    historia_doenca_atual = Column(Text)
    exame_fisico = Column(Text)
    hipotese_diagnostica = Column(Text)
    conduta = Column(Text)
    prescricao_medica = Column(Text)
    observacoes = Column(Text)
    
    # Próxima consulta
    retorno_em = Column(Integer)  # dias
    
    def __repr__(self):
        return f"<Consulta(paciente_id={self.paciente_id}, data={self.data_hora.date()})>"