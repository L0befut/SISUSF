# db/connection.py
# -*- coding: utf-8 -*-
"""
SISUSF - Gerenciador de conexão com DB.
Postgres preferencial, SQLite fallback.
Variáveis de ambiente:
  DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
  PG_RETRIES (int), PG_BACKOFF (float seconds), PG_TIMEOUT (int seconds)
  SISUSF_LOG_LEVEL (DEBUG/INFO/WARNING/ERROR)

Principais melhorias:
 - retries/backoff configuráveis
 - mensagens de erro granulares e sem vazar senha
 - usa engine.begin() ao executar PRAGMA/SET para evitar warnings de commit
 - health helpers
"""
from __future__ import annotations

# FORCE: ignorar qualquer DB_HOST externo — usar localhost (atende seu pedido)
# OBS: isso sobrescreve qualquer variável de ambiente DB_HOST na inicialização do processo.
import os
os.environ['DB_HOST'] = 'localhost'

import os
import sys
import time
import logging
from typing import Optional
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, ArgumentError, DBAPIError

# ---------------------------
# Locale / Encoding
# ---------------------------
# Prefer "C.UTF-8" quando disponível, senão tenta pt_BR, en_US, depois C
for candidate in ("C.UTF-8", "pt_BR.UTF-8", "en_US.UTF-8", "C"):
    try:
        os.environ.setdefault("LC_ALL", candidate)
        os.environ.setdefault("LANG", candidate)
        break
    except Exception:
        continue

# Força saída em UTF-8 quando possível
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ---------------------------
# Logging
# ---------------------------
logger = logging.getLogger("sisusf.db")
if not logger.handlers:
    handler = logging.StreamHandler()
    fmt = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)

log_level = os.getenv("SISUSF_LOG_LEVEL", "INFO").upper()
logger.setLevel(getattr(logging, log_level, logging.INFO))

# ---------------------------
# Helpers
# ---------------------------

def _mask_password(url: Optional[str], password: Optional[str]) -> str:
    if not url:
        return "<unavailable>"
    try:
        if password:
            return url.replace(password, "***")
    except Exception:
        pass
    return url


