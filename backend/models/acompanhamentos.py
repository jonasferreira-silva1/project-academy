from .base import db
from datetime import datetime

class Acompanhamento(db.Model):
    """Modelo para rastrear acompanhamentos entre chefes e alunos."""
    __tablename__ = 'acompanhamento'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_chefe = db.Column(db.Integer, db.ForeignKey('chefe.id_chefe'), nullable=False)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)
    data_acompanhamento = db.Column(db.DateTime, server_default=db.func.now())

    # Relacionamentos
    chefe = db.relationship('Chefe', backref='acompanhamentos')
    aluno = db.relationship('Aluno', backref='acompanhamentos')

    # Constraints
    __table_args__ = (
        db.UniqueConstraint('id_chefe', 'id_aluno', name='uix_chefe_aluno'),
    )
    
    def __repr__(self):
        return f'<Acompanhamento chefe_id={self.id_chefe} aluno_id={self.id_aluno}>'

class Indicacao(db.Model):
    """Modelo para rastrear indicações de alunos por chefes."""
    __tablename__ = 'indicacoes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_chefe = db.Column(db.Integer, db.ForeignKey('chefe.id_chefe'), nullable=False)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)
    data_indicacao = db.Column(db.DateTime, server_default=db.func.now())

    # Relacionamentos
    chefe = db.relationship('Chefe', backref='indicacoes')
    aluno = db.relationship('Aluno', backref='indicacoes')

    __table_args__ = (
        db.UniqueConstraint('id_chefe', 'id_aluno', name='uix_chefe_aluno_indicacao'),
    )
    
    def __repr__(self):
        return f'<Indicacao chefe_id={self.id_chefe} aluno_id={self.id_aluno}>'
