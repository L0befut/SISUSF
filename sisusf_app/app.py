# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Usuario, Paciente

app = Flask(__name__)
app.secret_key = 'chave_supersecreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o db aqui, passando o app
db.init_app(app)

from routes import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
