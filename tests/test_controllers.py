from utils.security import SecurityManager

# A senha que você tá tentando
senha_digitada = "admin123"

# Pega o hash do banco (roda o teste_usuarios.py modificado abaixo primeiro)
# Vou te dar o código completo:

from db.connection import db_manager
from sqlalchemy import text

with db_manager.engine.connect() as conn:
    result = conn.execute(text("SELECT senha_hash FROM usuarios WHERE email = 'admin@sisusf.com'"))
    row = result.first()
    if row:
        senha_hash_do_banco = row[0]
        print(f"Hash do banco: {senha_hash_do_banco[:50]}...")
        
        # Testa se a senha bate
        resultado = SecurityManager.verify_password("admin123", senha_hash_do_banco)
        print(f"Senha 'admin123' confere? {resultado}")