# Testes do DashTalent

Este diretório contém todos os testes automatizados para o sistema DashTalent.

## Estrutura dos Testes

```
tests/
├── __init__.py
├── conftest.py              # Configuração global e fixtures
├── test_services/          # Testes dos serviços de negócio
│   ├── __init__.py
│   ├── test_validation_service.py
│   ├── test_auth_service.py
│   └── test_user_service.py
├── test_routes/            # Testes das rotas
│   ├── __init__.py
│   └── test_auth_routes.py
├── test_models/            # Testes dos modelos
│   ├── __init__.py
│   ├── test_chefe_model.py
│   └── test_instituicao_model.py
└── README.md
```

## Como Executar os Testes

### 1. Instalar Dependências de Teste

```bash
pip install -r requirements.txt
```

### 2. Executar Todos os Testes

```bash
# Usando pytest diretamente
pytest

# Usando o script personalizado
python run_tests.py
```

### 3. Executar Testes com Cobertura

```bash
# Usando pytest com coverage
pytest --cov=. --cov-report=html:htmlcov

# Usando o script personalizado
python run_tests.py --coverage
```

### 4. Executar Teste Específico

```bash
# Teste específico
pytest tests/test_services/test_validation_service.py

# Usando o script personalizado
python run_tests.py tests/test_services/test_validation_service.py
```

### 5. Executar Testes Verbosos

```bash
pytest -v
```

## Configuração dos Testes

### Fixtures Disponíveis

- `app`: Instância da aplicação Flask para testes
- `client`: Cliente de teste para fazer requisições HTTP
- `db_session`: Sessão de banco de dados para cada teste
- `sample_chefe_data`: Dados de exemplo para chefe
- `sample_instituicao_data`: Dados de exemplo para instituição
- `sample_aluno_data`: Dados de exemplo para aluno
- `sample_curso_data`: Dados de exemplo para curso

### Configuração do Banco de Dados

Os testes usam um banco SQLite em memória para garantir isolamento e velocidade.

### Configuração de Ambiente

- `TESTING=True`: Modo de teste ativado
- `WTF_CSRF_ENABLED=False`: CSRF desabilitado para testes
- `SQLALCHEMY_DATABASE_URI=sqlite:///:memory:`: Banco em memória

## Tipos de Testes

### 1. Testes de Serviços (test_services/)

Testam a lógica de negócio dos serviços:

- Validação de dados
- Autenticação e autorização
- Processamento de usuários
- Rate limiting
- Envio de emails

### 2. Testes de Rotas (test_routes/)

Testam as rotas HTTP:

- Respostas corretas
- Redirecionamentos
- Autenticação de rotas
- Validação de formulários

### 3. Testes de Modelos (test_models/)

Testam os modelos de dados:

- Criação de objetos
- Validações de campos
- Relacionamentos
- Métodos especiais

## Cobertura de Código

O projeto está configurado para exigir pelo menos 80% de cobertura de código.

### Relatório de Cobertura

Após executar os testes com cobertura, um relatório HTML será gerado em `htmlcov/index.html`.

### Verificar Cobertura

```bash
# Ver cobertura no terminal
pytest --cov=. --cov-report=term-missing

# Gerar relatório HTML
pytest --cov=. --cov-report=html:htmlcov
```

## Boas Práticas

### 1. Nomenclatura

- Arquivos de teste: `test_*.py`
- Classes de teste: `Test*`
- Métodos de teste: `test_*`

### 2. Estrutura dos Testes

```python
def test_nome_do_teste(self):
    """Descrição do que o teste verifica."""
    # Arrange (preparar)
    # Act (executar)
    # Assert (verificar)
```

### 3. Isolamento

Cada teste é independente e não depende de outros testes.

### 4. Dados de Teste

Use fixtures para dados de teste consistentes e reutilizáveis.

### 5. Mocks

Use mocks para isolar dependências externas (emails, APIs, etc.).

## Exemplos de Testes

### Teste de Validação

```python
def test_validar_email_formato_valido(self):
    """Testa validação de email com formato válido."""
    emails_validos = ['usuario@email.com', 'teste@dominio.org']

    for email in emails_validos:
        assert not validar_email_formato(email)
```

### Teste de Rota

```python
def test_rota_login_get(self, client):
    """Testa acesso à página de login via GET."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
```

### Teste de Modelo

```python
def test_criar_chefe_valido(self, app, db_session, sample_chefe_data):
    """Testa criação de chefe com dados válidos."""
    with app.app_context():
        chefe = Chefe(**sample_chefe_data)
        db_session.add(chefe)
        db_session.commit()

        chefe_criado = Chefe.query.filter_by(email=sample_chefe_data['email']).first()
        assert chefe_criado is not None
```

## Troubleshooting

### Problemas Comuns

1. **Erro de importação**: Verifique se o PYTHONPATH está configurado
2. **Erro de banco**: Verifique se o SQLAlchemy está configurado corretamente
3. **Erro de CSRF**: Verifique se o CSRF está desabilitado nos testes

### Debug

```bash
# Executar com debug
pytest -v -s

# Executar teste específico com debug
pytest tests/test_services/test_validation_service.py -v -s
```

## Contribuindo

Ao adicionar novos testes:

1. Siga a estrutura existente
2. Use fixtures quando apropriado
3. Teste casos de sucesso e falha
4. Mantenha os testes independentes
5. Documente o que cada teste verifica

