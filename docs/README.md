## Projeto Academic (Flask) — Guia do Desenvolvedor

Este repositório contém uma aplicação web em Flask com camadas organizadas por `routes`, `services`, `models` e `domain`, além de templates Jinja2 e arquivos estáticos. O objetivo é oferecer uma base sólida para gestão acadêmica, com autenticação, 2FA, controle de acesso, registro de auditoria, paginação e recursos de visualização de dados.

---

## Resumo rápido (para iniciantes)

Se você só quer rodar a aplicação sem se preocupar com detalhes técnicos, siga um dos caminhos abaixo.

Opção A — Sem Docker (Windows):

```bash
cd academic_project/backend
python -m venv env
"env\\Scripts\\activate"
pip install -r requirements.txt
set FLASK_APP=app.py
set FLASK_ENV=development
python app.py
```

Opção B — Com Docker:

```bash
cd academic_project
docker compose build
docker compose up
```

A aplicação usa um banco local SQLite em `backend/instance/test.db`. Se precisar "resetar", apague esse arquivo (somente em ambiente local).

### Principais recursos

- **Arquitetura organizada**: Separação clara entre backend (Flask) e frontend (templates/static)
- **Autenticação e autorização**: Sistema completo com 2FA opcional
- **Proteções de segurança**: CSRF, rate limiting e validações de senha
- **Camada de serviços**: Regras de negócio desacopladas das rotas
- **Templates modulares**: Interface organizada em `frontend/templates/`
- **Assets organizados**: CSS, JS e imagens em `frontend/static/`
- **Docker e Docker Compose**: Execução padronizada e conteinerizada
- **Documentação completa**: Guias detalhados em `docs/`

### Linguagens e tecnologias utilizadas

- Python 3.12+ (framework Flask)
- HTML, CSS e JavaScript (front-end com templates Jinja2)
- SQLite (banco local padrão em `instance/test.db`)
- Docker e Docker Compose (execução conteinerizada opcional)

---

## Estrutura do projeto (resumo)

```
academic_project/
├── backend/                    # Código backend (Flask)
│   ├── app.py                 # Ponto de entrada Flask
│   ├── Dockerfile             # Build da imagem
│   ├── requirements.txt       # Dependências Python
│   ├── env_example.txt        # Exemplo de variáveis de ambiente
│   ├── wait-for-db.sh         # Script para aguardar banco
│   ├── routes/                # Blueprints e rotas HTTP
│   ├── services/              # Regras de negócio e integrações
│   ├── models/                # Modelos e camadas de persistência
│   ├── domain/                # Constantes e modelos de domínio
│   └── instance/              # Banco local (SQLite)
├── frontend/                   # Código frontend
│   ├── templates/             # Páginas Jinja2
│   ├── static/                # CSS, JS e imagens
│   │   ├── css/               # Estilos CSS
│   │   ├── js/                # Scripts JavaScript
│   │   └── img/               # Imagens e assets
│   ├── package.json           # Dependências Node.js (se necessário)
│   └── package-lock.json      # Lock file do npm
├── docs/                      # Documentação do projeto
│   ├── README.md              # Este arquivo
│   ├── SETUP_SECURITY.md      # Configurações de segurança
│   ├── RELATORIO_2FA.md       # Documentação 2FA
│   └── ...                    # Outros documentos
├── docker-compose.yaml        # Orquestração dos serviços
└── .gitignore                 # Arquivos ignorados pelo Git
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

1. Navegue para a pasta backend:

```bash
cd academic_project/backend
```

2. Crie e ative um ambiente virtual Python:

```bash
python -m venv env
"env\\Scripts\\activate"
```

3. Instale as dependências:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Variáveis de ambiente:

- Use `env_example.txt` como referência para configurar as variáveis necessárias
- Em Windows (cmd/powershell), defina temporariamente antes de rodar a aplicação, por exemplo:

```bash
set FLASK_APP=app.py
set FLASK_ENV=development
```

5. Executar a aplicação:

```bash
python app.py
```

A aplicação utilizará o SQLite padrão em `backend/instance/test.db`. Caso precise reinicializar, exclua o arquivo `test.db` (ele será recriado conforme a inicialização da app, se previsto pelo código).

---

## Execução com Docker

1. Navegue para a pasta do projeto:

```bash
cd academic_project
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
- Volumes/`backend/instance/` garantem persistência local do banco SQLite.
- O Docker Compose está configurado para usar a estrutura backend/frontend separada.

---

## Nova Organização do Projeto

Este projeto foi reorganizado para melhor separação de responsabilidades:

### 📁 **Estrutura Backend/Frontend**

- **`backend/`**: Contém todo o código Python/Flask
  - Lógica de negócio, rotas, serviços e modelos
  - Configurações Docker e dependências
  - Banco de dados e scripts auxiliares

- **`frontend/`**: Contém toda a interface do usuário
  - Templates Jinja2 organizados
  - Arquivos estáticos (CSS, JS, imagens)
  - Dependências Node.js (se necessário)

- **`docs/`**: Documentação centralizada
  - README, guias de segurança, relatórios
  - Instruções de execução e configuração

### 🔧 **Benefícios da Nova Organização**

1. **Separação clara**: Backend e frontend bem definidos
2. **Manutenção facilitada**: Código organizado por responsabilidade
3. **Escalabilidade**: Estrutura preparada para crescimento
4. **Colaboração**: Equipes podem trabalhar em áreas específicas
5. **Deploy independente**: Possibilidade de deploy separado no futuro

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
