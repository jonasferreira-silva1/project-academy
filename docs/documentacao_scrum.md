DashTalent – Backlog e Artefatos Ágeis (Fábrica de Software) – v1.0 – 07/10/2025

Documento de Backlog, Histórias, Critérios de Aceitação (DoR) e Definition of Done (DoD)

Este documento, da disciplina Fábrica de Software, consolida o Product Backlog e os principais artefatos ágeis do sistema DashTalent, alinhados à metodologia Scrum, com foco em segurança (2FA, CSRF, logs), usabilidade (UX responsiva) e gestão de usuários (Instituições, Chefes e Alunos). O conteúdo está 100% mapeado aos requisitos (RF/RNF), serviços e infraestrutura Docker do projeto.

Índice:

- 1 Product Backlog (lista priorizada)
- 1.1 Funcionalidades (RF)
- 1.2 Melhorias (RNF/DevOps/UX)
- 1.3 Correções (base em docs e infraestrutura)
- 2 Histórias de Usuário (formato e exemplos)
- 3 Critérios de Aceitação (DoR específico por história)
- 4 Definition of Done (DoD)

1 - Product Backlog (lista priorizada)

1.1 Funcionalidades (RF)

- P1 – Autenticação e Segurança
- US-RF001: Login para Instituições, Chefes e Alunos (Flask-Login)
- US-RF002: Autenticação de Dois Fatores (2FA)
- US-RF006: Recuperação de senha via e-mail
- US-RF007: Rate limiting e proteção CSRF
- P1 – Gestão de Instituições
- US-RF003/RF008: CRUD de Instituições e Cursos por instituição
- US-RF005: Visualização de alunos por instituição
- P1 – Gestão de Alunos
- US-RF002/RF004: Cadastro completo e edição de alunos
- US-RF005: Histórico de evolução e perfil do aluno
- P2 – Sistema de Skills
- US-RF004/RF005: Registro e avaliação de hard/soft skills
- US-RF010: Relatórios de evolução por aluno/curso
- P2 – Sistema de Indicações
- US-RF009: Indicação de alunos por chefes/gestores
- US-RF010: Acompanhamento e notificações por e-mail
- P2 – Logs e Auditoria

- US-RF007/RF017-RF020: Logs de acesso e auditoria consultáveis

  1.2 Melhorias (RNF/DevOps/UX)

- P1 – Segurança
- IM-RNF001: Revisão periódica de CSRF, rate limiting e secrets (.env)
- P2 – Performance
- IM-RNF002: Paginação otimizada e tuning de queries SQLAlchemy
- P2 – Observabilidade
- IM-RNF003: Padrões de logs estruturados e métricas básicas
- P3 – Usabilidade/Acessibilidade
- IM-RNF004: Feedback claro, foco visível e responsividade

  1.3 Correções (base em docs e infraestrutura)

- P1 – Autenticação
- FIX-AUTH-001: Mensagens de erro genéricas no login (sem vazar detalhes)
- P2 – Docker/Compose
- FIX-DOCKER-001: Garantir charset/collation utf8mb4 no MySQL
- FIX-DOCKER-002: Sincronizar variáveis do `.env` no `docker-compose.yaml`
- P2 – Relatórios/CSV
- FIX-REPORT-001: CSV UTF-8 com cabeçalho e separador ","

Observações:

- P1 = alta prioridade; P2 = média; P3 = baixa.
- Itens entram no Sprint Backlog somente após DoR atendido.

2 - Histórias de Usuário (formato e exemplos do DashTalent)

Formato: “Como [usuário], quero [funcionalidade], para [benefício]”.

- US-RF001 – Login
- Como usuário (Instituição/Chefe/Aluno), quero fazer login com e-mail e senha, para acessar minhas funcionalidades com segurança.
- US-RF002 – 2FA
- Como usuário, quero ativar 2FA pelo app autenticador, para aumentar a segurança do meu acesso.
- US-RF006 – Recuperar senha
- Como usuário, quero redefinir minha senha via link enviado por e-mail, para recuperar o acesso quando eu esquecer a senha.
- US-RF003 – Instituições
- Como administrador da instituição, quero cadastrar/editar minha instituição e cursos, para manter os dados acadêmicos atualizados.
- US-RF004 – Alunos (CRUD)
- Como administrador/chefe, quero cadastrar e editar alunos, para manter os dados acadêmicos corretos.
- US-RF005 – Evolução do aluno
- Como chefe, quero visualizar o histórico de evolução do aluno, para acompanhar seu desenvolvimento.
- US-RF004/RF005 – Skills
- Como aluno, quero registrar minhas hard e soft skills, para demonstrar minhas competências.
- US-RF009 – Indicações
- Como chefe, quero indicar um aluno para oportunidades, para conectar talentos a vagas.
- US-RF010 – Relatórios
- Como instituição, quero gerar relatórios e estatísticas, para avaliar desempenho e resultados.
- US-RF017 – Logs/Auditoria
- Como administrador, quero consultar logs de acesso e ações, para auditoria e segurança.

