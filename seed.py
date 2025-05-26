# seed.py

from sisusf_app.app import app, db
from sisusf_app.models import Usuario, Paciente, Profissional
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = Usuario(
        login='admin',
        senha=generate_password_hash('admin123'),
        role='admin'
    )
    paciente = Paciente(
        nome='Ricardo Emanuel de Assis Bispo',
        cpf='123.456.789-00'
    )
    profissional = Profissional(
        nome='Daniela Cristina de Assis dos Santos',
        cargo='enfermeira',
        registro='COREN12345'
    )

    db.session.add_all([admin, paciente, profissional])
    db.session.commit()
    print('Seed concluído com sucesso!')
