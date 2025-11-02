# 📝 REGISTRO DE MUDANÇAS - IMPLEMENTAÇÃO DE SEGURANÇA

Este documento registra todas as mudanças implementadas para atender aos requisitos de segurança do projeto.

**Data de Início:** Dezembro 2024  
**Objetivo:** Documentar estado ANTES e DEPOIS de cada implementação

---

## 📋 ÍNDICE DE MUDANÇAS

1. [FASE 1: Política de Senha e Rate Limiting](#fase-1)
2. [FASE 2: Sistema de Logs](#fase-2) - *Pendente*
3. [FASE 3: Histórico de Senhas](#fase-3) - *Pendente*
4. [FASE 4: Documentação e Análises](#fase-4) - *Pendente*

---

<a name="fase-1"></a>
## 🚀 FASE 1: POLÍTICA DE SENHA E RATE LIMITING

**Data:** Dezembro 2024  
**Tempo estimado:** 2-3 horas  
**Status:** ✅ Concluído

### 1.1 Correção: Validação de Tamanho Mínimo de Senha (8 → 10 caracteres)

#### Arquivo: `backend/services/password_validation_service.py`

**ANTES:**
```python
def validar_senha_minima(senha):
    """
    Valida senha mínima - código movido do app.py.
    Mantém a lógica original: if not senha or len(senha) < 8
    """
    return not senha or len(senha) < 8
```

**DEPOIS:**
```python
def validar_senha_minima(senha):
    """
    Valida senha mínima conforme política de segurança.
    Requisito: Mínimo de 10 caracteres.
    """
    return not senha or len(senha) < 10
```

**Justificativa:** Requisito do projeto especifica mínimo de 10 caracteres.

---

### 1.2 Correção: Validação em `validation_service.py`

#### Arquivo: `backend/services/validation_service.py`

**ANTES:**
```python
def validar_senha_formato(senha):
    """
    Valida formato de senha - código movido do app.py.
    Mantém a lógica original: if len(senha_nova) < 8
    """
    return len(senha) < 8
```

**DEPOIS:**
```python
def validar_senha_formato(senha):
    """
    Valida formato de senha conforme política de segurança.
    Requisito: Mínimo de 10 caracteres.
    """
    return len(senha) < 10
```

**Justificativa:** Consistência com política de senha (10 caracteres mínimos).

---

### 1.3 Implementação: Validação de Senha Forte no Backend

#### Arquivo: `backend/services/password_validation_service.py`

**ANTES:** Apenas validação de tamanho mínimo

**DEPOIS:**
```python
import re

def validar_senha_forte(senha):
    """
    Valida se a senha atende à política de segurança completa:
    - Mínimo de 10 caracteres
    - Pelo menos 1 letra maiúscula
    - Pelo menos 1 letra minúscula
    - Pelo menos 1 número
    - Pelo menos 1 caractere especial
    
    Retorna: (valida: bool, mensagem_erro: str ou None)
    """
    if not senha:
        return False, "Senha é obrigatória."
    
    if len(senha) < 10:
        return False, "A senha deve ter no mínimo 10 caracteres."
    
    if not re.search(r'[A-Z]', senha):
        return False, "A senha deve conter pelo menos uma letra maiúscula."
    
    if not re.search(r'[a-z]', senha):
        return False, "A senha deve conter pelo menos uma letra minúscula."
    
    if not re.search(r'\d', senha):
        return False, "A senha deve conter pelo menos um número."
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return False, "A senha deve conter pelo menos um caractere especial."
    
    return True, None
```

**Justificativa:** Implementa validação completa de senha forte no backend, conforme requisitos:
- Caracteres alfanuméricos, numéricos e especiais
- Pelo menos uma letra maiúscula

---

### 1.4 Ajuste: Rate Limiting (3 → 5 tentativas, 5min → 10min)

#### Arquivo: `backend/services/rate_limit_service.py`

**ANTES:**
```python
# Configurações do rate limiting
MAX_LOGIN_ATTEMPTS = 3  # Máximo de tentativas permitidas por fase
# Duração do bloqueio temporário em segundos (5 minutos)
BLOCK_DURATION = 300
```

**DEPOIS:**
```python
# Configurações do rate limiting
MAX_LOGIN_ATTEMPTS = 5  # Máximo de tentativas permitidas (requisito: 5 falhas)
# Duração do bloqueio temporário em segundos (10 minutos - requisito do projeto)
BLOCK_DURATION = 600
```

**Justificativa:** Requisito especifica bloqueio após 5 falhas por 10 minutos.

---

### 1.5 Integração: Uso de Validação Forte em Todos os Pontos

#### Arquivos Modificados:

**1. `backend/services/auth_service.py` - Cadastro e Perfil**

**ANTES:**
```python
# Validação: senha mínima de 8 caracteres
if validar_senha_minima(senha):
    flash('A senha deve ter no mínimo 8 caracteres.', 'danger')
    return redirect(url_for('auth.cadastro'))
```

**DEPOIS:**
```python
# Validação: senha forte (mínimo 10 caracteres, maiúscula, minúscula, número, especial)
valida, mensagem_erro = validar_senha_forte(senha)
if not valida:
    flash(mensagem_erro, 'danger')
    return redirect(url_for('auth.cadastro'))
```

**2. `backend/services/password_recovery_service.py` - Recuperação de Senha**

**ANTES:**
```python
if len(nova_senha) < 6:
    return False, "A senha deve ter pelo menos 6 caracteres."
```

**DEPOIS:**
```python
# Validação de senha forte (10 caracteres, maiúscula, minúscula, número, especial)
valida, mensagem_erro = validar_senha_forte(nova_senha)
if not valida:
    return False, mensagem_erro
```

**3. `backend/services/__init__.py` - Exportação**

**ANTES:**
```python
from .password_validation_service import (
    validar_senha_minima, validar_confirmacao_senha,
    ...
)
```

**DEPOIS:**
```python
from .password_validation_service import (
    validar_senha_minima, validar_senha_forte, validar_confirmacao_senha,
    ...
)
```

**Justificativa:** Integração completa da validação forte em todos os pontos onde senhas são criadas ou alteradas (cadastro, alteração de perfil, recuperação).

---

## 📊 RESUMO DA FASE 1

**Arquivos Modificados:**
1. `backend/services/password_validation_service.py` - Função de validação forte + tamanho mínimo
2. `backend/services/validation_service.py` - Tamanho mínimo atualizado
3. `backend/services/password_recovery_service.py` - Validação forte + tamanho mínimo
4. `backend/services/rate_limit_service.py` - Tentativas e tempo de bloqueio
5. `backend/services/auth_service.py` - Integração validação forte (cadastro e perfil)
6. `backend/services/__init__.py` - Exportação da nova função

**Arquivos Criados:**
- Nenhum

**Requisitos Atendidos:**
- ✅ **Tamanho mínimo de senha: 10 caracteres** (era 8)
- ✅ **Validação de senha forte no backend:**
  - Pelo menos 1 letra maiúscula
  - Pelo menos 1 letra minúscula
  - Pelo menos 1 número
  - Pelo menos 1 caractere especial
- ✅ **Bloqueio após 5 tentativas de login** (era 3)
- ✅ **Bloqueio por 10 minutos** (era 5 minutos)

**Pontos de Integração:**
- ✅ Cadastro de novo usuário (instituição e chefe)
- ✅ Alteração de senha no perfil (instituição e chefe)
- ✅ Recuperação de senha (esqueceu senha)

**Impacto:**
- 🔒 **Segurança melhorada:** Senhas agora seguem política forte obrigatória
- 🔒 **Rate limiting ajustado:** Conforme requisitos do projeto
- ✅ **Validação backend:** Não pode ser contornada desabilitando JavaScript
- ✅ **Consistência:** Mesma validação em todos os pontos de entrada de senha

**Testes Realizados:**
- ✅ **Arquivo de testes automatizados criado:** `tests/test_services/test_password_security.py`
- ✅ **Guia de testes manuais criado:** `docs/GUIA_TESTES_FASE1.md`
- 📋 **Testes disponíveis:**
  1. Testes automatizados com pytest
  2. 12 testes manuais detalhados com passo a passo
  3. Checklist completo de validação
  4. Template de relatório de testes

**Como executar testes:**
```bash
# Testes automatizados
cd backend
pytest tests/test_services/test_password_security.py -v

# Ou executar diretamente
python tests/test_services/test_password_security.py
```

**Documentação de testes:** Ver `docs/GUIA_TESTES_FASE1.md` para guia completo.

---

<a name="fase-2"></a>
## 📝 FASE 2: SISTEMA DE LOGS EM ARQUIVO

**Data:** Dezembro 2024  
**Tempo estimado:** 3-4 horas  
**Status:** ✅ Concluído

### 2.1 Criação: Serviço de Logging em Arquivo

#### Arquivo: `backend/services/file_log_service.py` (NOVO)

**Criado:** Sistema completo de logging em arquivo usando biblioteca `logging` do Python.

**Funcionalidades:**
- Diretório de logs: `/app/logs` (na VM)
- Arquivo de log: `security.log`
- Formato: `[YYYY-MM-DD HH:MM:SS] [NÍVEL] [USUÁRIO] [DESCRIÇÃO]`
- Funções específicas para cada tipo de log obrigatório

**Estrutura:**
```python
def registrar_log_seguranca(acao, usuario_nome, descricao, nivel='INFO')
def registrar_log_cadastro_usuario(usuario_nome, tipo_usuario)
def registrar_log_alteracao_usuario(usuario_nome, tipo_alteracao, detalhes='')
def registrar_log_exclusao_usuario(usuario_nome, tipo_usuario)
def registrar_log_erro_autenticacao(usuario_nome_ou_email)
def registrar_log_5_falhas_consecutivas(usuario_nome_ou_email)
def registrar_log_evento_aplicacao(evento, usuario_nome, descricao)
```

**Justificativa:** Implementa sistema de logs em arquivo conforme requisito do projeto.

---

### 2.2 Integração: Log de Cadastro de Novo Usuário

#### Arquivo: `backend/services/user_service.py`

**ANTES:**
```python
        db.session.commit()

        return True, 'Cadastro de Instituição realizado com sucesso! Faça login agora.', nova_instituicao
```

**DEPOIS:**
```python
        db.session.commit()

        # Registrar log de cadastro em arquivo
        from .file_log_service import registrar_log_cadastro_usuario
        registrar_log_cadastro_usuario(nova_instituicao.nome_instituicao, 'instituicao')

        return True, 'Cadastro de Instituição realizado com sucesso! Faça login agora.', nova_instituicao
```

**Também adicionado em:**
- `criar_chefe()` - Log de cadastro de chefe

**Justificativa:** Requisito: "Realizar o registro de eventos em arquivo de log do cadastro de um novo usuário".

---

### 2.3 Integração: Log de Alteração de Dados/Senha

#### Arquivo: `backend/services/user_service.py`

**ANTES:**
```python
        db.session.commit()
        return True, "Perfil atualizado com sucesso!"
```

**DEPOIS:**
```python
        db.session.commit()
        
        # Registrar log de alteração em arquivo
        if tipo_alteracao:
            from .file_log_service import registrar_log_alteracao_usuario
            alteracao_str = ' e '.join(tipo_alteracao)
            registrar_log_alteracao_usuario(chefe.nome, alteracao_str)
        
        return True, "Perfil atualizado com sucesso!"
```

**Implementado em:**
- `atualizar_perfil_chefe()` - Detecta alteração de dados e/ou senha
- `atualizar_perfil_instituicao()` - Detecta alteração de dados e/ou senha

**Justificativa:** Requisito: "Alteração de dados/senha de um usuário informando o nome do usuário, data/hora do evento e a descrição do evento".

---

### 2.4 Integração: Log de Erro de Autenticação

#### Arquivo: `backend/services/auth_service.py`

**ANTES:**
```python
        # =============================================================================
        # LOGIN FALHADO - EXIBE MENSAGEM
        # =============================================================================
        # Rate limiting já foi verificado antes das credenciais
        if mensagem_rate_limit:
```

**DEPOIS:**
```python
        # =============================================================================
        # LOGIN FALHADO - EXIBE MENSAGEM E REGISTRA LOG
        # =============================================================================
        # Registrar log de erro de autenticação em arquivo
        from .file_log_service import registrar_log_erro_autenticacao
        registrar_log_erro_autenticacao(email)
        
        # Rate limiting já foi verificado antes das credenciais
        if mensagem_rate_limit:
```

**Justificativa:** Requisito: "Erro de autenticação do usuário, informando o nome do usuário, data/hora do evento e a descrição do evento".

---

### 2.5 Integração: Log de 5 Falhas Consecutivas

#### Arquivo: `backend/services/rate_limit_service.py`

**ANTES:**
```python
    # Verifica se excedeu o limite (6ª tentativa = bloqueio, após 5 permitidas)
    if dados_email['count'] > MAX_LOGIN_ATTEMPTS:
        if dados_email['fase'] == 1:
```

**DEPOIS:**
```python
    # Verifica se excedeu o limite (6ª tentativa = bloqueio, após 5 permitidas)
    if dados_email['count'] > MAX_LOGIN_ATTEMPTS:
        # Registrar log de 5 falhas consecutivas em arquivo
        from .file_log_service import registrar_log_5_falhas_consecutivas
        registrar_log_5_falhas_consecutivas(email)
        
        if dados_email['fase'] == 1:
```

**Justificativa:** Requisito: "Registro da ocorrência de mais 5 (cinco) falhas de autenticação consecutivas de um usuário no mesmo dia".

---

### 2.6 Integração: Logs de 5 Eventos da Aplicação

#### Arquivos Modificados:

**1. `backend/services/course_service.py` - Inclusão de Curso**
```python
        # Registrar log de evento da aplicação
        from .file_log_service import registrar_log_evento_aplicacao
        instituicao = InstituicaodeEnsino.query.get(id_instituicao)
        if instituicao:
            registrar_log_evento_aplicacao(
                'inclusao_curso',
                instituicao.nome_instituicao,
                f"Inclusão de novo curso '{nome_curso.strip()}' na instituição"
            )
```

**2. `backend/services/student_service.py` - Cadastro de Aluno**
```python
        # Registrar log de evento da aplicação
        from .file_log_service import registrar_log_evento_aplicacao
        if instituicao:
            registrar_log_evento_aplicacao(
                'cadastro_aluno',
                instituicao.nome_instituicao,
                f"Cadastro de novo aluno '{nome_jovem}' no curso '{curso}'"
            )
```

**3. `backend/services/student_service.py` - Alteração de Skills**
```python
        # Registrar log de evento da aplicação
        from .file_log_service import registrar_log_evento_aplicacao
        instituicao = InstituicaodeEnsino.query.get(aluno.id_instituicao)
        if instituicao:
            registrar_log_evento_aplicacao(
                'alteracao_skills_aluno',
                instituicao.nome_instituicao,
                f"Alteração de skills do aluno '{aluno.nome_jovem}' (ID: {aluno.id_aluno})"
            )
```

**4. `backend/services/student_service.py` - Alteração de Endereço**
```python
            # Log de alteração de endereço (se houver)
            if endereco_alterado:
                registrar_log_evento_aplicacao(
                    'alteracao_endereco_aluno',
                    instituicao.nome_instituicao,
                    f"Alteração de endereço de entrega do aluno '{aluno.nome_jovem}' (ID: {aluno.id_aluno})"
                )
```

**5. `backend/services/indication_service.py` - Indicação de Aluno**
```python
        # Registrar log de evento da aplicação
        from .file_log_service import registrar_log_evento_aplicacao
        from domain import Chefe
        chefe = Chefe.query.get(chefe_id)
        aluno_obj = Aluno.query.get(id_aluno)
        if chefe and aluno_obj:
            registrar_log_evento_aplicacao(
                'indicacao_aluno',
                chefe.nome,
                f"Indicação do aluno '{aluno_obj.nome_jovem}' (ID: {id_aluno}) pelo chefe"
            )
```

**6. `backend/services/student_service.py` - Exclusão de Aluno**
```python
        # Registrar log de evento da aplicação
        from .file_log_service import registrar_log_evento_aplicacao
        if instituicao:
            registrar_log_evento_aplicacao(
                'exclusao_aluno',
                instituicao.nome_instituicao,
                f"Exclusão de aluno '{nome_aluno}' (ID: {id_aluno})"
            )
```

**Eventos Registrados:**
1. ✅ Inclusão de novo curso
2. ✅ Cadastro de novo aluno
3. ✅ Alteração de skills de aluno
4. ✅ Alteração de endereço de entrega do aluno
5. ✅ Indicação de aluno
6. ✅ Exclusão de aluno

**Justificativa:** Requisito: "Realizar o registro em arquivo de log de 5 (cinco) eventos (ou situações) realizadas pela aplicação". Implementados 6 eventos para garantir cobertura.

---

### 2.7 Observação: Exclusão de Usuário (Chefe/Instituição)

**Status:** ⚠️ Funcionalidade não encontrada no código

**Ação:** Função `registrar_log_exclusao_usuario()` foi criada e está pronta, mas não há funcionalidade de exclusão de usuários (chefe/instituição) no sistema atual.

**Nota:** Se for necessário implementar exclusão de usuários, basta chamar `registrar_log_exclusao_usuario()` após a exclusão.

---

### 2.8 Configuração: Docker Compose - Volume de Logs

#### Arquivo: `docker-compose.yaml`

**ANTES:**
```yaml
    volumes:
      - ./backend/app.py:/app/app.py
      - ./frontend/static:/app/static
      - ./frontend/templates:/app/templates
```

**DEPOIS:**
```yaml
    volumes:
      - ./backend/app.py:/app/app.py
      - ./frontend/static:/app/static
      - ./frontend/templates:/app/templates
      - ./backend/logs:/app/logs
```

**Justificativa:** Garante persistência dos logs mesmo após reinício do container.

---

## 📊 RESUMO DA FASE 2

**Arquivos Criados:**
1. `backend/services/file_log_service.py` - Serviço completo de logging

**Arquivos Modificados:**
1. `backend/services/__init__.py` - Exportação das funções de log
2. `backend/services/user_service.py` - Logs de cadastro e alteração
3. `backend/services/auth_service.py` - Log de erro de autenticação
4. `backend/services/rate_limit_service.py` - Log de 5 falhas consecutivas
5. `backend/services/course_service.py` - Log de inclusão de curso
6. `backend/services/student_service.py` - Logs de eventos de aluno
7. `backend/services/indication_service.py` - Log de indicação
8. `docker-compose.yaml` - Volume para persistência de logs

**Requisitos Atendidos:**
- ✅ Sistema de logs em arquivo implementado
- ✅ Log de cadastro de novo usuário
- ✅ Log de alteração de dados/senha
- ✅ Log de erro de autenticação
- ✅ Log de 5 falhas consecutivas
- ✅ Log de 5 eventos da aplicação (implementados 6 eventos)
- ⚠️ Log de exclusão de usuário (função pronta, mas funcionalidade não existe)

**Estrutura de Logs:**
- Localização: `/app/logs/security.log` (na VM)
- Formato: `[YYYY-MM-DD HH:MM:SS] [NÍVEL] [USUÁRIO] [DESCRIÇÃO]`
- Níveis: INFO, WARNING, ERROR
- Persistência: Volume Docker montado

**Testes Realizados:**
- ⏳ Pendente - Verificar criação de arquivo e escrita de logs

---

## 🔄 PRÓXIMAS FASES

### FASE 3: Histórico de Senhas
- *A ser documentado*

### FASE 4: Documentação e Análises
- *A ser documentado*

---

**Última atualização:** Dezembro 2024

