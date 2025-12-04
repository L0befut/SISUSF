# =============================================================================
# db/create_tables.py
# =============================================================================
# -*- coding: utf-8 -*-

import sys
import traceback
from sqlalchemy import text
from db.connection import db_manager
from models.base import Base

# Importar todas as models **antes** de criar as tabelas
import models.usuario
import models.paciente
import models.endereco
import models.familia
import models.consulta
import models.medicamento
import models.auditoria

# Configurar UTF-8 para o sistema
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def configure_database_encoding():
    """Configura o encoding do banco de dados"""
    try:
        with db_manager.engine.connect() as conn:
            url = str(db_manager.engine.url).lower()
            if 'sqlite' in url:
                conn.execute(text("PRAGMA encoding = 'UTF-8'"))
                conn.execute(text("PRAGMA foreign_keys = ON"))
            elif 'mysql' in url:
                conn.execute(text("SET NAMES utf8mb4"))
                conn.execute(text("SET CHARACTER SET utf8mb4"))
                conn.execute(text("SET character_set_connection=utf8mb4"))
            elif 'postgresql' in url:
                conn.execute(text("SET CLIENT_ENCODING TO 'UTF8'"))
            conn.commit()
            print("✅ Encoding do banco configurado")
    except Exception as e:
        print(f"⚠️ Aviso ao configurar encoding: {e}")

def check_database_connection():
    """Verifica se a conexão com o banco está OK"""
    try:
        with db_manager.engine.connect() as conn:
            conn.execute(text("SELECT 1")).fetchone()
        print("✅ Conexão com banco OK")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def create_all_tables():
    """Cria todas as tabelas do banco de dados de forma segura"""
    try:
        print("🔧 Configurando encoding do banco...")
        configure_database_encoding()

        print("📋 Criando todas as tabelas...")
        Base.metadata.create_all(db_manager.engine)
        print("✅ Todas as tabelas foram criadas com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        print("📋 Traceback completo:")
        traceback.print_exc()
        return False

def drop_all_tables():
    """Remove todas as tabelas (CUIDADO!)"""
    try:
        Base.metadata.drop_all(db_manager.engine)
        print("⚠️ Todas as tabelas foram removidas")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover tabelas: {e}")
        return False

def reset_database():
    """Remove e recria todas as tabelas"""
    print("🔄 Resetando banco de dados...")
    if drop_all_tables():
        return create_all_tables()
    return False

if __name__ == "__main__":
    print("🏥 SISUSF - Criação de Tabelas")
    print("=" * 50)

    if not check_database_connection():
        sys.exit(1)

    if create_all_tables():
        print("🎉 Processo concluído com sucesso!")
    else:
        print("❌ Processo falhou. Verifique os erros acima.")
        sys.exit(1)
