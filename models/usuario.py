import enum
from datetime import datetime
from sqlalchemy import Column, String, Enum, Integer, Boolean, DateTime
from sqlalchemy.orm import validates, declarative_base
import bcrypt

Base = declarative_base()

# ========================
# ENUMS
# ========================
class TipoUsuario(enum.Enum):
    ADMIN = "ADMIN"
    PACIENTE = "PACIENTE"
    MEDICO = "MEDICO"
    ENFERMEIRO = "ENFERMEIRO"
    ACS = "ACS"  # Agente Comunitário de Saúde

# ========================
# MODELO USUARIO
# ========================
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    tipo = Column(Enum(TipoUsuario, name="tipo_usuario"), nullable=False)
    cpf = Column(String(11), nullable=False)  # CPF sem máscara
    ativo = Column(Boolean, default=True, nullable=False)
    cns = Column(String(15))
    conselho_profissional = Column(String(20))

    # Auditoria
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    updated_by = Column(String(100))

    # ========================
    # Validações
    # ========================
    @validates('email')
    def validate_email(self, key, endereco):
        if not endereco or '@' not in endereco:
            raise ValueError("Email inválido ou vazio.")
        return endereco.lower()

    @validates('tipo')
    def validate_tipo(self, key, tipo):
        if tipo is None:
            raise ValueError("Tipo de usuário é obrigatório.")
        if not isinstance(tipo, TipoUsuario):
            raise ValueError("Tipo de usuário inválido.")
        return tipo

    @validates('senha_hash')
    def validate_senha_hash(self, key, senha):
        if not senha:
            raise ValueError("Senha inválida ou vazia.")
        return senha

    # ========================
    # Métodos de senha
    # ========================
    def definir_senha(self, senha: str):
        """Gera o hash da senha usando bcrypt"""
        if not senha:
            raise ValueError("Senha não pode ser vazia.")
        hash_bytes = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        self.senha_hash = hash_bytes.decode('utf-8')

    def verificar_senha(self, senha: str) -> bool:
        """Verifica se a senha em texto simples corresponde ao hash armazenado"""
        if not self.senha_hash or not senha:
            return False
        senha_bytes = senha.encode('utf-8')
        hash_bytes = self.senha_hash.encode('utf-8')
        return bcrypt.checkpw(senha_bytes, hash_bytes)

    # ========================
    # Representação
    # ========================
    def __repr__(self):
        return f"<Usuario(id={self.id}, nome='{self.nome}', email='{self.email}', tipo='{self.tipo.value}', ativo={self.ativo})>"
