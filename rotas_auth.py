from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from modelos import db, Usuario

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha_hash, senha):
            if not usuario.ativo:
                flash('Usuario inativo. Procure o administrador.', 'erro')
                return redirect(url_for('auth.login'))
            login_user(usuario)
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha invalidos.', 'erro')
    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        current_user.nome = request.form.get('nome')
        nova_senha = request.form.get('nova_senha')
        senha_atual = request.form.get('senha_atual')
        if nova_senha:
            if check_password_hash(current_user.senha_hash, senha_atual):
                current_user.senha_hash = generate_password_hash(nova_senha)
                db.session.commit()
                flash('Dados e senha atualizados com sucesso.', 'sucesso')
            else:
                flash('Senha atual incorreta. A senha nao foi alterada.', 'erro')
        else:
            db.session.commit()
            flash('Dados atualizados com sucesso.', 'sucesso')
        return redirect(url_for('auth.perfil'))
    return render_template('perfil.html')
