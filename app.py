import time
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import text

from config import Config
from modelos import db, Usuario, Paciente, Sintoma, Avaliacao

from rotas_auth import auth
from rotas_pacientes import pacientes_bp
from rotas_avaliacoes import avaliacoes_bp
from rotas_sintomas import sintomas_bp
from rotas_relatorios import relatorios_bp
from rotas_usuarios import usuarios_bp


login_manager = LoginManager()


@login_manager.user_loader
def carregar_usuario(user_id):
    return Usuario.query.get(int(user_id))


def esperar_banco(app):
    tentativas = 0
    while tentativas < 30:
        try:
            with app.app_context():
                db.session.execute(text('SELECT 1'))
            return True
        except Exception:
            tentativas = tentativas + 1
            time.sleep(2)
    return False


def criar_admin_padrao():
    admin = Usuario.query.filter_by(email='admin@sistema.com').first()
    if not admin:
        novo_admin = Usuario(
            nome='Administrador IBK',
            email='admin@sistema.com',
            senha_hash=generate_password_hash('admin123'),
            tipo='admin',
            cpf='000.000.000-00',
            ativo=True
        )
        db.session.add(novo_admin)
        db.session.commit()


def criar_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faça login para acessar esta página.'

    app.register_blueprint(auth)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(avaliacoes_bp)
    app.register_blueprint(sintomas_bp)
    app.register_blueprint(relatorios_bp)
    app.register_blueprint(usuarios_bp)

    esperar_banco(app)
    with app.app_context():
        db.create_all()
        criar_admin_padrao()

    return app


app = criar_app()


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))


@app.route('/dashboard')
@login_required
def dashboard():
    dados = {}
    if current_user.tipo == 'admin':
        dados['total_usuarios'] = Usuario.query.filter_by(ativo=True).count()
        dados['total_pacientes'] = Paciente.query.filter_by(ativo=True).count()
        dados['total_sintomas'] = Sintoma.query.filter_by(ativo=True).count()
        dados['total_avaliacoes'] = Avaliacao.query.count()
        dados['indicados'] = Avaliacao.query.filter_by(resultado='Indicado para Teste Genetico').count()
        dados['sem_indicacao'] = Avaliacao.query.filter_by(resultado='Sem Indicacao para Teste Genetico').count()
        dados['ultimas_avaliacoes'] = Avaliacao.query.order_by(Avaliacao.id.desc()).limit(5).all()
    elif current_user.tipo == 'profissional':
        dados['total_pacientes'] = Paciente.query.filter_by(usuario_id=current_user.id, ativo=True).count()
        dados['total_avaliacoes'] = Avaliacao.query.filter_by(usuario_id=current_user.id).count()
        dados['indicados'] = Avaliacao.query.filter_by(usuario_id=current_user.id, resultado='Indicado para Teste Genetico').count()
        dados['sem_indicacao'] = Avaliacao.query.filter_by(usuario_id=current_user.id, resultado='Sem Indicacao para Teste Genetico').count()
        dados['ultimas_avaliacoes'] = Avaliacao.query.filter_by(usuario_id=current_user.id).order_by(Avaliacao.id.desc()).limit(5).all()
    else:
        meus_pacientes = Paciente.query.filter_by(cpf=current_user.cpf).all()
        ids = []
        for p in meus_pacientes:
            ids.append(p.id)
        if ids:
            dados['minhas_avaliacoes'] = Avaliacao.query.filter(Avaliacao.paciente_id.in_(ids)).order_by(Avaliacao.id.desc()).all()
        else:
            dados['minhas_avaliacoes'] = []
    return render_template('dashboard.html', dados=dados)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
