# =============================================================================
# db/manage_data.py
# =============================================================================
# -*- coding: utf-8 -*-
import os
import logging
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from db.connection import db_manager
from utils.security import SecurityManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def _is_production() -> bool:
    return os.getenv("APP_ENV", "development").lower() == "production"

def delete_all_users(force: bool = False) -> bool:
    if _is_production() and not force:
        logger.error("Refused to delete users in production environment without force=True.")
        return False
    try:
        with db_manager.engine.begin() as conn:
            conn.execute(text("DELETE FROM usuarios"))
        logger.info("🗑️ Todos os usuários foram deletados!")
        return True
    except Exception:
        logger.exception("❌ Erro ao deletar usuários:")
        return False

def update_user_email(old_email: str, new_email: str) -> bool:
    try:
        with db_manager.engine.begin() as conn:
            result = conn.execute(
                text("UPDATE usuarios SET email = :new_email WHERE email = :old_email"),
                {'new_email': new_email, 'old_email': old_email}
            )
        logger.info(f"✏️ Email do usuário {old_email} atualizado para {new_email} (linhas afetadas: {getattr(result, 'rowcount', 'n/a')})")
        return True
    except Exception:
        logger.exception("❌ Erro ao atualizar email:")
        return False

def create_user(
    nome: str,
    email: str,
    senha: str,
    cpf: str,
    tipo: str,
    ativo: bool = True,
    cns: Optional[str] = None,
    conselho_profissional: Optional[str] = None,
    created_by: str = 'Sistema'
) -> bool:
    senha_hash = SecurityManager.hash_password(senha)
    now = datetime.now(timezone.utc)

    sql = """
    INSERT INTO usuarios (
        nome, email, senha_hash, cpf, tipo, ativo,
        cns, conselho_profissional, created_by, created_at, updated_at
    ) VALUES (
        :nome, :email, :senha_hash, :cpf, :tipo, :ativo,
        :cns, :conselho_profissional, :created_by, :created_at, :updated_at
    )
    """

    params = {
        'nome': nome,
        'email': email,
        'senha_hash': senha_hash,
        'cpf': cpf,
        'tipo': tipo,
        'ativo': ativo,
        'cns': cns,
        'conselho_profissional': conselho_profissional,
        'created_by': created_by,
        'created_at': now,
        'updated_at': now
    }

    try:
        with db_manager.engine.begin() as conn:
            conn.execute(text(sql), params)
        logger.info(f"✅ Usuário {nome} criado com sucesso!")
        return True
    except IntegrityError:
        logger.exception("❌ Erro de integridade ao criar usuário (possível duplicidade):")
        return False
    except Exception:
        logger.exception("❌ Erro ao criar usuário:")
        return False

def create_seed_data() -> bool:
    users_to_create = [
        
    {
        'nome': 'Administrador',
        'email': 'admin@sisusf.com',
        'senha': 'admin123',
        'cpf': '00000000000',
        'tipo': 'ADMIN'
    },
    {
        'nome': 'Medico',
        'email': 'medico@sisusf.com',
        'senha': 'medico123',
        'cpf': '11111111111',
        'tipo': 'MEDICO',
        'cns': '123456789012345',
        'conselho_profissional': 'CRM-SP 123456'
    },
    {
        'nome': 'Enfermeiro',
        'email': 'enfermeiro@sisusf.com',
        'senha': 'enfermeiro123',
        'cpf': '22222222222',
        'tipo': 'ENFERMEIRO',
        'cns': '234567890123456',
        'conselho_profissional': 'COREN-SP 12345'
    },
    {
        'nome': 'Agente Comunitario',
        'email': 'acs@sisusf.com',
        'senha': 'acs123',
        'cpf': '33333333333',
        'tipo': 'ACS',
        'cns': '345678901234567'
    }
]

    sql = """
    INSERT INTO usuarios (
        nome, email, senha_hash, cpf, tipo, ativo,
        cns, conselho_profissional, created_by, created_at, updated_at
    ) VALUES (
        :nome, :email, :senha_hash, :cpf, :tipo, :ativo,
        :cns, :conselho_profissional, :created_by, :created_at, :updated_at
    )
    """

    success_count = 0
    skip_count = 0

    try:
        with db_manager.engine.connect() as conn:
            for user in users_to_create:
                senha_hash = SecurityManager.hash_password(user['senha'])
                now = datetime.now(timezone.utc)
                
                params = {
                    'nome': user['nome'],
                    'email': user['email'],
                    'senha_hash': senha_hash,
                    'cpf': user['cpf'],
                    'tipo': user['tipo'],
                    'ativo': True,
                    'cns': user.get('cns'),
                    'conselho_profissional': user.get('conselho_profissional'),
                    'created_by': 'Sistema',
                    'created_at': now,
                    'updated_at': now
                }
                
                try:
                    with conn.begin():
                        conn.execute(text(sql), params)
                    logger.info(f"✅ Usuário {user['nome']} ({user['email']}) criado com sucesso!")
                    success_count += 1
                except IntegrityError:
                    logger.warning(
                        "⚠️ Usuário já existe ou violação de integridade para %s. Pulando.",
                        user['email']
                    )
                    skip_count += 1
        
        logger.info(f"✅ Seed data concluído: {success_count} criados, {skip_count} pulados.")
        return True
    except Exception:
        logger.exception("❌ Erro ao criar seed data:")
        return False

if __name__ == "__main__":
    if not _is_production():
        delete_all_users(force=True)
        create_seed_data()
    else:
        logger.error("Execução abortada: APP_ENV=production. Para rodar, mude APP_ENV ou modifique este script.")