"""
Testes para o serviço de usuários.
"""

from services.user_service import (
    criar_instituicao_ensino,
    criar_chefe,
    atualizar_perfil_chefe,
    atualizar_perfil_instituicao,
    verificar_email_duplicado_instituicao,
    verificar_email_duplicado_chefe
)


class TestUserService:
    """Testes para o serviço de usuários."""

    def test_criar_instituicao_ensino_sucesso(self, test_app, db_session, sample_instituicao_data):
        """Testa criação bem-sucedida de instituição de ensino."""
        with test_app.app_context():
            resultado = criar_instituicao_ensino(sample_instituicao_data)

            assert resultado['sucesso'] is True
            assert 'Instituição cadastrada com sucesso' in resultado['mensagem']

            # Verificar se a instituição foi criada no banco
            instituicao = InstituicaodeEnsino.query.filter_by(
                email=sample_instituicao_data['email']
            ).first()
            assert instituicao is not None
            assert instituicao.nome_instituicao == sample_instituicao_data['nome_instituicao']

    def test_criar_instituicao_ensino_email_duplicado(self, test_app, db_session, sample_instituicao_data):
        """Testa criação de instituição com email duplicado."""
        with test_app.app_context():
            # Criar primeira instituição
            criar_instituicao_ensino(sample_instituicao_data)

            # Tentar criar segunda com mesmo email
            dados_duplicados = sample_instituicao_data.copy()
            dados_duplicados['nome_instituicao'] = 'Outra Instituição'

            resultado = criar_instituicao_ensino(dados_duplicados)

            assert resultado['sucesso'] is False
            assert 'Email já cadastrado' in resultado['mensagem']

    def test_criar_chefe_sucesso(self, test_app, db_session, sample_chefe_data):
        """Testa criação bem-sucedida de chefe."""
        with test_app.app_context():
            resultado = criar_chefe(sample_chefe_data)

            assert resultado['sucesso'] is True
            assert 'Chefe cadastrado com sucesso' in resultado['mensagem']

            # Verificar se o chefe foi criado no banco
            chefe = Chefe.query.filter_by(
                email=sample_chefe_data['email']).first()
            assert chefe is not None
            assert chefe.nome == sample_chefe_data['nome']

    def test_criar_chefe_email_duplicado(self, test_app, db_session, sample_chefe_data):
        """Testa criação de chefe com email duplicado."""
        with test_app.app_context():
            # Criar primeiro chefe
            criar_chefe(sample_chefe_data)

            # Tentar criar segundo com mesmo email
            dados_duplicados = sample_chefe_data.copy()
            dados_duplicados['nome'] = 'Outro Chefe'

            resultado = criar_chefe(dados_duplicados)

            assert resultado['sucesso'] is False
            assert 'Email já cadastrado' in resultado['mensagem']

    def test_verificar_email_duplicado_instituicao_existente(self, test_app, db_session, sample_instituicao_data):
        """Testa verificação de email duplicado para instituição existente."""
        with test_app.app_context():
            # Criar instituição
            criar_instituicao_ensino(sample_instituicao_data)

            # Verificar email duplicado
            resultado = verificar_email_duplicado_instituicao(
                sample_instituicao_data['email'])
            assert resultado is True

    def test_verificar_email_duplicado_instituicao_inexistente(self, test_app):
        """Testa verificação de email duplicado para instituição inexistente."""
        with test_app.app_context():
            resultado = verificar_email_duplicado_instituicao(
                'email@inexistente.com')
            assert resultado is False

    def test_verificar_email_duplicado_chefe_existente(self, test_app, db_session, sample_chefe_data):
        """Testa verificação de email duplicado para chefe existente."""
        with test_app.app_context():
            # Criar chefe
            criar_chefe(sample_chefe_data)

            # Verificar email duplicado
            resultado = verificar_email_duplicado_chefe(
                sample_chefe_data['email'])
            assert resultado is True

    def test_verificar_email_duplicado_chefe_inexistente(self, test_app):
        """Testa verificação de email duplicado para chefe inexistente."""
        with test_app.app_context():
            resultado = verificar_email_duplicado_chefe(
                'email@inexistente.com')
            assert resultado is False

    def test_atualizar_perfil_chefe_sucesso(self, test_app, db_session, sample_chefe_data):
        """Testa atualização bem-sucedida de perfil de chefe."""
        with test_app.app_context():
            # Criar chefe
            criar_chefe(sample_chefe_data)
            chefe = Chefe.query.filter_by(
                email=sample_chefe_data['email']).first()

            # Dados de atualização
            dados_atualizacao = {
                'nome': 'João Silva Atualizado',
                'cargo': 'Diretor',
                'empresa': 'Empresa Atualizada'
            }

            resultado = atualizar_perfil_chefe(chefe.id, dados_atualizacao)

            assert resultado['sucesso'] is True
            assert 'Perfil atualizado com sucesso' in resultado['mensagem']

            # Verificar se os dados foram atualizados
            chefe_atualizado = Chefe.query.get(chefe.id)
            assert chefe_atualizado.nome == dados_atualizacao['nome']
            assert chefe_atualizado.cargo == dados_atualizacao['cargo']
            assert chefe_atualizado.empresa == dados_atualizacao['empresa']

    def test_atualizar_perfil_instituicao_sucesso(self, app, db_session, sample_instituicao_data):
        """Testa atualização bem-sucedida de perfil de instituição."""
        with test_app.app_context():
            # Criar instituição
            criar_instituicao_ensino(sample_instituicao_data)
            instituicao = InstituicaodeEnsino.query.filter_by(
                email=sample_instituicao_data['email']
            ).first()

            # Dados de atualização
            dados_atualizacao = {
                'nome_instituicao': 'Universidade Atualizada',
                'contato': '11988888888',
                'endereco': 'Novo Endereço, 456',
                'nota_mec': 4.8,
                'modalidade': 'Híbrido'
            }

            resultado = atualizar_perfil_instituicao(
                instituicao.id, dados_atualizacao)

            assert resultado['sucesso'] is True
            assert 'Perfil atualizado com sucesso' in resultado['mensagem']

            # Verificar se os dados foram atualizados
            instituicao_atualizada = InstituicaodeEnsino.query.get(
                instituicao.id)
            assert instituicao_atualizada.nome_instituicao == dados_atualizacao[
                'nome_instituicao']
            assert instituicao_atualizada.contato == dados_atualizacao['contato']
            assert instituicao_atualizada.endereco == dados_atualizacao['endereco']
            assert instituicao_atualizada.nota_mec == dados_atualizacao['nota_mec']
            assert instituicao_atualizada.modalidade == dados_atualizacao['modalidade']

    def test_atualizar_perfil_chefe_inexistente(self, app):
        """Testa atualização de perfil de chefe inexistente."""
        with test_app.app_context():
            dados_atualizacao = {
                'nome': 'Nome Atualizado',
                'cargo': 'Novo Cargo',
                'empresa': 'Nova Empresa'
            }

            resultado = atualizar_perfil_chefe(
                99999, dados_atualizacao)  # ID inexistente

            assert resultado['sucesso'] is False
            assert 'Chefe não encontrado' in resultado['mensagem']

    def test_atualizar_perfil_instituicao_inexistente(self, app):
        """Testa atualização de perfil de instituição inexistente."""
        with test_app.app_context():
            dados_atualizacao = {
                'nome_instituicao': 'Nome Atualizado',
                'contato': '11999999999'
            }

            resultado = atualizar_perfil_instituicao(
                99999, dados_atualizacao)  # ID inexistente

            assert resultado['sucesso'] is False
            assert 'Instituição não encontrada' in resultado['mensagem']
