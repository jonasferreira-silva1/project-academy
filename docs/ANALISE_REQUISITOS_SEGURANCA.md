# 📋 ANÁLISE DETALHADA - REQUISITOS DE SEGURANÇA DO PROJETO

**Data da Análise:** Dezembro 2024  
**Projeto:** DashTalent - Projeto de Segurança da Informação

---

## 📊 RESUMO EXECUTIVO

Esta análise detalha quais requisitos de segurança solicitados pelo orientador estão **IMPLEMENTADOS** ✅, **PARCIALMENTE IMPLEMENTADOS** ⚠️ e **NÃO IMPLEMENTADOS** ❌.

---

## 1. REQUISITOS DE AUTENTICAÇÃO E SENHA

### 1.1 Autenticação Baseada em Senha
- **Status:** ✅ **IMPLEMENTADO**
- **Localização:** `backend/services/auth_service.py`, `backend/routes/auth_routes.py`
- **Detalhes:** Sistema de autenticação completo usando Flask-Login e hash de senhas com werkzeug.

### 1.2 Política de Senha

#### 1.2.1 Tamanho Mínimo de 10 Caracteres
- **Status:** ❌ **NÃO ATENDE AO REQUISITO**
- **Atual:** A validação aceita apenas 8 caracteres mínimos
- **Localização:** `backend/services/password_validation_service.py` (linha 12)
- **Problema:**
  ```python
  def validar_senha_minima(senha):
      return not senha or len(senha) < 8  # ❌ DEVERIA SER < 10
  ```
- **Também em:** `backend/services/validation_service.py` (linha 62)
- **Ação Necessária:** Alterar todas as validações de `< 8` para `< 10`

#### 1.2.2 Caracteres Alfanuméricos, Numéricos e Especiais
- **Status:** ⚠️ **PARCIALMENTE IMPLEMENTADO**
- **Localização:** Frontend (`frontend/static/js/cadastro.js`, `frontend/static/js/perfil.js`)
- **Problema:** A validação existe no **frontend** (JavaScript), mas **NÃO** no **backend**
- **Risco:** Validação pode ser contornada se o JavaScript for desabilitado ou requisições forem feitas diretamente via API
- **Ação Necessária:** Implementar validação no backend em `password_validation_service.py`

#### 1.2.3 Pelo Menos Uma Letra Maiúscula
- **Status:** ⚠️ **PARCIALMENTE IMPLEMENTADO**
- **Mesmo problema:** Apenas no frontend, não no backend
- **Ação Necessária:** Implementar validação no backend

#### 1.2.4 Não Usar Últimas 3 Senhas
- **Status:** ❌ **NÃO IMPLEMENTADO**
- **Problema:** Não há modelo de banco de dados para armazenar histórico de senhas
- **Ação Necessária:**
  1. Criar modelo `PasswordHistory` no banco de dados
  2. Armazenar hash das últimas 3 senhas ao alterar senha
  3. Validar ao criar/alterar senha que a nova não está no histórico

### 1.3 Bloqueio de Acesso Após 5 Falhas
- **Status:** ❌ **NÃO ATENDE AO REQUISITO**
- **Atual:** Sistema bloqueia após **3 tentativas** (não 5)
- **Localização:** `backend/services/rate_limit_service.py` (linha 16)
  ```python
  MAX_LOGIN_ATTEMPTS = 3  # ❌ DEVERIA SER 5
  ```
- **Bloqueio:** Sistema atual bloqueia por 5 minutos (300 segundos) - **ATENDE** ao requisito de 10 minutos
- **Problema Adicional:** O bloqueio é temporário (5 min) na primeira fase, e permanente na segunda fase
- **Requisito:** Bloqueio de **10 minutos após 5 falhas**
- **Ação Necessária:**
  1. Alterar `MAX_LOGIN_ATTEMPTS` para 5
  2. Ajustar `BLOCK_DURATION` para 600 segundos (10 minutos)

