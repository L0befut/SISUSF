# =============================================================================
# models/endereco.py - VERSÃO CORRIGIDA
# =============================================================================
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base, AuditMixin

class Endereco(Base, AuditMixin):
    __tablename__ = 'enderecos'
    
    id = Column(Integer, primary_key=True)
    cep = Column(String(8), nullable=False)
    logradouro = Column(String(200), nullable=False)
    numero = Column(String(10))
    complemento = Column(String(100))
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    uf = Column(String(2), nullable=False)
    ponto_referencia = Column(String(200))
    
    # RELACIONAMENTOS CORRIGIDOS - SEM back_populates
    # Deixar o SQLAlchemy gerenciar automaticamente
    def __repr__(self):
        return f"<Endereco(logradouro='{self.logradouro}', cidade='{self.cidade}')>"