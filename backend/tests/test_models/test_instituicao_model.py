"""
Testes para o modelo InstituicaodeEnsino.
"""

import pytest
from models.instituicao import InstituicaodeEnsino


class TestInstituicaodeEnsinoModel:
    """Testes para o modelo InstituicaodeEnsino."""

    def test_criar_instituicao_valida(self, app, db_session, sample_instituicao_data):
        """Testa criação de instituição com dados válidos."""
        with app.app_context():
            instituicao = InstituicaodeEnsino(
                nome_instituicao=sample_instituicao_data['nome_instituicao'],
                email=sample_instituicao_data['email'],
                senha=sample_instituicao_data['senha'],
                contato=sample_instituicao_data['contato'],
                endereco=sample_instituicao_data['endereco'],
                nota_mec=sample_instituicao_data['nota_mec'],
                modalidade=sample_instituicao_data['modalidade']
            )

            db_session.add(instituicao)
            db_session.commit()

            # Verificar se foi criada
            instituicao_criada = InstituicaodeEnsino.query.filter_by(
                email=sample_instituicao_data['email']
            ).first()
            assert instituicao_criada is not None
            assert instituicao_criada.nome_instituicao == sample_instituicao_data[
                'nome_instituicao']
            assert instituicao_criada.email == sample_instituicao_data['email']
            assert instituicao_criada.contato == sample_instituicao_data['contato']
            assert instituicao_criada.endereco == sample_instituicao_data['endereco']
            assert instituicao_criada.nota_mec == sample_instituicao_data['nota_mec']
            assert instituicao_criada.modalidade == sample_instituicao_data['modalidade']

    def test_instituicao_repr(self, app, db_session, sample_instituicao_data):
        """Testa representação string da instituição."""
        with app.app_context():
            instituicao = InstituicaodeEnsino(
                nome_instituicao=sample_instituicao_data['nome_instituicao'],
                email=sample_instituicao_data['email'],
                senha=sample_instituicao_data['senha'],
                contato=sample_instituicao_data['contato'],
                endereco=sample_instituicao_data['endereco'],
                nota_mec=sample_instituicao_data['nota_mec'],
                modalidade=sample_instituicao_data['modalidade']
            )

            db_session.add(instituicao)
            db_session.commit()

            # Verificar representação
            repr_str = repr(instituicao)
            assert sample_instituicao_data['nome_instituicao'] in repr_str
            assert 'InstituicaodeEnsino' in repr_str

    def test_instituicao_get_id(self, app, db_session, sample_instituicao_data):
        """Testa método get_id da instituição."""
        with app.app_context():
            instituicao = InstituicaodeEnsino(
                nome_instituicao=sample_instituicao_data['nome_instituicao'],
                email=sample_instituicao_data['email'],
                senha=sample_instituicao_data['senha'],
                contato=sample_instituicao_data['contato'],
                endereco=sample_instituicao_data['endereco'],
                nota_mec=sample_instituicao_data['nota_mec'],
                modalidade=sample_instituicao_data['modalidade']
            )

            db_session.add(instituicao)
            db_session.commit()

            # Verificar get_id
            assert instituicao.get_id() == instituicao.id

    def test_instituicao_is_authenticated(self, app, db_session, sample_instituicao_data):
        """Testa método is_authenticated da instituição."""
        with app.app_context():
            instituicao = InstituicaodeEnsino(
                nome_instituicao=sample_instituicao_data['nome_instituicao'],
                email=sample_instituicao_data['email'],
                senha=sample_instituicao_data['senha'],
                contato=sample_instituicao_data['contato'],
                endereco=sample_instituicao_data['endereco'],
                nota_mec=sample_instituicao_data['nota_mec'],
                modalidade=sample_instituicao_data['modalidade']
            )

            db_session.add(instituicao)
            db_session.commit()

            # Verificar is_authenticated
            assert instituicao.is_authenticated is True

    def test_instituicao_is_active(self, app, db_session, sample_instituicao_data):
        """Testa método is_active da instituição."""
        with app.app_context():
            instituicao = InstituicaodeEnsino(
                nome_instituicao=sample_instituicao_data['nome_instituicao'],
                email=sample_instituicao_data['email'],
                senha=sample_instituicao_data['senha'],
                contato=sample_instituicao_data['contato'],
                endereco=sample_instituicao_data['endereco'],
                nota_mec=sample_instituicao_data['nota_mec'],
                modalidade=sample_instituicao_data['modalidade']
            )

            db_session.add(instituicao)
            db_session.commit()

            # Verificar is_active
            assert instituicao.is_active is True

    def test_instituicao_is_anonymous(self, app, db_session, sample_instituicao_data):
        """Testa método is_anonymous da instituição."""
        with app.app_context():
            instituicao = InstituicaodeEnsino(
                nome_instituicao=sample_instituicao_data['nome_instituicao'],
                email=sample_instituicao_data['email'],
                senha=sample_instituicao_data['senha'],
                contato=sample_instituicao_data['contato'],
                endereco=sample_instituicao_data['endereco'],
                nota_mec=sample_instituicao_data['nota_mec'],
                modalidade=sample_instituicao_data['modalidade']
            )

            db_session.add(instituicao)
            db_session.commit()

            # Verificar is_anonymous
            assert instituicao.is_anonymous is False

    def test_instituicao_email_unico(self, app, db_session, sample_instituicao_data):
        """Testa que email deve ser único."""
        with app.app_context():
            # Criar primeira instituição
            instituicao1 = InstituicaodeEnsino(
                nome_instituicao=sample_instituicao_data['nome_instituicao'],
                email=sample_instituicao_data['email'],
                senha=sample_instituicao_data['senha'],
                contato=sample_instituicao_data['contato'],
                endereco=sample_instituicao_data['endereco'],
                nota_mec=sample_instituicao_data['nota_mec'],
                modalidade=sample_instituicao_data['modalidade']
            )

            db_session.add(instituicao1)
            db_session.commit()

            # Tentar criar segunda instituição com mesmo email
            instituicao2 = InstituicaodeEnsino(
                nome_instituicao='Outra Instituição',
                email=sample_instituicao_data['email'],  # Mesmo email
                senha='outra_senha',
                contato='11988888888',
                endereco='Outro Endereço',
                nota_mec=3.5,
                modalidade='EAD'
            )

            db_session.add(instituicao2)

            # Deve gerar erro de integridade
            with pytest.raises(Exception):  # SQLAlchemy IntegrityError
                db_session.commit()

    def test_instituicao_campos_obrigatorios(self, app, db_session):
        """Testa que campos obrigatórios não podem ser nulos."""
        with app.app_context():
            # Tentar criar instituição sem campos obrigatórios
            instituicao = InstituicaodeEnsino()

            db_session.add(instituicao)

            # Deve gerar erro de validação
            with pytest.raises(Exception):
                db_session.commit()

    def test_instituicao_atualizar_dados(self, app, db_session, sample_instituicao_data):
        """Testa atualização de dados da instituição."""
        with app.app_context():
            instituicao = InstituicaodeEnsino(
                nome_instituicao=sample_instituicao_data['nome_instituicao'],
                email=sample_instituicao_data['email'],
                senha=sample_instituicao_data['senha'],
                contato=sample_instituicao_data['contato'],
                endereco=sample_instituicao_data['endereco'],
                nota_mec=sample_instituicao_data['nota_mec'],
                modalidade=sample_instituicao_data['modalidade']
            )

            db_session.add(instituicao)
            db_session.commit()

            # Atualizar dados
            instituicao.nome_instituicao = 'Instituição Atualizada'
            instituicao.contato = '11988888888'
            instituicao.endereco = 'Endereço Atualizado'
            instituicao.nota_mec = 4.8
            instituicao.modalidade = 'Híbrido'

            db_session.commit()

            # Verificar atualização
            instituicao_atualizada = InstituicaodeEnsino.query.get(
                instituicao.id)
            assert instituicao_atualizada.nome_instituicao == 'Instituição Atualizada'
            assert instituicao_atualizada.contato == '11988888888'
            assert instituicao_atualizada.endereco == 'Endereço Atualizado'
            assert instituicao_atualizada.nota_mec == 4.8
            assert instituicao_atualizada.modalidade == 'Híbrido'

    def test_instituicao_nota_mec_range(self, app, db_session):
        """Testa validação do range da nota MEC."""
        with app.app_context():
            # Testar nota válida
            instituicao = InstituicaodeEnsino(
                nome_instituicao='Universidade Teste',
                email='teste@universidade.com',
                senha='senha123456',
                contato='11999999999',
                endereco='Rua Teste, 123',
                nota_mec=4.5,  # Nota válida
                modalidade='Presencial'
            )

            db_session.add(instituicao)
            db_session.commit()

            # Verificar se foi criada
            instituicao_criada = InstituicaodeEnsino.query.filter_by(
                email='teste@universidade.com'
            ).first()
            assert instituicao_criada is not None
            assert instituicao_criada.nota_mec == 4.5