### 1.4 Armazenamento de Senha
- **Status:** ⚠️ **PARCIALMENTE ATENDE**
- **Atual:** Senhas armazenadas no **banco de dados MySQL** usando hash (werkzeug)
- **Requisito:** "A senha deverá ser armazenada **localmente (em arquivo)** na máquina virtual fazendo uso de algum mecanismo que impeça ser visualizada no arquivo que irá armazená-la (criptografia ou hash)"
- **Problema:** O requisito especifica **arquivo**, não banco de dados
- **Ação Necessária:** Decidir com orientador se banco de dados atende ou se precisa ser arquivo físico. Se arquivo:
  - Criar sistema de armazenamento em arquivo criptografado
  - Usar biblioteca como `cryptography` para criptografar arquivo
  - Manter hash das senhas no arquivo

---

## 2. GERENCIAMENTO DE USUÁRIOS

### 2.1 Cadastro de Usuários
- **Status:** ✅ **IMPLEMENTADO**
- **Localização:** `backend/routes/auth_routes.py`, `backend/services/auth_service.py`
- **Funcionalidades:** Cadastro de instituições e chefes

### 2.2 Alteração de Dados/Senha
- **Status:** ✅ **IMPLEMENTADO**
- **Localização:** `backend/routes/users_routes.py`, `backend/services/user_service.py`

### 2.3 Exclusão de Usuários
- **Status:** ❓ **NÃO VERIFICADO**
- **Ação Necessária:** Verificar se há funcionalidade de exclusão de usuários implementada

---

## 3. COMUNICAÇÃO CRIPTOGRAFADA

### 3.1 HTTPS/TLS
- **Status:** ⚠️ **PREPARADO MAS NÃO CONFIGURADO**
- **Localização:** `backend/app.py` (linhas 62-65)
- **Código Atual:**
  ```python
  use_https = os.getenv('USE_HTTPS', 'False').lower() == 'true'
  SESSION_COOKIE_SECURE=use_https
  ```