3 - Critérios de Aceitação (DoR específico por história)

Exemplos objetivos e testáveis:

- US-RF001 – Login

- Dado que tenho uma conta válida, quando informo e-mail e senha corretos, então acesso o sistema e vejo o dashboard correspondente ao meu perfil.
- Dado que informo credenciais inválidas, então vejo mensagem genérica de erro sem revelar detalhes sensíveis.

- US-RF002 – 2FA

- Dado que ativei 2FA, quando escaneio o QR e confirmo o código TOTP, então o segundo fator fica habilitado e exigido no próximo login.
- Dado que erro o TOTP 6 dígitos, então recebo mensagem de código inválido e posso tentar novamente.

- US-RF006 – Recuperar senha

- Dado que informo um e-mail cadastrado, quando solicito recuperação, então recebo link único com expiração (≥ 1h) para redefinição.
- Dado que acesso o link no prazo, quando defino nova senha forte, então a senha é atualizada e recebo confirmação.

- US-RF003 – Instituições

- Dado que estou autenticado como instituição, quando envio dados válidos, então a instituição é criada/editada e aparece na listagem.
- Regras: campos obrigatórios validados; feedback de sucesso/erro exibido.

- US-RF004 – Alunos

- Dado que possuo permissão, quando preencho dados obrigatórios do aluno, então o cadastro é salvo e auditado nos logs.

- US-RF004/RF005 – Skills

- Dado que estou no perfil do aluno, quando registro uma skill válida (hard/soft) com pontuação, então ela aparece no histórico do aluno.

- US-RF009 – Indicações

- Dado que sou chefe, quando indico um aluno existente, então a indicação é registrada e envia notificação por e-mail.

- US-RF010 – Relatórios

- Dado que possuo dados suficientes, quando gero relatório, então recebo arquivo/visualização com métricas corretas.

- US-RF017 – Logs/Auditoria
- Dado que sou administrador, quando filtro por usuário e período, então visualizo eventos registrados (login, CRUD, indicações).

Checklist de DoR (antes de ir para Sprint):

- Objetivo e valor claros; dependências mapeadas; dados de exemplo definidos;
- Critérios de aceitação testáveis; riscos/segurança avaliados (CSRF, rate limit, 2FA);
- Impacto em docker-compose.yaml/Dockerfile considerado quando aplicável.

4 - Definition of Done (DoD)

- Implementação cumpre critérios de aceitação e regras de negócio.
- Code review aprovado por 1+ pessoa; padrões de segurança verificados (CSRF, 2FA, secrets, logs).
- Testes:
- Unitários cobrindo casos principais e erros críticos;
- Integração para fluxos com DB/serviços; cenários de autenticação/2FA;
- Cobertura mínima acordada (≥ 70% no módulo afetado).
- Observabilidade: logs estruturados e eventos chave; métricas básicas.
- Documentação atualizada (README/rotas, variáveis .env, scripts Docker).
- Deploy validado no ambiente Docker local (compose up) e plano de rollback.

Anexo – Exemplo consolidado (US-RF002 – 2FA)

- História: Como usuário, quero ativar 2FA pelo app autenticador, para aumentar a segurança do meu acesso.
- Critérios de Aceitação:
- Ativação via QR e verificação TOTP 6 dígitos; erro mostra mensagem genérica;
- Exigência do 2FA em logins seguintes; opção de desativar com confirmação.
- DoR (resumo): dependência de serviço de e-mail/QR, regras definidas, riscos mapeados.
- DoD (resumo): testes unitários/integração, logs de auditoria, doc atualizada, validação em Docker.

Autor: Jonas Ferreira da Silva – Disciplina: Fábrica de Software – Sistema de Gestão DashTalent
