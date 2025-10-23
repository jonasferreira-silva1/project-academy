"""
Testes para o modelo Chefe.
"""

import pytest
from models.chefes import Chefe


class TestChefeModel:
    """Testes para o modelo Chefe."""

    def test_criar_chefe_valido(self, app, db_session, sample_chefe_data):
        """Testa criação de chefe com dados válidos."""
        with app.app_context():
            chefe = Chefe(
                nome=sample_chefe_data['nome'],
                email=sample_chefe_data['email'],
                senha=sample_chefe_data['senha'],
                cargo=sample_chefe_data['cargo'],
                empresa=sample_chefe_data['empresa']
            )

            db_session.add(chefe)
            db_session.commit()

            # Verificar se foi criado
            chefe_criado = Chefe.query.filter_by(
                email=sample_chefe_data['email']).first()
            assert chefe_criado is not None
            assert chefe_criado.nome == sample_chefe_data['nome']
            assert chefe_criado.email == sample_chefe_data['email']
            assert chefe_criado.cargo == sample_chefe_data['cargo']
            assert chefe_criado.empresa == sample_chefe_data['empresa']

    def test_chefe_repr(self, app, db_session, sample_chefe_data):
        """Testa representação string do chefe."""
        with app.app_context():
            chefe = Chefe(
                nome=sample_chefe_data['nome'],
                email=sample_chefe_data['email'],
                senha=sample_chefe_data['senha'],
                cargo=sample_chefe_data['cargo'],
                empresa=sample_chefe_data['empresa']
            )

            db_session.add(chefe)
            db_session.commit()

            # Verificar representação
            repr_str = repr(chefe)
            assert sample_chefe_data['nome'] in repr_str
            assert 'Chefe' in repr_str

    def test_chefe_get_id(self, app, db_session, sample_chefe_data):
        """Testa método get_id do chefe."""
        with app.app_context():
            chefe = Chefe(
                nome=sample_chefe_data['nome'],
                email=sample_chefe_data['email'],
                senha=sample_chefe_data['senha'],
                cargo=sample_chefe_data['cargo'],
                empresa=sample_chefe_data['empresa']
            )

            db_session.add(chefe)
            db_session.commit()

            # Verificar get_id
            assert chefe.get_id() == chefe.id

    def test_chefe_is_authenticated(self, app, db_session, sample_chefe_data):
        """Testa método is_authenticated do chefe."""
        with app.app_context():
            chefe = Chefe(
                nome=sample_chefe_data['nome'],
                email=sample_chefe_data['email'],
                senha=sample_chefe_data['senha'],
                cargo=sample_chefe_data['cargo'],
                empresa=sample_chefe_data['empresa']
            )

            db_session.add(chefe)
            db_session.commit()

            # Verificar is_authenticated
            assert chefe.is_authenticated is True

    def test_chefe_is_active(self, app, db_session, sample_chefe_data):
        """Testa método is_active do chefe."""
        with app.app_context():
            chefe = Chefe(
                nome=sample_chefe_data['nome'],
                email=sample_chefe_data['email'],
                senha=sample_chefe_data['senha'],
                cargo=sample_chefe_data['cargo'],
                empresa=sample_chefe_data['empresa']
            )

            db_session.add(chefe)
            db_session.commit()

            # Verificar is_active
            assert chefe.is_active is True

    def test_chefe_is_anonymous(self, app, db_session, sample_chefe_data):
        """Testa método is_anonymous do chefe."""
        with app.app_context():
            chefe = Chefe(
                nome=sample_chefe_data['nome'],
                email=sample_chefe_data['email'],
                senha=sample_chefe_data['senha'],
                cargo=sample_chefe_data['cargo'],
                empresa=sample_chefe_data['empresa']
            )

            db_session.add(chefe)
            db_session.commit()

            # Verificar is_anonymous
            assert chefe.is_anonymous is False

    def test_chefe_email_unico(self, app, db_session, sample_chefe_data):
        """Testa que email deve ser único."""
        with app.app_context():
            # Criar primeiro chefe
            chefe1 = Chefe(
                nome=sample_chefe_data['nome'],
                email=sample_chefe_data['email'],
                senha=sample_chefe_data['senha'],
                cargo=sample_chefe_data['cargo'],
                empresa=sample_chefe_data['empresa']
            )

            db_session.add(chefe1)
            db_session.commit()

            # Tentar criar segundo chefe com mesmo email
            chefe2 = Chefe(
                nome='Outro Nome',
                email=sample_chefe_data['email'],  # Mesmo email
                senha='outra_senha',
                cargo='Outro Cargo',
                empresa='Outra Empresa'
            )

            db_session.add(chefe2)

            # Deve gerar erro de integridade
            with pytest.raises(Exception):  # SQLAlchemy IntegrityError
                db_session.commit()

    def test_chefe_campos_obrigatorios(self, app, db_session):
        """Testa que campos obrigatórios não podem ser nulos."""
        with app.app_context():
            # Tentar criar chefe sem campos obrigatórios
            chefe = Chefe()

            db_session.add(chefe)

            # Deve gerar erro de validação
            with pytest.raises(Exception):
                db_session.commit()

    def test_chefe_atualizar_dados(self, app, db_session, sample_chefe_data):
        """Testa atualização de dados do chefe."""
        with app.app_context():
            chefe = Chefe(
                nome=sample_chefe_data['nome'],
                email=sample_chefe_data['email'],
                senha=sample_chefe_data['senha'],
                cargo=sample_chefe_data['cargo'],
                empresa=sample_chefe_data['empresa']
            )

            db_session.add(chefe)
            db_session.commit()

            # Atualizar dados
            chefe.nome = 'Nome Atualizado'
            chefe.cargo = 'Cargo Atualizado'
            chefe.empresa = 'Empresa Atualizada'

            db_session.commit()

            # Verificar atualização
            chefe_atualizado = Chefe.query.get(chefe.id)
            assert chefe_atualizado.nome == 'Nome Atualizado'
            assert chefe_atualizado.cargo == 'Cargo Atualizado'
            assert chefe_atualizado.empresa == 'Empresa Atualizada'
