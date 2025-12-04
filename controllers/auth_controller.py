# =============================================================================
# controllers/auth_controller.py
# =============================================================================
from types import SimpleNamespace
from models.usuario import Usuario
from models.auditoria import LogAuditoria
from utils.security import SecurityManager
from db.connection import db_manager
from sqlalchemy.exc import OperationalError, DBAPIError


class AuthController:
    def __init__(self):
        self.current_user = None

    # ------------------------
    # Auxiliares
    # ------------------------
    def _log_auditoria(self, session, usuario_id=None, usuario_nome=None, acao="", ip_address=None, observacoes=""):
        """Cria log de auditoria, falhas não interrompem fluxo"""
        try:
            log = LogAuditoria(
                usuario_id=usuario_id,
                usuario_nome=usuario_nome,
                acao=acao,
                ip_address=ip_address,
                observacoes=observacoes
            )
            session.add(log)
            session.commit()
        except Exception:
            session.rollback()

    def _handle_exception(self, e, code="INTERNAL_ERROR", message="Erro interno"):
        """Formata exceção genérica"""
        return {
            "success": False,
            "message": message,
            "code": code,
            "detail": str(e)
        }

    # ------------------------
    # Login
    # ------------------------
    def login(self, email: str, password: str, ip_address: str = None) -> dict:
        """Realiza login com debug detalhado e tratamento de falhas."""
        try:
            with db_manager.get_session() as session:
                # -----------------------------
                # Busca usuário ativo
                # -----------------------------
                try:
                    user = session.query(Usuario).filter(
                        Usuario.email == email.lower(),
                        Usuario.ativo == True
                    ).first()
                    print(f"DEBUG: usuário carregado: {user}")
                except Exception as e:
                    print(f"DEBUG: erro ao buscar usuário: {repr(e)}")
                    return self._handle_exception(e, "DATA_ACCESS_ERROR", "Erro interno ao acessar dados")

                # Usuário não encontrado
                if not user:
                    self._log_auditoria(
                        session,
                        usuario_nome=email,
                        acao="LOGIN_FAILED_USER_NOT_FOUND",
                        ip_address=ip_address,
                        observacoes=f"Tentativa de login com email não cadastrado: {email}"
                    )
                    return {"success": False, "message": "Email não cadastrado", "code": "USER_NOT_FOUND"}

                # -----------------------------
                # Verifica senha
                # -----------------------------
                try:
                    senha_valida = SecurityManager.verify_password(password, getattr(user, "senha_hash", None))
                    if senha_valida is None:
                        raise ValueError("Senha hash não encontrada para o usuário")
                except Exception as e:
                    print(f"DEBUG: erro ao verificar senha: {repr(e)}")
                    return self._handle_exception(e, "AUTH_VALIDATION_ERROR", "Erro ao validar credenciais")

                if not senha_valida:
                    self._log_auditoria(
                        session,
                        usuario_id=getattr(user, "id", None),
                        usuario_nome=email,
                        acao="LOGIN_FAILED_INVALID_PASSWORD",
                        ip_address=ip_address,
                        observacoes=f"Senha inválida para o email: {email}"
                    )
                    return {"success": False, "message": "Senha incorreta", "code": "INVALID_PASSWORD"}

                # -----------------------------
                # Monta objeto user_data protegido
                # -----------------------------
                user_data = SimpleNamespace(
                    id=getattr(user, "id", None),
                    nome=getattr(user, "nome", None),
                    email=getattr(user, "email", None),
                    cpf=getattr(user, "cpf", None),
                    tipo=str(getattr(user, "tipo", None)) if getattr(user, "tipo", None) else None,
                    cns=getattr(user, "cns", None),
                    conselho_profissional=getattr(user, "conselho_profissional", None),
                    ativo=getattr(user, "ativo", None)
                )
                self.current_user = user_data

                # -----------------------------
                # Log de auditoria login bem-sucedido
                # -----------------------------
                self._log_auditoria(
                    session,
                    usuario_id=user_data.id,
                    usuario_nome=user_data.nome,
                    acao="LOGIN",
                    ip_address=ip_address,
                    observacoes="Login realizado com sucesso"
                )

                return {"success": True, "user": user_data, "message": "Login realizado com sucesso", "code": "OK"}

        except Exception as e:
            print(f"DEBUG: exceção geral no login: {repr(e)}")
            return self._handle_exception(e)

    # ------------------------
    # Logout
    # ------------------------
    def logout(self):
        """Realiza logout do usuário com log de auditoria"""
        if not self.current_user:
            return
        try:
            with db_manager.get_session() as session:
                self._log_auditoria(
                    session,
                    usuario_id=self.current_user.id,
                    usuario_nome=self.current_user.nome,
                    acao="LOGOUT",
                    observacoes="Logout realizado"
                )
        except Exception:
            pass
        finally:
            self.current_user = None

    # ------------------------
    # Autenticação / Permissões
    # ------------------------
    def is_authenticated(self) -> bool:
        return self.current_user is not None

    def has_permission(self, action: str) -> bool:
        """Verifica permissões do usuário"""
        if not self.current_user:
            return False

        permissions = {
            'admin': ['create', 'read', 'update', 'delete', 'report'],
            'medico': ['create', 'read', 'update', 'report'],
            'enfermeiro': ['create', 'read', 'update'],
            'agente': ['read', 'update']
        }

        role = str(self.current_user.tipo).lower()
        return action in permissions.get(role, [])


# Instância global
auth = AuthController()
