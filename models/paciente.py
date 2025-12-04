# =============================================================================
# models/paciente.py
# =============================================================================
from sqlalchemy import Column, String, Integer, Date, Boolean, DateTime, ForeignKey, Text, Enum, event
from sqlalchemy.orm import relationship, Session
from datetime import datetime, date
import enum
import re
from models.base import Base

# ========================
# ENUMS
# ========================
class Sexo(enum.Enum):
    MASCULINO = "M"
    FEMININO = "F"
    NAO_INFORMADO = "N"

class EstadoCivil(enum.Enum):
    SOLTEIRO = "Solteiro(a)"
    CASADO = "Casado(a)"
    DIVORCIADO = "Divorciado(a)"
    VIUVO = "Viúvo(a)"
    UNIAO_ESTAVEL = "União Estável"

class Escolaridade(enum.Enum):
    NAO_ALFABETIZADO = "Não Alfabetizado"
    ENSINO_FUNDAMENTAL_INCOMPLETO = "Ensino Fundamental Incompleto"
    ENSINO_FUNDAMENTAL_COMPLETO = "Ensino Fundamental Completo"
    ENSINO_MEDIO_INCOMPLETO = "Ensino Médio Incompleto"
    ENSINO_MEDIO_COMPLETO = "Ensino Médio Completo"
    ENSINO_SUPERIOR_INCOMPLETO = "Ensino Superior Incompleto"
    ENSINO_SUPERIOR_COMPLETO = "Ensino Superior Completo"
    POS_GRADUACAO = "Pós-Graduação"

class StatusPaciente(enum.Enum):
    RASCUNHO = "rascunho"
    ATIVO = "ativo"
    INATIVO = "inativo"

# ========================
# MIXIN DE AUDITORIA
# ========================
class AuditMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    updated_by = Column(String(100))

# ========================
# MODELO PACIENTE
# ========================
class Paciente(AuditMixin, Base):
    __tablename__ = "pacientes"

    # Identificação básica
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_completo = Column(String(200), nullable=False, index=True)
    nome_social = Column(String(200))
    cpf = Column(String(11), unique=True, index=True)
    cns = Column(String(15), unique=True, index=True)
    rg = Column(String(20))
    sexo = Column(Enum(Sexo, name="sexo_enum"), nullable=False)
    data_nascimento = Column(Date)

    # Documentos e identificação
    nome_mae = Column(String(200))
    nome_pai = Column(String(200))
    estado_civil = Column(Enum(EstadoCivil, name="estado_civil_enum"))
    profissao = Column(String(100))
    escolaridade = Column(Enum(Escolaridade, name="escolaridade_enum"))

    # Contato
    telefone = Column(String(15))
    celular = Column(String(15))
    email = Column(String(100))

    # Relacionamento familiar (FK opcional se tabela existir)
    familia_id = Column(Integer, ForeignKey("familias.id", ondelete="SET NULL"), nullable=True)
    responsavel_familia = Column(Boolean, default=False)

    # Endereço individual (FK opcional se tabela existir)
    endereco_id = Column(Integer, ForeignKey("enderecos.id", ondelete="SET NULL"), nullable=True)
    endereco = relationship("Endereco", back_populates="pacientes", passive_deletes=True)

    # Informações de saúde
    tipo_sanguineo = Column(String(10))
    alergias = Column(Text)
    medicamentos_uso_continuo = Column(Text)
    condicoes_cronicas = Column(Text)
    observacoes_medicas = Column(Text)

    # Situação no sistema
    ativo = Column(Boolean, default=True, nullable=False)
    status = Column(Enum(StatusPaciente, name="status_paciente_enum"), default=StatusPaciente.RASCUNHO, nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow, nullable=False)
    ultima_consulta = Column(DateTime, nullable=True)

    # ========================
    # MÉTODOS
    # ========================
    def __repr__(self):
        return f"<Paciente(id={self.id}, nome='{self.nome_completo}', status='{self.status.value}')>"

    @property
    def idade(self):
        """Calcula a idade do paciente"""
        if not self.data_nascimento:
            return None
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year
        if hoje < self.data_nascimento.replace(year=hoje.year):
            idade -= 1
        return idade

    def validar(self, forcar_completo=False):
        """Valida campos do paciente."""
        erros = []

        # Validações obrigatórias
        if forcar_completo or self.status == StatusPaciente.ATIVO:
            if not self.nome_completo or not self.nome_completo.strip():
                erros.append("O nome completo é obrigatório.")
            if not self.data_nascimento:
                erros.append("A data de nascimento é obrigatória.")
            if not self.sexo:
                erros.append("O sexo é obrigatório.")

        # CPF
        if self.cpf:
            cpf_limpo = re.sub(r"\D", "", self.cpf)
            if len(cpf_limpo) != 11 or not self._validar_cpf(cpf_limpo):
                erros.append("O CPF informado é inválido.")

        # Email
        if self.email and self.email.strip():
            if not re.match(r"^[^@]+@[^@]+\.[^@]+$", self.email):
                erros.append("O e-mail informado é inválido.")

        if erros:
            raise ValueError("; ".join(erros))

    @staticmethod
    def _validar_cpf(cpf):
        """Valida CPF usando algoritmo de dígitos verificadores."""
        if len(set(cpf)) == 1:
            return False
        def calc_dv(digs):
            s = sum(int(d)*w for d, w in zip(digs, range(len(digs)+1, 1, -1)))
            r = 11 - s % 11
            return r if r < 10 else 0
        dv1 = calc_dv(cpf[:9])
        dv2 = calc_dv(cpf[:9] + str(dv1))
        return cpf[-2:] == f"{dv1}{dv2}"

    def to_dict(self):
        """Converte o objeto para dicionário, tratando enums e datas."""
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        for key in ['sexo', 'estado_civil', 'escolaridade', 'status']:
            if data.get(key):
                data[key] = data[key].value

        for key in ['data_nascimento', 'data_cadastro', 'ultima_consulta', 'created_at', 'updated_at']:
            if data.get(key):
                data[key] = data[key].isoformat()

        data['idade'] = self.idade
        return data

# ========================
# LISTENER DE VALIDAÇÃO AUTOMÁTICA
# ========================
@event.listens_for(Session, "before_flush")
def validar_pacientes(session, flush_context, instances):
    for obj in session.new.union(session.dirty):
        if isinstance(obj, Paciente):
            try:
                obj.validar(forcar_completo=False)
            except ValueError as e:
                raise ValueError(f"Erro ao salvar paciente '{obj.nome_completo or 'Sem Nome'}': {e}")
