# =============================================================================
# models/base.py
# =============================================================================

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime

Base = declarative_base()

class AuditMixin:
    """Mixin para auditoria automática"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(100))
    updated_by = Column(String(100))

    