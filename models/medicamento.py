# =============================================================================
# models/medicamento.py
# =============================================================================

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base, AuditMixin

class Medicamento(Base, AuditMixin):
    __tablename__ = 'medicamentos'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False, index=True)
    principio_ativo = Column(String(200))
    concentracao = Column(String(50))
    forma_farmaceutica = Column(String(50))  # comprimido, xarope, etc.
    fabricante = Column(String(100))
    lote = Column(String(50))
    validade = Column(DateTime)
    estoque_atual = Column(Integer, default=0)
    estoque_minimo = Column(Integer, default=10)
    ativo = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Medicamento(nome='{self.nome}', estoque={self.estoque_atual})>"

class DispensacaoMedicamento(Base, AuditMixin):
    __tablename__ = 'dispensacoes'
    
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    medicamento_id = Column(Integer, ForeignKey('medicamentos.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_dispensacao = Column(DateTime, nullable=False)
    profissional_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    observacoes = Column(Text)
    
    # Relacionamentos com backrefs únicos
    paciente = relationship("Paciente", backref="dispensacoes_recebidas")
    medicamento = relationship("Medicamento", backref="dispensacoes_realizadas")
    profissional = relationship("Usuario", backref="dispensacoes_feitas")
    
    def __repr__(self):
        return f"<DispensacaoMedicamento(paciente_id={self.paciente_id}, medicamento_id={self.medicamento_id}, qtd={self.quantidade})>"