- **Problema:** A aplicação está preparada para HTTPS, mas não há configuração de certificado SSL/TLS
- **Ação Necessária:**
  1. Configurar certificado SSL na VM (usando Let's Encrypt/Certbot)
  2. Configurar proxy reverso (Nginx) com SSL
  3. Ou configurar Flask para usar SSL diretamente

---

## 4. SISTEMA DE LOGS

### 4.1 Armazenamento de Logs
- **Status:** ⚠️ **PARCIALMENTE ATENDE**
- **Atual:** Logs armazenados no **banco de dados** (`backend/models/logs.py`)
- **Requisito:** "Realizar o registro de eventos **em arquivo de log**"
- **Problema:** Requisito especifica **arquivo**, não banco de dados
- **Ação Necessária:**
  1. Implementar sistema de escrita em arquivo de log
  2. Usar biblioteca `logging` do Python para escrever em arquivo
  3. Manter estrutura: nome do arquivo, data/hora, descrição do evento

### 4.2 Logs Obrigatórios

#### 4.2.1 Cadastro de Novo Usuário
- **Status:** ❌ **NÃO IMPLEMENTADO**
- **Ação Necessária:** Adicionar chamada `registrar_log()` após criação bem-sucedida de usuário

#### 4.2.2 Alteração de Dados/Senha de Usuário
- **Status:** ❌ **NÃO IMPLEMENTADO**
- **Ação Necessária:** Adicionar log após atualização de perfil/senha

#### 4.2.3 Exclusão de Usuário
- **Status:** ❌ **NÃO IMPLEMENTADO**
- **Ação Necessária:** Implementar funcionalidade de exclusão (se não existir) e adicionar log

#### 4.2.4 Erro de Autenticação
- **Status:** ❌ **NÃO IMPLEMENTADO**
- **Localização:** `backend/services/auth_service.py` (função `processar_login`)
- **Ação Necessária:** Adicionar log quando `usuario_valido` é `None`

#### 4.2.5 5 Falhas Consecutivas no Mesmo Dia
- **Status:** ❌ **NÃO IMPLEMENTADO**
- **Ação Necessária:** 
  1. Modificar `rate_limit_service.py` para rastrear tentativas por dia
  2. Adicionar log quando 5 falhas consecutivas forem detectadas no mesmo dia

#### 4.2.6 5 Eventos da Aplicação
- **Status:** ❓ **NÃO VERIFICADO**
- **Requisito:** "Realizar o registro em arquivo de log de 5 (cinco) eventos (ou situações) realizadas pela aplicação"
- **Ação Necessária:** 
  1. Identificar 5 eventos relevantes da aplicação (ex: inclusão de curso, alteração de skill, etc.)
  2. Implementar logs para cada um desses eventos

---

## 5. ANÁLISE DE RISCO (GRS - GERENCIAMENTO DE RISCO SIMPLIFICADO)

### 5.1 Documentação de GRS
- **Status:** ✅ **DOCUMENTAÇÃO EXISTENTE**
- **Localização:** `docs/RELATORIO_GRS_SIMPLIFICADO.md`
- **Problema:** A documentação atual trata de "Gerenciamento de Requisitos de Software", não "Gerência de Risco Simplificada" de segurança
- **Ação Necessária:** Criar nova documentação seguindo metodologia GRS de segurança:

#### 5.1.1 Riscos a Identificar (Requisito)
- ✅ Malware (uso de Endpoint Protection) - **Mencionar na documentação**
- ❌ Pelo menos 10 outros riscos de segurança - **NÃO ENCONTRADO**

#### 5.1.2 Avaliação de Riscos (Requisito)
- ❌ Como os riscos afetam Confidencialidade, Integridade, Disponibilidade - **NÃO ENCONTRADO**
- ❌ Classificação como "baixo" ou "alto" com justificativa - **NÃO ENCONTRADO**
- ❌ Tratamento de cada risco identificado - **NÃO ENCONTRADO**

### 5.2 Implementação de Ações de Tratamento
- **Status:** ❌ **NÃO DOCUMENTADO/IMPLEMENTADO**
- **Ação Necessária:** Implementar as ações previstas para tratamento dos riscos

---

## 6. ANÁLISE DE VULNERABILIDADES

### 6.1 Análise de Vulnerabilidades Local
- **Status:** ❌ **NÃO ENCONTRADA DOCUMENTAÇÃO**
- **Requisito:** "Realizar uma análise de vulnerabilidades (locais e remotas) no servidor (máquina virtual)"
- **Ação Necessária:**
  1. Executar ferramentas de análise local (ex: Lynis, chkrootkit)
  2. Documentar todas as vulnerabilidades encontradas
  3. Documentar impacto e soluções possíveis

### 6.2 Análise de Vulnerabilidades Remota
- **Status:** ❌ **NÃO ENCONTRADA DOCUMENTAÇÃO**
- **Ação Necessária:**
  1. Executar ferramentas de análise remota (ex: Nmap, OpenVAS, Nessus)
  2. Documentar vulnerabilidades encontradas
  3. Documentar impacto e soluções

### 6.3 Correção de Vulnerabilidades
- **Status:** ❌ **NÃO DOCUMENTADO**
- **Requisito:** "Realizar as correções para as vulnerabilidades encontradas. Caso alguma vulnerabilidade não seja corrigida, justificar o motivo"
- **Ação Necessária:**
  1. Corrigir vulnerabilidades identificadas
  2. Documentar cada correção realizada
  3. Justificar vulnerabilidades não corrigidas (se houver)

### 6.4 Nova Análise Pós-Correção
- **Status:** ❌ **NÃO DOCUMENTADO**
- **Requisito:** "Realizar uma nova análise de vulnerabilidade no servidor (máquina virtual) para constatar a correção das vulnerabilidades"
- **Ação Necessária:** Executar nova análise e comparar com resultados anteriores

---

## 7. ESTRUTURA E DOCUMENTAÇÃO DO PROJETO

### 7.1 Relatório Técnico
- **Status:** ⚠️ **PARCIALMENTE IMPLEMENTADO**
- **Localização:** `docs/DOCUMENTACAO_PRIMEIRA_AVALIACAO.md`
- **Problemas:**
  - ❌ Falta capa completa
  - ❌ Falta índice detalhado
  - ❌ Estrutura não segue exatamente os tópicos solicitados

### 7.2 Storytelling
- **Status:** ✅ **EXISTENTE**
- **Localização:** `docs/Storytelling.txt`

### 7.3 Características da Aplicação
- **Status:** ✅ **IMPLEMENTADO**
- **Localização:** `docs/DOCUMENTACAO_PRIMEIRA_AVALIACAO.md` (seção 2)

### 7.4 Descrição de Testes de Vulnerabilidade
- **Status:** ❌ **NÃO ENCONTRADO**
- **Ação Necessária:** Adicionar seção descrevendo todos os testes realizados

### 7.5 Item de Conclusão
- **Status:** ❌ **NÃO ENCONTRADO**
- **Ação Necessária:** Adicionar seção de conclusão com principais achados

---

## 8. INFRAESTRUTURA

### 8.1 Máquina Virtual Local
- **Status:** ✅ **DOCUMENTADO**
- **Localização:** `docs/INSTRUCOES_EXECUCAO_VM.md`
- **Detalhes:** Instruções para criação e execução em VM local

### 8.2 Sistema Operacional
- **Status:** ✅ **DOCUMENTADO**
- **Detalhes:** Ubuntu 20.04 LTS ou superior

### 8.3 Aplicação Não em Nuvem
- **Status:** ✅ **ATENDE**
- **Detalhes:** Docker Compose em VM local

---

## 📝 CHECKLIST DE AÇÕES NECESSÁRIAS

### Prioridade ALTA (Requisitos Obrigatórios)

- [ ] **1.1** Alterar validação de senha mínima de 8 para 10 caracteres no backend
- [ ] **1.2** Implementar validação de senha forte no backend (alfanuméricos, numéricos, especiais, maiúscula)
- [ ] **1.3** Implementar sistema de histórico de senhas (últimas 3)
- [ ] **1.4** Alterar bloqueio de 3 para 5 tentativas
- [ ] **1.5** Ajustar tempo de bloqueio para 10 minutos
- [ ] **2.1** Verificar/implementar exclusão de usuários
- [ ] **3.1** Configurar HTTPS/SSL na aplicação
- [ ] **4.1** Implementar sistema de logs em arquivo (não apenas banco)
- [ ] **4.2** Adicionar log de cadastro de novo usuário
- [ ] **4.3** Adicionar log de alteração de dados/senha
- [ ] **4.4** Adicionar log de exclusão de usuário
- [ ] **4.5** Adicionar log de erro de autenticação
- [ ] **4.6** Implementar log de 5 falhas consecutivas no mesmo dia
- [ ] **4.7** Implementar logs de 5 eventos da aplicação
- [ ] **5.1** Criar documentação GRS de segurança com pelo menos 11 riscos (incluindo malware)
- [ ] **5.2** Documentar impacto nos 3 pilares (CID)
- [ ] **5.3** Classificar riscos como baixo/alto com justificativa
- [ ] **5.4** Documentar tratamento de cada risco
- [ ] **6.1** Realizar análise de vulnerabilidades local
- [ ] **6.2** Realizar análise de vulnerabilidades remota
- [ ] **6.3** Corrigir vulnerabilidades encontradas
- [ ] **6.4** Realizar nova análise pós-correção
- [ ] **7.1** Completar relatório técnico com capa e índice
- [ ] **7.2** Adicionar seção de testes de vulnerabilidade
- [ ] **7.3** Adicionar seção de conclusão

### Prioridade MÉDIA (Pode precisar esclarecimento)

- [ ] **1.6** Esclarecer com orientador se armazenamento em banco atende requisito de "arquivo local"
- [ ] **1.7** Se necessário, implementar armazenamento em arquivo criptografado

---

## 📊 RESUMO ESTATÍSTICO

| Categoria | ✅ Implementado | ⚠️ Parcial | ❌ Faltando |
|-----------|-----------------|-----------|-------------|
| Autenticação/Senha | 1 | 3 | 4 |
| Gerenciamento Usuários | 2 | 0 | 1 |
| Comunicação Segura | 0 | 1 | 0 |
| Logs | 0 | 1 | 6 |
| Análise de Risco | 0 | 1 | 3 |
| Análise Vulnerabilidades | 0 | 0 | 4 |
| Documentação | 2 | 1 | 3 |
| **TOTAL** | **5** | **7** | **21** |

**Percentual de Conclusão Aproximado:** ~15% dos requisitos de segurança implementados completamente

---

## 🎯 PRÓXIMOS PASSOS RECOMENDADOS

1. **Imediato:** Corrigir política de senha (10 caracteres, validação backend)
2. **Imediato:** Implementar sistema de logs em arquivo
3. **Curto Prazo:** Implementar histórico de senhas e ajustar bloqueio
4. **Médio Prazo:** Realizar análises de vulnerabilidade
5. **Médio Prazo:** Completar documentação GRS de segurança
6. **Longo Prazo:** Configurar HTTPS e completar relatório final

---

**Data de Criação:** Dezembro 2024  
**Versão:** 1.0

