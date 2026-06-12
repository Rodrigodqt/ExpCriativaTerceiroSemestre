from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from modelos import db, Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuarios_bp.route('/')
@login_required
def listar():
    if current_user.tipo != 'admin':
        abort(403)
    usuarios = Usuario.query.filter_by(ativo=True).order_by(Usuario.nome).all()
    return render_template('usuarios/listar.html', usuarios=usuarios)


@usuarios_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if current_user.tipo != 'admin':
        abort(403)
    if request.method == 'POST':
        email = request.form.get('email')
        existe = Usuario.query.filter_by(email=email).first()
        if existe:
            flash('Ja existe um usuario com este email.', 'erro')
            return render_template('usuarios/form.html', usuario=None)
        usuario = Usuario(
            nome=request.form.get('nome'),
            email=email,
            senha_hash=generate_password_hash(request.form.get('senha')),
            tipo=request.form.get('tipo'),
            cpf=request.form.get('cpf'),
            crm=request.form.get('crm') or None,
            especialidade=request.form.get('especialidade') or None,
            ativo=True
        )
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario cadastrado com sucesso.', 'sucesso')
        return redirect(url_for('usuarios.listar'))
    return render_template('usuarios/form.html', usuario=None)


@usuarios_bp.route('/editar/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def editar(usuario_id):
    if current_user.tipo != 'admin':
        abort(403)
    usuario = Usuario.query.get_or_404(usuario_id)
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.tipo = request.form.get('tipo')
        usuario.cpf = request.form.get('cpf')
        usuario.crm = request.form.get('crm') or None
        usuario.especialidade = request.form.get('especialidade') or None
        nova_senha = request.form.get('senha')
        if nova_senha:
            usuario.senha_hash = generate_password_hash(nova_senha)
        db.session.commit()
        flash('Usuario atualizado com sucesso.', 'sucesso')
        return redirect(url_for('usuarios.listar'))
    return render_template('usuarios/form.html', usuario=usuario)


@usuarios_bp.route('/excluir/<int:usuario_id>', methods=['POST'])
@login_required
def excluir(usuario_id):
    if current_user.tipo != 'admin':
        abort(403)
    usuario = Usuario.query.get_or_404(usuario_id)
    if usuario.id == current_user.id:
        flash('Voce nao pode remover o proprio usuario.', 'erro')
        return redirect(url_for('usuarios.listar'))
    usuario.ativo = False
    db.session.commit()
    flash('Usuario removido com sucesso.', 'sucesso')
    return redirect(url_for('usuarios.listar'))
