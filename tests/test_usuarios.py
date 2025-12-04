from db.connection import db_manager
from sqlalchemy import text

print("🔍 Verificando usuários no banco...\n")

with db_manager.engine.connect() as conn:
    result = conn.execute(text("SELECT email, nome, tipo, senha_hash FROM usuarios"))
    usuarios = result.fetchall()
    
    if not usuarios:
        print("❌ NENHUM USUÁRIO ENCONTRADO NO BANCO!")
        print("   Precisa rodar o manage_data.py pra criar os usuários")
    else:
        print(f"✅ {len(usuarios)} usuário(s) encontrado(s):\n")
        for user in usuarios:
            print(f"Email: {user[0]}")
            print(f"Nome: {user[1]}")
            print(f"Tipo: {user[2]}")
            print(f"Hash: {user[3][:30]}...")
            print("-" * 50)