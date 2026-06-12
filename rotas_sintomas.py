from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user

from modelos import db, Sintoma

sintomas_bp = Blueprint('sintomas', __name__, url_prefix='/sintomas')


@sintomas_bp.route('/')
@login_required
def listar():
    if current_user.tipo != 'admin':
        abort(403)
    sintomas = Sintoma.query.order_by(Sintoma.ordem).all()
    return render_template('sintomas/listar.html', sintomas=sintomas)


@sintomas_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if current_user.tipo != 'admin':
        abort(403)
    if request.method == 'POST':
        peso_feminino = request.form.get('peso_feminino')
        sintoma = Sintoma(
            nome=request.form.get('nome'),
            descricao=request.form.get('descricao'),
            categoria=request.form.get('categoria'),
            peso_masculino=float(request.form.get('peso_masculino') or 0),
            peso_feminino=float(peso_feminino) if peso_feminino else None,
            ordem=int(request.form.get('ordem') or 0),
            ativo=True
        )
        db.session.add(sintoma)
        db.session.commit()
        flash('Sintoma cadastrado com sucesso.', 'sucesso')
        return redirect(url_for('sintomas.listar'))
    return render_template('sintomas/form.html', sintoma=None)


@sintomas_bp.route('/editar/<int:sintoma_id>', methods=['GET', 'POST'])
@login_required
def editar(sintoma_id):
    if current_user.tipo != 'admin':
        abort(403)
    sintoma = Sintoma.query.get_or_404(sintoma_id)
    if request.method == 'POST':
        peso_feminino = request.form.get('peso_feminino')
        sintoma.nome = request.form.get('nome')
        sintoma.descricao = request.form.get('descricao')
        sintoma.categoria = request.form.get('categoria')
        sintoma.peso_masculino = float(request.form.get('peso_masculino') or 0)
        sintoma.peso_feminino = float(peso_feminino) if peso_feminino else None
        sintoma.ordem = int(request.form.get('ordem') or 0)
        db.session.commit()
        flash('Sintoma atualizado com sucesso.', 'sucesso')
        return redirect(url_for('sintomas.listar'))
    return render_template('sintomas/form.html', sintoma=sintoma)


@sintomas_bp.route('/excluir/<int:sintoma_id>', methods=['POST'])
@login_required
def excluir(sintoma_id):
    if current_user.tipo != 'admin':
        abort(403)
    sintoma = Sintoma.query.get_or_404(sintoma_id)
    sintoma.ativo = False
    db.session.commit()
    flash('Sintoma removido com sucesso.', 'sucesso')
    return redirect(url_for('sintomas.listar'))
