## Projeto Academic (Flask) — Guia do Desenvolvedor

Este repositório contém uma aplicação web em Flask com camadas organizadas por `routes`, `services`, `models` e `domain`, além de templates Jinja2 e arquivos estáticos. O objetivo é oferecer uma base sólida para gestão acadêmica, com autenticação, 2FA, controle de acesso, registro de auditoria, paginação e recursos de visualização de dados.

---

## Resumo rápido (para iniciantes)

Se você só quer rodar a aplicação sem se preocupar com detalhes técnicos, siga um dos caminhos abaixo.

Opção A — Sem Docker (Windows):

```bash
python -m venv env
"env\\Scripts\\activate"
pip install -r requirements.txt
set FLASK_APP=app.py
set FLASK_ENV=development
python app.py
```

Opção B — Com Docker:

```bash
docker build -t educ .
docker compose build
docker compose up
```

A aplicação usa um banco local SQLite em `instance/test.db`. Se precisar “resetar”, apague esse arquivo (somente em ambiente local).

### Principais recursos

- Autenticação e autorização (com 2FA opcional)
- Proteções de segurança: CSRF, rate limiting e validações de senha
- Camada de serviços com regras de negócio desacopladas das rotas
- Templates modulares e assets em `static/`
- Docker e Docker Compose para execução padronizada

### Linguagens e tecnologias utilizadas

- Python 3.12+ (framework Flask)
- HTML, CSS e JavaScript (front-end com templates Jinja2)
- SQLite (banco local padrão em `instance/test.db`)
- Docker e Docker Compose (execução conteinerizada opcional)

---

## Estrutura do projeto (resumo)

```
academic_project/
  app.py                 # Ponto de entrada Flask
  Dockerfile             # Build da imagem
  docker-compose.yaml    # Orquestração local
  requirements.txt       # Dependências Python
  routes/                # Blueprints e rotas HTTP
  services/              # Regras de negócio e integrações
  models/                # Modelos e camadas de persistência
  domain/                # Constantes e modelos de domínio
  templates/             # Páginas Jinja2
  static/                # CSS, JS e imagens
  instance/test.db       # Banco local (SQLite)
```

Consulte também:

- `SETUP_SECURITY.md`, `MUDANCAS_SEGURANÇA.txt`, `Proteção CSRF.txt` — Diretrizes de segurança
- `RELATORIO_2FA.md` — Detalhes do segundo fator
- `RATE_LIMITING_EXPLANATION.md` — Limitação de taxa
- `ESTRUTURA_SERVICES.md` e `ESTRUTURA_SERVICES_EXPLICADA.txt` — Organização da camada de serviços

---

## Pré‑requisitos

- Windows 10/11 (ou Linux/macOS)
- Python 3.12+
- Docker e Docker Compose (opcional, para execução conteinerizada)

---

## Configuração do ambiente (sem Docker)

1. Crie e ative um ambiente virtual Python:

```bash
python -m venv env
"env\\Scripts\\activate"
```

2. Instale as dependências:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Variáveis de ambiente:

- Use `env_example.txt` como referência para configurar as variáveis necessárias
- Em Windows (cmd/powershell), defina temporariamente antes de rodar a aplicação, por exemplo:

```bash
set FLASK_APP=app.py
set FLASK_ENV=development
```

4. Executar a aplicação:

```bash
python app.py
```

A aplicação utilizará o SQLite padrão em `instance/test.db`. Caso precise reinicializar, exclua o arquivo `test.db` (ele será recriado conforme a inicialização da app, se previsto pelo código).

---

## Execução com Docker

1. Construir a imagem (nome sugerido: `educ`):

```bash
docker build -t educ .
```

2. Construir os serviços do Compose:

```bash
docker compose build
```

3. Subir os serviços:

```bash
docker compose up
```

4. Parar e remover (quando necessário):

```bash
docker compose down
```

Notas:

- As variáveis de ambiente podem ser definidas no `docker-compose.yaml` ou via arquivo `.env` (se configurado).
- Volumes/`instance/` garantem persistência local do banco SQLite.

---

## Convenções e dicas

- Estruture novas regras de negócio na camada `services/` evitando lógica nas rotas.
- Registre ações sensíveis via `services/audit_log_service.py` quando aplicável.
- Mantenha validações centralizadas (ex.: `validation_service.py`, `password_validation_service.py`).
- Para novos endpoints, crie blueprints em `routes/` e use `templates/` para renderizações.

---

## Solução de problemas

- Porta já em uso: ajuste a porta no `docker-compose.yaml` ou nas configs do Flask.
- Dependências falhando na instalação: verifique `pip`, `setuptools`, `wheel` e use `--use-pep517` se necessário.
- Banco corrompido em desenvolvimento: apague `instance/test.db` (somente em ambiente local) e reinicie.

---

## Licença

Este projeto é acadêmico. Verifique as diretrizes institucionais aplicáveis antes de uso em produção.

---

## Contatos e documentação complementar

- Documentos na raiz do projeto detalham segurança, arquitetura e execução em VM.
- Consulte `INSTRUCOES_EXECUCAO_VM.md`, `ESTRUTURA_ORGANIZACIONAL.md` e `EVOLUCAO_ARQUITETURA.txt` para contexto adicional.

---

## Créditos

Projeto desenvolvido por: Jonas Silva, Guilherme Diniz e Bruno Belarmino.
