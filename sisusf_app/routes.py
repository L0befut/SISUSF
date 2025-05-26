# sisusf_app/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .app import app, login_manager
from .models import db, Usuario, Paciente, Profissional
from .forms import LoginForm, PacienteForm
from werkzeug.security import generate_password_hash, check_password_hash
import re

# user_loader
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# home → redireciona
@app.route('/')
def index():
    return redirect(url_for('login'))

# login
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(login=form.login.data).first()
        if user and check_password_hash(user.senha, form.senha.data):
            login_user(user)
            flash('Bem-vindo, {}'.format(user.login), 'success')
            next_page = request.args.get('next') or url_for('listar_pacientes')
            return redirect(next_page)
        flash('Login ou senha incorretos.', 'danger')
    return render_template('login.html', form=form)

# logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu.', 'info')
    return redirect(url_for('login'))

# listar pacientes
@app.route('/pacientes')
@login_required
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes/listar.html', pacientes=pacientes)

# validar CPF (usado na rota de criação)
def validate_cpf(cpf):
    return bool(re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf))

# novo paciente
@app.route('/pacientes/novo', methods=['GET','POST'])
@login_required
def novo_paciente():
    if current_user.role not in ['admin','enfermeiro']:
        flash('Acesso negado.', 'warning')
        return redirect(url_for('listar_pacientes'))
    form = PacienteForm()
    if form.validate_on_submit():
        if not validate_cpf(form.cpf.data):
            flash('CPF em formato inválido.', 'danger')
            return redirect(url_for('novo_paciente'))
        p = Paciente(
            nome=form.nome.data,
            cpf=form.cpf.data,
            data_nascimento=form.data_nascimento.data,
            contato=form.contato.data,
            endereco=form.endereco.data
        )
        db.session.add(p)
        db.session.commit()
        flash('Paciente cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_pacientes'))
    return render_template('pacientes/form.html', form=form)
