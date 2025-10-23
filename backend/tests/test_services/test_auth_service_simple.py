"""
Testes simplificados para o serviço de autenticação.
"""

from unittest.mock import patch, MagicMock
from services.auth_service import load_user


class TestAuthServiceSimple:
    """Testes simplificados para o serviço de autenticação."""

    def test_load_user_chefe_existente(self, test_app, db_session, sample_chefe_data):
        """Testa carregamento de usuário chefe existente."""
        with test_app.app_context():
            from models.chefes import Chefe

            # Criar um chefe de teste
            chefe = Chefe(
                nome=sample_chefe_data['nome'],
                email=sample_chefe_data['email'],
                senha=sample_chefe_data['senha'],
                cargo=sample_chefe_data['cargo'],
                empresa=sample_chefe_data['empresa']
            )
            db_session.add(chefe)
            db_session.commit()

            # Simular sessão para teste
            with test_app.test_request_context():
                from flask import session
                session['tipo_usuario'] = 'chefe'

                # Testar carregamento
                usuario = load_user(chefe.id)
                assert usuario is not None
                assert usuario.email == sample_chefe_data['email']
                assert isinstance(usuario, Chefe)

    def test_load_user_instituicao_existente(self, test_app, db_session, sample_instituicao_data):
        """Testa carregamento de usuário instituição existente."""
        with test_app.app_context():
            from models.instituicao import InstituicaodeEnsino

            # Criar uma instituição de teste
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

            # Simular sessão para teste
            with test_app.test_request_context():
                from flask import session
                session['tipo_usuario'] = 'instituicao'

                # Testar carregamento
                usuario = load_user(instituicao.id)
                assert usuario is not None
                assert usuario.email == sample_instituicao_data['email']
                assert isinstance(usuario, InstituicaodeEnsino)

    def test_load_user_inexistente(self, test_app):
        """Testa carregamento de usuário inexistente."""
        with test_app.app_context():
            with test_app.test_request_context():
                from flask import session
                session['tipo_usuario'] = 'chefe'

                usuario = load_user(99999)  # ID que não existe
                assert usuario is None

    def test_load_user_sem_tipo_usuario(self, test_app):
        """Testa carregamento sem tipo de usuário na sessão."""
        with test_app.app_context():
            with test_app.test_request_context():
                from flask import session
                # Não definir tipo_usuario na sessão

                usuario = load_user(1)
                assert usuario is None

    def test_load_user_tipo_invalido(self, test_app):
        """Testa carregamento com tipo de usuário inválido."""
        with test_app.app_context():
            with test_app.test_request_context():
                from flask import session
                session['tipo_usuario'] = 'tipo_invalido'

                usuario = load_user(1)
                assert usuario is None
