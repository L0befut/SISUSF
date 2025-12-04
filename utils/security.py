# =============================================================================
# utils/security.py
# =============================================================================

import bcrypt
from config.settings import settings

class SecurityManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """Gera hash da senha"""
        salt = bcrypt.gensalt(rounds=settings.SALT_ROUNDS)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verifica se a senha confere com o hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))