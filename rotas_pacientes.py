from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user

from modelos import db, Paciente

pacientes_bp = Blueprint('pacientes', __name__, url_prefix='/pacientes')


def converter_data(texto):
    if not texto:
        return None
    try:
        return datetime.strptime(texto, '%Y-%m-%d').date()
    except ValueError:
        return None


@pacientes_bp.route('/')
@login_required
def listar():
    if current_user.tipo == 'paciente':
        abort(403)
    if current_user.tipo == 'admin':
        pacientes = Paciente.query.filter_by(ativo=True).order_by(Paciente.nome).all()
    else:
        pacientes = Paciente.query.filter_by(ativo=True, usuario_id=current_user.id).order_by(Paciente.nome).all()
    return render_template('pacientes/listar.html', pacientes=pacientes)


@pacientes_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if current_user.tipo == 'paciente':
        abort(403)
    if request.method == 'POST':
        nome = request.form.get('nome')
        if not nome:
            flash('O nome do paciente e obrigatorio.', 'erro')
            return render_template('pacientes/form.html', paciente=None)
        paciente = Paciente(
            nome=nome,
            data_nascimento=converter_data(request.form.get('data_nascimento')),
            sexo=request.form.get('sexo'),
            cpf=request.form.get('cpf'),
            contato=request.form.get('contato'),
            historico_familiar=request.form.get('historico_familiar'),
            usuario_id=current_user.id,
            ativo=True
        )
        db.session.add(paciente)
        db.session.commit()
        flash('Paciente cadastrado com sucesso.', 'sucesso')
        return redirect(url_for('pacientes.listar'))
    return render_template('pacientes/form.html', paciente=None)


@pacientes_bp.route('/editar/<int:paciente_id>', methods=['GET', 'POST'])
@login_required
def editar(paciente_id):
    if current_user.tipo == 'paciente':
        abort(403)
    paciente = Paciente.query.get_or_404(paciente_id)
    if current_user.tipo == 'profissional' and paciente.usuario_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        paciente.nome = request.form.get('nome')
        paciente.data_nascimento = converter_data(request.form.get('data_nascimento'))
        paciente.sexo = request.form.get('sexo')
        paciente.cpf = request.form.get('cpf')
        paciente.contato = request.form.get('contato')
        paciente.historico_familiar = request.form.get('historico_familiar')
        db.session.commit()
        flash('Paciente atualizado com sucesso.', 'sucesso')
        return redirect(url_for('pacientes.listar'))
    return render_template('pacientes/form.html', paciente=paciente)


@pacientes_bp.route('/detalhes/<int:paciente_id>')
@login_required
def detalhes(paciente_id):
    if current_user.tipo == 'paciente':
        abort(403)
    paciente = Paciente.query.get_or_404(paciente_id)
    if current_user.tipo == 'profissional' and paciente.usuario_id != current_user.id:
        abort(403)
    return render_template('pacientes/detalhes.html', paciente=paciente)


@pacientes_bp.route('/excluir/<int:paciente_id>', methods=['POST'])
@login_required
def excluir(paciente_id):
    if current_user.tipo == 'paciente':
        abort(403)
    paciente = Paciente.query.get_or_404(paciente_id)
    if current_user.tipo == 'profissional' and paciente.usuario_id != current_user.id:
        abort(403)
    paciente.ativo = False
    db.session.commit()
    flash('Paciente removido com sucesso.', 'sucesso')
    return redirect(url_for('pacientes.listar'))
