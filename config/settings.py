# =============================================================================
# config/settings.py
# =============================================================================

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'sisusf')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '0806')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'sisusf-secret-key-2025')
    SALT_ROUNDS = 12
    
    # App
    APP_NAME = "SISUSF - Sistema de Saúde da Família"
    VERSION = "1.0.0"
    
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()