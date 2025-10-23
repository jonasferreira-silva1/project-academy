"""
Testes para as rotas de autenticação.
"""

from unittest.mock import patch


class TestAuthRoutes:
    """Testes para as rotas de autenticação."""

    def test_rota_login_get(self, client):
        """Testa acesso à página de login via GET."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data

    def test_rota_cadastro_get(self, client):
        """Testa acesso à página de cadastro via GET."""
        response = client.get('/cadastro')
        assert response.status_code == 200
        assert b'Cadastro' in response.data

    def test_rota_home_redireciona_para_login(self, client):
        """Testa se a rota home redireciona para login quando não autenticado."""
        response = client.get('/')
        assert response.status_code == 302  # Redirecionamento
        assert '/login' in response.location

    @patch('routes.auth_routes.processar_login')
    def test_rota_login_post_sucesso(self, mock_processar_login, client, sample_chefe_data):
        """Testa login bem-sucedido via POST."""
        mock_processar_login.return_value = {
            'sucesso': True,
            'usuario': sample_chefe_data,
            'tipo_usuario': 'chefe'
        }

        response = client.post('/login', data={
            'email': sample_chefe_data['email'],
            'senha': sample_chefe_data['senha']
        })

        assert response.status_code == 302  # Redirecionamento após login
        mock_processar_login.assert_called_once()

    @patch('routes.auth_routes.processar_login')
    def test_rota_login_post_falha(self, mock_processar_login, client):
        """Testa login com falha via POST."""
        mock_processar_login.return_value = {
            'sucesso': False,
            'mensagem': 'Credenciais inválidas'
        }

        response = client.post('/login', data={
            'email': 'usuario@teste.com',
            'senha': 'senha_errada'
        })

        assert response.status_code == 200  # Página de login com erro
        assert 'Credenciais inválidas' in response.data.decode('utf-8')

    @patch('routes.auth_routes.processar_cadastro')
    def test_rota_cadastro_post_sucesso(self, mock_processar_cadastro, client):
        """Testa cadastro bem-sucedido via POST."""
        mock_processar_cadastro.return_value = {
            'sucesso': True,
            'mensagem': 'Cadastro realizado com sucesso'
        }

        dados_cadastro = {
            'nome': 'Novo Usuário',
            'email': 'novo@usuario.com',
            'senha': 'senha123456',
            'confirmar_senha': 'senha123456',
            'cargo': 'Gerente',
            'empresa': 'Nova Empresa',
            'tipo_usuario': 'chefe'
        }

        response = client.post('/cadastro', data=dados_cadastro)

        assert response.status_code == 302  # Redirecionamento após cadastro
        mock_processar_cadastro.assert_called_once()

    @patch('routes.auth_routes.processar_cadastro')
    def test_rota_cadastro_post_falha(self, mock_processar_cadastro, client):
        """Testa cadastro com falha via POST."""
        mock_processar_cadastro.return_value = {
            'sucesso': False,
            'mensagem': 'Email já cadastrado'
        }

        dados_cadastro = {
            'nome': 'Usuário Existente',
            'email': 'existente@email.com',
            'senha': 'senha123456',
            'confirmar_senha': 'senha123456',
            'cargo': 'Gerente',
            'empresa': 'Empresa',
            'tipo_usuario': 'chefe'
        }

        response = client.post('/cadastro', data=dados_cadastro)

        assert response.status_code == 200  # Página de cadastro com erro
        assert 'Email já cadastrado' in response.data.decode('utf-8')

    def test_rota_logout(self, client):
        """Testa rota de logout."""
        response = client.post('/logout')
        assert response.status_code == 302  # Redirecionamento após logout

    def test_rota_esqueceu_senha_get(self, client):
        """Testa acesso à página de esqueceu senha via GET."""
        response = client.get('/esqueceu-senha')
        assert response.status_code == 200
        assert b'Esqueceu sua senha' in response.data

    @patch('routes.esqueceu_senha_routes.processar_esqueceu_senha')
    def test_rota_esqueceu_senha_post_sucesso(self, mock_processar, client):
        """Testa solicitação de recuperação de senha bem-sucedida."""
        mock_processar.return_value = {
            'sucesso': True,
            'mensagem': 'Email de recuperação enviado'
        }

        response = client.post('/esqueceu-senha', data={
            'email': 'usuario@teste.com'
        })

        assert response.status_code == 200
        assert 'Email de recuperação enviado' in response.data.decode('utf-8')

    @patch('routes.esqueceu_senha_routes.processar_esqueceu_senha')
    def test_rota_esqueceu_senha_post_falha(self, mock_processar, client):
        """Testa solicitação de recuperação de senha com falha."""
        mock_processar.return_value = {
            'sucesso': False,
            'mensagem': 'Email não encontrado'
        }

        response = client.post('/esqueceu-senha', data={
            'email': 'inexistente@teste.com'
        })

        assert response.status_code == 200
        assert 'Email não encontrado' in response.data.decode('utf-8')
