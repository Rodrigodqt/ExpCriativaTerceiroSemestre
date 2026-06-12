from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(14))
    crm = db.Column(db.String(20))
    especialidade = db.Column(db.String(120))
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now)

    pacientes = db.relationship('Paciente', backref='usuario', lazy=True)
    avaliacoes = db.relationship('Avaliacao', backref='usuario', lazy=True)


class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    data_nascimento = db.Column(db.Date)
    sexo = db.Column(db.String(1))
    cpf = db.Column(db.String(14))
    contato = db.Column(db.String(120))
    historico_familiar = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'))
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now)

    avaliacoes = db.relationship('Avaliacao', backref='paciente', lazy=True)


class Sintoma(db.Model):
    __tablename__ = 'sintomas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(80))
    peso_masculino = db.Column(db.Float)
    peso_feminino = db.Column(db.Float)
    ativo = db.Column(db.Boolean, default=True)
    ordem = db.Column(db.Integer)


class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'))
    data_avaliacao = db.Column(db.DateTime, default=datetime.now)
    score_total = db.Column(db.Float)
    limiar_aplicado = db.Column(db.Float)
    resultado = db.Column(db.String(60))
    observacoes = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.now)

    itens = db.relationship('ItemAvaliacao', backref='avaliacao', lazy=True, cascade='all, delete-orphan')


class ItemAvaliacao(db.Model):
    __tablename__ = 'itens_avaliacao'

    id = db.Column(db.Integer, primary_key=True)
    avaliacao_id = db.Column(db.Integer, db.ForeignKey('avaliacoes.id', ondelete='CASCADE'), nullable=False)
    sintoma_id = db.Column(db.Integer, db.ForeignKey('sintomas.id', ondelete='CASCADE'), nullable=False)
    presente = db.Column(db.Boolean, default=False)

    sintoma = db.relationship('Sintoma')
