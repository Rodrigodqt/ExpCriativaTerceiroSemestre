import csv
import io
from flask import Blueprint, render_template, abort, Response
from flask_login import login_required, current_user

from modelos import Avaliacao, Paciente, ItemAvaliacao, Sintoma

relatorios_bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')


def pode_ver_avaliacao(avaliacao):
    if current_user.tipo == 'admin':
        return True
    if current_user.tipo == 'profissional':
        return avaliacao.usuario_id == current_user.id
    paciente = Paciente.query.get(avaliacao.paciente_id)
    if paciente and paciente.cpf == current_user.cpf:
        return True
    return False


@relatorios_bp.route('/')
@login_required
def listar():
    if current_user.tipo == 'admin':
        avaliacoes = Avaliacao.query.order_by(Avaliacao.id.desc()).all()
    elif current_user.tipo == 'profissional':
        avaliacoes = Avaliacao.query.filter_by(usuario_id=current_user.id).order_by(Avaliacao.id.desc()).all()
    else:
        meus_pacientes = Paciente.query.filter_by(cpf=current_user.cpf).all()
        ids = []
        for p in meus_pacientes:
            ids.append(p.id)
        if ids:
            avaliacoes = Avaliacao.query.filter(Avaliacao.paciente_id.in_(ids)).order_by(Avaliacao.id.desc()).all()
        else:
            avaliacoes = []
    return render_template('relatorios/listar.html', avaliacoes=avaliacoes)


@relatorios_bp.route('/<int:avaliacao_id>')
@login_required
def detalhe(avaliacao_id):
    avaliacao = Avaliacao.query.get_or_404(avaliacao_id)
    if not pode_ver_avaliacao(avaliacao):
        abort(403)
    itens = ItemAvaliacao.query.filter_by(avaliacao_id=avaliacao.id).all()
    return render_template('relatorios/detalhe.html', avaliacao=avaliacao, itens=itens)


@relatorios_bp.route('/<int:avaliacao_id>/csv')
@login_required
def exportar_csv(avaliacao_id):
    avaliacao = Avaliacao.query.get_or_404(avaliacao_id)
    if not pode_ver_avaliacao(avaliacao):
        abort(403)
    itens = ItemAvaliacao.query.filter_by(avaliacao_id=avaliacao.id).all()
    paciente = Paciente.query.get(avaliacao.paciente_id)

    saida = io.StringIO()
    escritor = csv.writer(saida, delimiter=';')
    escritor.writerow(['Relatorio de Avaliacao - Sindrome do X Fragil'])
    escritor.writerow(['Paciente', paciente.nome])
    escritor.writerow(['Data da Avaliacao', avaliacao.data_avaliacao.strftime('%d/%m/%Y %H:%M')])
    escritor.writerow(['Score Total', avaliacao.score_total])
    escritor.writerow(['Limiar Aplicado', avaliacao.limiar_aplicado])
    escritor.writerow(['Resultado', avaliacao.resultado])
    escritor.writerow([])
    escritor.writerow(['Sintoma', 'Presente'])
    for item in itens:
        sintoma = Sintoma.query.get(item.sintoma_id)
        if item.presente:
            presente_texto = 'Sim'
        else:
            presente_texto = 'Nao'
        escritor.writerow([sintoma.nome, presente_texto])

    conteudo = saida.getvalue()
    saida.close()
    nome_arquivo = 'relatorio_avaliacao_' + str(avaliacao.id) + '.csv'
    return Response(
        conteudo,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=' + nome_arquivo}
    )
