from db.connection import db_manager
from sqlalchemy import text

with db_manager.engine.connect() as conn:
    result = conn.execute(text("SELECT email, nome, tipo FROM usuarios"))
    for row in result:
        print(f"Email: {row[0]} | Nome: {row[1]} | Tipo: {row[2]}")