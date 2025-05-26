# sisusf_app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    login  = StringField('Usuário', validators=[DataRequired()])
    senha  = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class PacienteForm(FlaskForm):
    nome            = StringField('Nome', validators=[DataRequired(), Length(max=120)])
    cpf             = StringField('CPF', validators=[DataRequired(), Length(max=14)])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d')
    contato         = StringField('Contato', validators=[Length(max=50)])
    endereco        = StringField('Endereço', validators=[Length(max=200)])
    submit          = SubmitField('Salvar')
