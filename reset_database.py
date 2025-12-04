#!/usr/bin/env python3
"""
Script para resetar o banco de dados SISUSF
Execute: python reset_database.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from db.connection import db_manager

def reset_database():
    """Remove todas as tabelas e tipos do banco"""
    
    print("🗑️ Resetando banco de dados...")
    
    try:
        with db_manager.engine.begin() as conn:
            # Remover tabelas
            tables_to_drop = [
                'dispensacoes',
                'consultas', 
                'pacientes',
                'familias',
                'usuarios',
                'medicamentos',
                'logs_auditoria',
                'enderecos'
            ]
            
            for table in tables_to_drop:
                try:
                    conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                    print(f"✅ Tabela {table} removida")
                except Exception as e:
                    print(f"⚠️ Erro ao remover tabela {table}: {e}")
            
            # Remover tipos ENUM
            enums_to_drop = [
                'tipousuario',
                'sexo', 
                'tipoconsulta'
            ]
            
            for enum_type in enums_to_drop:
                try:
                    conn.execute(text(f"DROP TYPE IF EXISTS {enum_type} CASCADE"))
                    print(f"✅ Tipo {enum_type} removido")
                except Exception as e:
                    print(f"⚠️ Erro ao remover tipo {enum_type}: {e}")
        
        print("\n✅ Banco resetado com sucesso!")
        print("🚀 Agora execute: python run.py")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao resetar banco: {e}")
        return False

if __name__ == "__main__":
    reset_database()