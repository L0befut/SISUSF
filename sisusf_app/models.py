# sisusf_app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    id    = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    role  = db.Column(db.String(50), nullable=False, default='atendente')

class Paciente(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    nome            = db.Column(db.String(120), nullable=False)
    cpf             = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=True)
    contato         = db.Column(db.String(50), nullable=True)
    endereco        = db.Column(db.String(200), nullable=True)

class Profissional(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    nome     = db.Column(db.String(120), nullable=False)
    cargo    = db.Column(db.String(50), nullable=False)
    registro = db.Column(db.String(50), nullable=False)
