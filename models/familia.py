# =============================================================================
# models/familia.py - VERSÃO CORRIGIDA
# =============================================================================
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

class Familia(Base):
    __tablename__ = "familias"
    
    # Campos básicos
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_familia = Column(String(20), unique=True, nullable=False, index=True)
    nome_responsavel = Column(String(200), nullable=False)
    cpf_responsavel = Column(String(11), nullable=False, index=True)
    
    # Endereço (referência para tabela de endereços)
    endereco_id = Column(Integer, ForeignKey("enderecos.id"), nullable=False)
    
    # Dados socioeconômicos
    renda_familiar = Column(Float, default=0.0)
    beneficiario_bolsa_familia = Column(Boolean, default=False)
    tipo_moradia = Column(String(50))  # Própria, Alugada, Cedida, etc.
    situacao_moradia = Column(String(100))  # Condições da habitação
    
    # Informações de saúde da família
    plano_saude_privado = Column(Boolean, default=False)
    observacoes = Column(Text)
    
    # Campos de auditoria
    ativo = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    updated_by = Column(String(100))
    
    # RELACIONAMENTOS CORRIGIDOS
    endereco = relationship("Endereco")
    membros = relationship("Paciente", backref="familia")
    
    def __repr__(self):
        return f"<Familia(codigo='{self.codigo_familia}', responsavel='{self.nome_responsavel}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo_familia': self.codigo_familia,
            'nome_responsavel': self.nome_responsavel,
            'cpf_responsavel': self.cpf_responsavel,
            'endereco_id': self.endereco_id,
            'renda_familiar': self.renda_familiar,
            'beneficiario_bolsa_familia': self.beneficiario_bolsa_familia,
            'tipo_moradia': self.tipo_moradia,
            'situacao_moradia': self.situacao_moradia,
            'plano_saude_privado': self.plano_saude_privado,
            'observacoes': self.observacoes,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by
        }