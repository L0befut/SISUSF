# routes.py

# Importa o app, o banco e os modelos
from app import app, db
from flask import render_template, request, redirect, url_for, session
from models import Usuario, Paciente

# Página inicial (redireciona pro login)
@app.route('/')
def index():
    return redirect(url_for('login'))

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario.query.filter_by(login=request.form['login']).first()
        if usuario and usuario.senha == request.form['senha']:
            session['usuario'] = usuario.login
            return redirect(url_for('listar_pacientes'))
    return render_template('login.html')

# Lista os pacientes (ainda básico)
@app.route('/pacientes')
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes.html', pacientes=pacientes)

# Adiciona um novo paciente
@app.route('/pacientes/novo', methods=['POST'])
def novo_paciente():
    nome = request.form['nome']
    cpf = request.form['cpf']
    paciente = Paciente(nome=nome, cpf=cpf)
    db.session.add(paciente)
    db.session.commit()
    return redirect(url_for('listar_pacientes'))
