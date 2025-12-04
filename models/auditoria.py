# =============================================================================
# models/auditoria.py
# =============================================================================

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from models.base import Base
from datetime import datetime

class LogAuditoria(Base):
    __tablename__ = 'logs_auditoria'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer)
    usuario_nome = Column(String(200))
    acao = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN
    tabela = Column(String(50))
    registro_id = Column(Integer)
    dados_anteriores = Column(JSON)  # dados antes da alteração
    dados_novos = Column(JSON)  # dados após alteração
    ip_address = Column(String(45))
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    observacoes = Column(Text)
    
    def __repr__(self):
        return f"<LogAuditoria(usuario='{self.usuario_nome}', acao='{self.acao}')>"
