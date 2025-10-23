"""
Configuração global para testes pytest.
Define fixtures e configurações compartilhadas entre todos os testes.
"""

import pytest

# Importar a aplicação e modelos
from app import app as flask_app
from domain import db
from models import Chefe, InstituicaodeEnsino, Aluno, Curso


@pytest.fixture(scope='session')
def test_app():
    """Fixture que cria uma instância da aplicação Flask para testes."""
    # Configurar banco de dados em memória para testes
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    # Desabilitar CSRF para testes
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['SECRET_KEY'] = 'test-secret-key'

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()


@pytest.fixture(scope='function')
def client(test_app):
    """Fixture que cria um cliente de teste para fazer requisições."""
    return test_app.test_client()


@pytest.fixture(scope='function')
def db_session(test_app):
    """Fixture que cria uma sessão de banco de dados para cada teste."""
    with test_app.app_context():
        db.session.begin()
        yield db.session
        db.session.rollback()


@pytest.fixture
def sample_chefe_data():
    """Dados de exemplo para um chefe."""
    return {
        'nome': 'João Silva',
        'email': 'joao@empresa.com',
        'senha': 'senha123456',
        'cargo': 'Gerente de RH',
        'empresa': 'TechCorp'
    }


@pytest.fixture
def sample_instituicao_data():
    """Dados de exemplo para uma instituição."""
    return {
        'nome_instituicao': 'Universidade Tech',
        'email': 'contato@universidadetech.com',
        'senha': 'senha123456',
        'contato': '11999999999',
        'endereco': 'Rua das Flores, 123',
        'nota_mec': 4.5,
        'modalidade': 'Presencial'
    }


@pytest.fixture
def sample_aluno_data():
    """Dados de exemplo para um aluno."""
    return {
        'nome': 'Maria Santos',
        'email': 'maria@email.com',
        'periodo': '3º',
        'curso_id': 1,
        'instituicao_id': 1
    }


@pytest.fixture
def sample_curso_data():
    """Dados de exemplo para um curso."""
    return {
        'nome_curso': 'Ciência da Computação',
        'instituicao_id': 1,
        'duracao': '4 anos',
        'modalidade': 'Presencial'
    }