# ---------------------------
# Database manager
# ---------------------------
class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.database_type: Optional[str] = None

        # configurações de retry/backoff via env
        self.pg_retries = int(os.getenv("PG_RETRIES", "2"))
        try:
            self.pg_backoff = float(os.getenv("PG_BACKOFF", "0.5"))
        except Exception:
            self.pg_backoff = 0.5
        try:
            self.pg_connect_timeout = int(os.getenv("PG_TIMEOUT", "10"))
        except Exception:
            self.pg_connect_timeout = 10

        self._setup_database()

    def _setup_database(self) -> None:
        # tenta PostgreSQL primeiro
        if self._setup_postgresql():
            return

        # fallback para SQLite
        logger.info("FALLBACK: configurando SQLite como alternativa.")
        self._setup_sqlite()

    def _setup_postgresql(self) -> bool:
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "sisusf")
        db_user = os.getenv("DB_USER", "sisusf_adm")
        db_pass = os.getenv("DB_PASS", "AD0806")

        password_encoded = quote_plus(db_pass) if db_pass else ""
        database_url = f"postgresql://{db_user}:{password_encoded}@{db_host}:{db_port}/{db_name}"

        logger.info("Tentando PostgreSQL: %s@%s:%s/%s", db_user, db_host, db_port, db_name)

        last_exc = None
        # Tenta algumas vezes com backoff
        for attempt in range(1, self.pg_retries + 2):
            try:
                self.engine = create_engine(
                    database_url,
                    echo=False,
                    pool_size=5,
                    max_overflow=10,
                    pool_timeout=30,
                    pool_recycle=3600,
                    pool_pre_ping=True,
                    connect_args={
                        # psycopg2 accepts "connect_timeout"
                        "connect_timeout": int(self.pg_connect_timeout),
                        # application_name pode ser útil no server side
                        # não passamos client_encoding aqui para evitar warn; vamos usar engine.begin() para SET
                        "application_name": "SISUSF",
                    },
                )

                # Teste simples: abrir conexão e executar SELECT 1 dentro de begin() para evitar avisos sobre commit
                with self.engine.begin() as conn:
                    conn.execute(text("SELECT 1"))
                    # Forçar client_encoding dentro de transação evita warnings
                    conn.execute(text("SET client_encoding TO 'UTF8'"))

                self.SessionLocal = sessionmaker(
                    autocommit=False, autoflush=False, bind=self.engine
                )
                self.database_type = "postgresql"
                logger.info("Conexão PostgreSQL estabelecida com sucesso.")
                return True

            except OperationalError as oe:
                last_exc = oe
                # OperationalError tipicamente rede/driver/credenciais/timeout
                msg = str(oe).splitlines()[0]
                logger.warning(
                    "Tentativa %d/%d: falha operacional ao conectar PostgreSQL: %s",
                    attempt,
                    self.pg_retries + 1,
                    msg,
                )
            except ArgumentError as ae:
                last_exc = ae
                # URL mal formada ou argumentos inválidos — não adianta retry
                logger.error("Argumento inválido ao criar engine: %s", str(ae).splitlines()[0])
                break
            except DBAPIError as dbapi_exc:
                last_exc = dbapi_exc
                logger.error("Erro DBAPI ao testar conexão: %s", str(dbapi_exc).splitlines()[0])
            except Exception as exc:
                last_exc = exc
                logger.exception("Erro inesperado ao tentar conectar PostgreSQL: %s", exc)

            # backoff antes da próxima tentativa (exceto após última)
            if attempt < (self.pg_retries + 1):
                wait = self.pg_backoff * attempt
                logger.info("Aguardando %.2fs antes da próxima tentativa...", wait)
                time.sleep(wait)

        # todas tentativas falharam
        if last_exc is not None:
            logger.error(
                "Não foi possível conectar ao PostgreSQL após %d tentativas. Última exceção: %s",
                self.pg_retries + 1,
                repr(last_exc),
            )
        return False

    def _setup_sqlite(self) -> bool:
        try:
            os.makedirs("data", exist_ok=True)
            database_url = "sqlite:///data/sisusf.db"
            self.engine = create_engine(
                database_url,
                echo=False,
                connect_args={"check_same_thread": False, "timeout": 20},
            )

            # Aplicar pragmas dentro de begin() para evitar warnings sobre commit
            with self.engine.begin() as conn:
                # encoding só altera no momento de criação do arquivo DB
                # garantimos foreign_keys e journal_mode
                conn.execute(text("PRAGMA foreign_keys = ON"))
                conn.execute(text("PRAGMA journal_mode = WAL"))

            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )
            self.database_type = "sqlite"
            logger.info("SQLite configurado com sucesso (data/sisusf.db).")
            return True
        except Exception as e:
            logger.exception("Erro crítico ao configurar SQLite: %s", e)
            raise

    def get_session(self):
        if not self.SessionLocal:
            raise RuntimeError("SessionLocal não inicializada. Banco não disponível.")
        return self.SessionLocal()

    def test_connection(self) -> bool:
        if not self.engine:
            logger.error("test_connection: engine não está configurada.")
            return False
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.debug("test_connection: OK.")
            return True
        except OperationalError as oe:
            logger.warning("test_connection: falha operacional - %s", str(oe).splitlines()[0])
            return False
        except DBAPIError as dbapi_exc:
            logger.error("test_connection: erro DBAPI - %s", str(dbapi_exc).splitlines()[0])
            return False
        except Exception as exc:
            logger.exception("test_connection: erro inesperado - %s", exc)
            return False

    def get_database_info(self) -> dict:
        try:
            url_str = str(self.engine.url)
        except Exception:
            url_str = "<unavailable>"

        password = None
        try:
            password = getattr(self.engine.url, "password", None)
        except Exception:
            password = None

        masked = _mask_password(url_str, password)

        pool_size = None
        try:
            pool = getattr(self.engine, "pool", None)
            pool_size = getattr(pool, "size", None)
        except Exception:
            pool_size = None

        return {
            "type": self.database_type,
            "url": masked,
            "pool_size": pool_size,
            "echo": getattr(self.engine, "echo", False),
        }


# instância global
db_manager = DatabaseManager()


# helpers para frameworks (FastAPI/Flask)
def get_db():
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()


def init_database() -> bool:
    logger.info("🏥 SISUSF - Inicializando Banco de Dados")
    if not db_manager.test_connection():
        info = db_manager.get_database_info()
        logger.error("Inicialização falhou. Tipo detectado: %s ; URL: %s", info.get("type"), info.get("url"))
        return False

    info = db_manager.get_database_info()
    logger.info("Banco inicializado. Tipo: %s ; URL: %s", info.get("type"), info.get("url"))
    return True


if __name__ == "__main__":
    ok = init_database()
    if not ok:
        logger.error("Inicialização finalizada com ERRO. Verifique logs acima.")
        sys.exit(2)
    logger.info("Inicialização finalizada com sucesso.")
    sys.exit(0)
