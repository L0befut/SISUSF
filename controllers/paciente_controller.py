# =============================================================================
# controllers/paciente_controller.py
# =============================================================================
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from models.paciente import Paciente
from models.endereco import Endereco
from models.auditoria import LogAuditoria
from utils.validators import Validators
from db.connection import db_manager
from controllers.auth_controller import auth
from datetime import datetime
import re

class PacienteController:

    def create_paciente(self, data: dict) -> dict:
        """Cria novo paciente"""
        if not auth.has_permission('create'):
            return {"success": False, "message": "Sem permissão para criar pacientes"}

        session = db_manager.get_session()
        try:
            # Validações
            if not Validators.validate_cpf(data.get('cpf', '')):
                return {"success": False, "message": "CPF inválido"}
            if not Validators.validate_cns(data.get('cns', '')):
                return {"success": False, "message": "CNS inválido"}

            # Verificar duplicatas
            existing = session.query(Paciente).filter(
                or_(
                    Paciente.cpf == data['cpf'],
                    Paciente.cns == data['cns']
                )
            ).first()
            if existing:
                return {"success": False, "message": "CPF ou CNS já cadastrado"}

            # Criar endereço se fornecido
            endereco = None
            if data.get('endereco'):
                endereco = Endereco(**data['endereco'])
                session.add(endereco)
                session.flush()

            paciente_data = data.copy()
            paciente_data.pop('endereco', None)

            paciente = Paciente(
                **paciente_data,
                endereco_id=endereco.id if endereco else None,
                created_by=auth.current_user.nome
            )

            session.add(paciente)
            session.commit()

            # Log auditoria
            log = LogAuditoria(
                usuario_id=auth.current_user.id,
                usuario_nome=auth.current_user.nome,
                acao="CREATE",
                tabela="pacientes",
                registro_id=paciente.id,
                dados_novos={"nome": paciente.nome, "cpf": paciente.cpf}
            )
            session.add(log)
            session.commit()

            return {"success": True, "message": "Paciente cadastrado com sucesso", "paciente_id": paciente.id}

        except Exception as e:
            session.rollback()
            return {"success": False, "message": f"Erro ao cadastrar paciente: {str(e)}"}
        finally:
            session.close()

    def search_pacientes(self, query: str, limit: int = 50) -> list:
        """Busca pacientes por nome, CPF ou CNS"""
        if not auth.has_permission('read'):
            return []

        session = db_manager.get_session()
        try:
            clean_query = re.sub(r'\D', '', query) if query else ''
            pacientes = session.query(Paciente).filter(
                and_(
                    Paciente.ativo == True,
                    or_(
                        Paciente.nome.ilike(f'%{query}%'),
                        Paciente.cpf == clean_query,
                        Paciente.cns == clean_query
                    )
                )
            ).limit(limit).all()
            return pacientes
        except Exception as e:
            print(f"Erro na busca: {e}")
            return []
        finally:
            session.close()

    def get_paciente_by_id(self, paciente_id: int) -> dict:
        if not auth.has_permission('read'):
            return {"success": False, "message": "Sem permissão"}

        session = db_manager.get_session()
        try:
            paciente = session.query(Paciente).filter(
                Paciente.id == paciente_id,
                Paciente.ativo == True
            ).first()
            if not paciente:
                return {"success": False, "message": "Paciente não encontrado"}
            return {"success": True, "paciente": paciente}
        except Exception as e:
            return {"success": False, "message": f"Erro: {str(e)}"}
        finally:
            session.close()

    def update_paciente(self, paciente_id: int, data: dict) -> dict:
        if not auth.has_permission('update'):
            return {"success": False, "message": "Sem permissão"}

        session = db_manager.get_session()
        try:
            paciente = session.query(Paciente).filter(
                Paciente.id == paciente_id,
                Paciente.ativo == True
            ).first()
            if not paciente:
                return {"success": False, "message": "Paciente não encontrado"}

            dados_anteriores = {"nome": paciente.nome, "cpf": paciente.cpf, "telefone": paciente.telefone}

            for key, value in data.items():
                if hasattr(paciente, key) and key != 'id':
                    setattr(paciente, key, value)

            paciente.updated_by = auth.current_user.nome
            session.commit()

            log = LogAuditoria(
                usuario_id=auth.current_user.id,
                usuario_nome=auth.current_user.nome,
                acao="UPDATE",
                tabela="pacientes",
                registro_id=paciente.id,
                dados_anteriores=dados_anteriores,
                dados_novos={"nome": paciente.nome, "cpf": paciente.cpf}
            )
            session.add(log)
            session.commit()

            return {"success": True, "message": "Paciente atualizado com sucesso"}

        except Exception as e:
            session.rollback()
            return {"success": False, "message": f"Erro: {str(e)}"}
        finally:
            session.close()

# Instância global
paciente_controller = PacienteController()
