from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user

from modelos import db, Paciente, Sintoma, Avaliacao, ItemAvaliacao

avaliacoes_bp = Blueprint('avaliacoes', __name__, url_prefix='/avaliacoes')


@avaliacoes_bp.route('/')
@login_required
def listar():
    if current_user.tipo == 'paciente':
        abort(403)
    if current_user.tipo == 'admin':
        avaliacoes = Avaliacao.query.order_by(Avaliacao.id.desc()).all()
    else:
        avaliacoes = Avaliacao.query.filter_by(usuario_id=current_user.id).order_by(Avaliacao.id.desc()).all()
    return render_template('avaliacoes/listar.html', avaliacoes=avaliacoes)


@avaliacoes_bp.route('/selecionar')
@login_required
def selecionar():
    if current_user.tipo == 'paciente':
        abort(403)
    if current_user.tipo == 'admin':
        pacientes = Paciente.query.filter_by(ativo=True).order_by(Paciente.nome).all()
    else:
        pacientes = Paciente.query.filter_by(ativo=True, usuario_id=current_user.id).order_by(Paciente.nome).all()
    return render_template('avaliacoes/selecionar.html', pacientes=pacientes)


@avaliacoes_bp.route('/nova/<int:paciente_id>', methods=['GET', 'POST'])
@login_required
def nova(paciente_id):
    if current_user.tipo == 'paciente':
        abort(403)
    paciente = Paciente.query.get_or_404(paciente_id)
    if current_user.tipo == 'profissional' and paciente.usuario_id != current_user.id:
        abort(403)

    if paciente.sexo == 'F':
        sintomas = Sintoma.query.filter(Sintoma.ativo == True, Sintoma.peso_feminino != None).order_by(Sintoma.ordem).all()
    else:
        sintomas = Sintoma.query.filter_by(ativo=True).order_by(Sintoma.ordem).all()

    if request.method == 'POST':
        marcados = request.form.getlist('sintomas')
        score = 0.0
        for sintoma in sintomas:
            if str(sintoma.id) in marcados:
                if paciente.sexo == 'M':
                    score = score + sintoma.peso_masculino
                else:
                    score = score + sintoma.peso_feminino
        score = round(score, 2)

        if paciente.sexo == 'M':
            limiar = 0.56
        else:
            limiar = 0.55

        if score > limiar:
            resultado = 'Indicado para Teste Genetico'
        else:
            resultado = 'Sem Indicacao para Teste Genetico'

        avaliacao = Avaliacao(
            paciente_id=paciente.id,
            usuario_id=current_user.id,
            score_total=score,
            limiar_aplicado=limiar,
            resultado=resultado,
            observacoes=request.form.get('observacoes')
        )
        db.session.add(avaliacao)
        db.session.commit()

        for sintoma in sintomas:
            if str(sintoma.id) in marcados:
                presente = True
            else:
                presente = False
            item = ItemAvaliacao(
                avaliacao_id=avaliacao.id,
                sintoma_id=sintoma.id,
                presente=presente
            )
            db.session.add(item)
        db.session.commit()

        flash('Avaliação registrada com sucesso.', 'sucesso')
        return redirect(url_for('relatorios.detalhe', avaliacao_id=avaliacao.id))

    return render_template('avaliacoes/nova.html', paciente=paciente, sintomas=sintomas)


@avaliacoes_bp.route('/excluir/<int:avaliacao_id>', methods=['POST'])
@login_required
def excluir(avaliacao_id):
    if current_user.tipo == 'paciente':
        abort(403)
    avaliacao = Avaliacao.query.get_or_404(avaliacao_id)
    if current_user.tipo == 'profissional' and avaliacao.usuario_id != current_user.id:
        abort(403)
    db.session.delete(avaliacao)
    db.session.commit()
    flash('Avaliação excluída com sucesso.', 'sucesso')
    return redirect(url_for('avaliacoes.listar'))
