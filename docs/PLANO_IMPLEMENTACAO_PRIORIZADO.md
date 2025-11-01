# 🎯 PLANO DE IMPLEMENTAÇÃO PRIORIZADO

## Recomendações Estratégicas para Implementação dos Requisitos

**Data:** Dezembro 2024  
**Estratégia:** Impacto Rápido → Base Sólida → Funcionalidades Complexas → Documentação

---

## 📋 ESTRATÉGIA GERAL

Sugiro começar pelas correções **mais rápidas e impactantes** primeiro, porque:

1. ✅ Ganho rápido de pontos com o orientador
2. ✅ Validação fácil (mudanças simples)
3. ✅ Base sólida para funcionalidades mais complexas
4. ✅ Menor risco de quebrar código existente

---

## 🚀 FASE 1: CORREÇÕES RÁPIDAS E IMPACTANTES

**Tempo estimado: 2-3 horas | Impacto: ALTO | Dificuldade: BAIXA**

### Prioridade 1.1: Corrigir Política de Senha (Backend)

**Por quê começar aqui:**

- ⚡ Mudanças simples (alterar números e adicionar validações)
- ✅ Impacto imediato na segurança
- ✅ Fácil de testar e validar
- ✅ Base para funcionalidades mais complexas

**O que fazer:**

1. **Aumentar tamanho mínimo de 8 para 10 caracteres**

   - Arquivo: `backend/services/password_validation_service.py` (linha 12)
   - Arquivo: `backend/services/validation_service.py` (linha 62)
   - Arquivo: `backend/services/password_recovery_service.py` (linha 200)
   - Mudança: `len(senha) < 8` → `len(senha) < 10`

2. **Implementar validação completa de senha forte no backend**
   - Criar função `validar_senha_forte()` que verifica:
     - Mínimo 10 caracteres
     - Pelo menos 1 letra maiúscula
     - Pelo menos 1 letra minúscula
     - Pelo menos 1 número
     - Pelo menos 1 caractere especial
   - Substituir todas as validações simples por esta função
   - Arquivos a modificar:
     - `backend/services/password_validation_service.py`
     - `backend/services/auth_service.py` (cadastro e alteração de senha)
     - `backend/services/user_service.py` (atualização de perfil)
     - `backend/services/password_recovery_service.py` (recuperação)

**Vantagens:**

- ✅ Resolve 2 requisitos críticos de uma vez
- ✅ Melhora segurança imediatamente
- ✅ Não quebra funcionalidades existentes
- ✅ Fácil de testar

---

### Prioridade 1.2: Ajustar Rate Limiting (5 tentativas, 10 minutos)

**Por quê fazer junto:**

- ⚡ Mudança muito simples (apenas números)
- ✅ Complementa a segurança de autenticação
- ✅ Fácil de validar

**O que fazer:**

- Arquivo: `backend/services/rate_limit_service.py`
- Linha 16: `MAX_LOGIN_ATTEMPTS = 3` → `MAX_LOGIN_ATTEMPTS = 5`
- Linha 18: `BLOCK_DURATION = 300` (5 min) → `BLOCK_DURATION = 600` (10 min)

**Vantagens:**

- ✅ Resolve requisito crítico
- ✅ Alteração de 2 linhas
- ✅ Teste imediato

---

## 🔧 FASE 2: SISTEMA DE LOGS EM ARQUIVO

**Tempo estimado: 3-4 horas | Impacto: ALTO | Dificuldade: MÉDIA**

### Prioridade 2.1: Implementar Logging em Arquivo

**Por quê fazer em seguida:**

- 🔗 Depende de infraestrutura básica (já existe)
- ✅ Resolve múltiplos requisitos de uma vez
- ✅ Base para todos os logs obrigatórios
- ⚠️ Não é trivial, mas bem definido

**O que fazer:**

1. **Criar serviço de logging em arquivo**

   - Arquivo novo: `backend/services/file_log_service.py`
   - Usar biblioteca `logging` do Python
   - Configurar formato padrão: `[data/hora] [nível] [usuário] [descrição]`
   - Criar arquivo `logs/security.log` na VM

2. **Integrar logs obrigatórios:**
   - ✅ Cadastro de novo usuário (já tem função, só adicionar log)
   - ✅ Alteração de dados/senha (já tem função, só adicionar log)
   - ⚠️ Exclusão de usuário (verificar se existe, se não, implementar)
   - ✅ Erro de autenticação (adicionar no `processar_login`)
   - ✅ 5 falhas consecutivas (modificar `rate_limit_service.py`)
   - ✅ 5 eventos da aplicação (identificar e adicionar)

**Vantagens:**

- ✅ Resolve 6 requisitos de uma vez
- ✅ Sistema centralizado de logs
- ✅ Fácil de expandir depois

**Estrutura sugerida:**

```python
# backend/services/file_log_service.py
import logging
from datetime import datetime

def setup_file_logger():
    """Configura logger para arquivo"""
    logger = logging.getLogger('security_logger')
    # Configurar arquivo de log
    # Formato: [YYYY-MM-DD HH:MM:SS] [NÍVEL] [USUÁRIO] [DESCRIÇÃO]

def registrar_log_seguranca(acao, usuario_nome, descricao):
    """Registra log de segurança em arquivo"""
    # Escreve no arquivo logs/security.log
```

---

## 🏗️ FASE 3: HISTÓRICO DE SENHAS

**Tempo estimado: 4-5 horas | Impacto: MÉDIO | Dificuldade: MÉDIA-ALTA**

### Prioridade 3.1: Implementar Sistema de Histórico de Senhas

**Por quê fazer depois:**

- 🔗 Depende da validação de senha forte (Fase 1)
- ⚠️ Requer mudanças no banco de dados
- ⚠️ Lógica mais complexa
- ✅ Importante para segurança, mas menos crítico que logs

**O que fazer:**

1. **Criar modelo de histórico de senhas**

   - Arquivo novo: `backend/models/password_history.py`
   - Tabela: `password_history`
   - Campos: `id`, `user_type`, `user_id`, `password_hash`, `created_at`
   - Relacionamento com `Chefe` e `InstituicaodeEnsino`

2. **Implementar lógica de histórico**

   - Ao criar/alterar senha:
     - Armazenar hash da nova senha no histórico
     - Manter apenas últimas 3 senhas (deletar mais antigas)
   - Ao validar nova senha:
     - Verificar se nova senha está no histórico (comparar hashes)
     - Rejeitar se estiver nas últimas 3

3. **Integrar validação**
   - Modificar `user_service.py` (atualização de senha)
   - Modificar `auth_service.py` (cadastro)
   - Modificar `password_recovery_service.py` (recuperação)

**Vantagens:**

- ✅ Resolve requisito importante
- ✅ Melhora segurança significativamente
- ⚠️ Requer migração de banco de dados

---

## 📄 FASE 4: DOCUMENTAÇÃO E ANÁLISES

**Tempo estimado: 6-8 horas | Impacto: ALTO (avaliação) | Dificuldade: BAIXA-MÉDIA**

### Prioridade 4.1: Documentação GRS de Segurança

**Por quê fazer depois:**

- 📝 É documentação, não código
- ✅ Pode ser feito em paralelo com outras fases
- ✅ Crítico para aprovação do projeto

**O que fazer:**

1. **Criar novo documento GRS de segurança**
   - Arquivo: `docs/GRS_SEGURANCA_INFORMACAO.md`
   - Identificar 11 riscos (incluindo malware):
     - 1. Malware (Endpoint Protection)
     - 2-11. Outros riscos (ex: SQL Injection, XSS, CSRF, etc.)
   - Para cada risco:
     - Descrição
     - Impacto em Confidencialidade, Integridade, Disponibilidade
     - Classificação: Baixo/Alto com justificativa
     - Tratamento proposto
     - Status da implementação

**Riscos sugeridos:**

1. Malware (Endpoint Protection)
2. SQL Injection
3. Cross-Site Scripting (XSS)
4. Cross-Site Request Forgery (CSRF) - já parcialmente implementado
5. Ataques de força bruta - já parcialmente implementado
6. Senhas fracas - será corrigido na Fase 1
7. Exposição de dados sensíveis
8. Falta de logs de auditoria - será corrigido na Fase 2
9. Comunicação não criptografada - HTTPS não configurado
10. Vulnerabilidades no sistema operacional
11. Falta de backup de dados

---

### Prioridade 4.2: Análise de Vulnerabilidades

**Por quê fazer no final:**

- 🔍 Requer ambiente estável
- ✅ Melhor fazer após correções de segurança
- ✅ Documentação técnica

**O que fazer:**

1. **Análise Local:**

   - Ferramentas: Lynis, chkrootkit, rkhunter
   - Documentar todas as vulnerabilidades encontradas

2. **Análise Remota:**

   - Ferramentas: Nmap, OpenVAS (ou Nessus se disponível)
   - Portas abertas, serviços expostos
   - Vulnerabilidades conhecidas

3. **Correções:**

   - Aplicar correções possíveis
   - Documentar vulnerabilidades não corrigidas e justificativas

4. **Nova Análise:**
   - Executar análise novamente
   - Comparar resultados antes/depois
   - Documentar melhorias

---

## 🎯 ORDEM RECOMENDADA DE EXECUÇÃO

```
SEMANA 1 - FASE 1 (2-3 horas)
├── ✅ 1.1: Corrigir política de senha (10 chars + validação forte)
└── ✅ 1.2: Ajustar rate limiting (5 tentativas, 10 min)

SEMANA 1-2 - FASE 2 (3-4 horas)
├── ✅ 2.1: Criar sistema de logs em arquivo
├── ✅ 2.2: Adicionar logs obrigatórios (6 tipos)
└── ✅ 2.3: Testar e validar logs

SEMANA 2 - FASE 3 (4-5 horas)
├── ✅ 3.1: Criar modelo de histórico de senhas
├── ✅ 3.2: Implementar lógica de histórico
└── ✅ 3.3: Integrar validação

SEMANA 2-3 - FASE 4 (6-8 horas)
├── ✅ 4.1: Documentação GRS de segurança (paralelo)
├── ✅ 4.2: Análise de vulnerabilidades local
├── ✅ 4.3: Análise de vulnerabilidades remota
├── ✅ 4.4: Correções e nova análise
└── ✅ 4.5: Finalizar documentação do relatório
```

---

## 💡 DICAS IMPORTANTES

### ✅ Boas Práticas

1. **Teste cada fase antes de avançar** - Garanta que tudo funciona
2. **Commite frequentemente** - Facilita rollback se necessário
3. **Documente enquanto implementa** - Não deixe para depois
4. **Valide com orientador** - Principalmente sobre armazenamento em arquivo vs banco

### ⚠️ Pontos de Atenção

1. **Armazenamento de senha em arquivo**: Esclarecer com orientador se banco de dados atende
2. **HTTPS**: Pode ser complicado configurar certificado - considerar deixar para depois se não for crítico
3. **Exclusão de usuários**: Verificar se já existe, pode ser apenas log faltando

### 🎓 Sobre a Avaliação

- Fase 1 e 2 são **críticas** - resolvem maioria dos requisitos técnicos
- Fase 3 melhora qualidade, mas não é tão crítica
- Fase 4 é **obrigatória** para aprovação - fazer mesmo que sem tempo para outras fases

---

## 📊 RESUMO DE IMPACTO

| Fase       | Requisitos Resolvidos  | Tempo | Dificuldade       | Prioridade |
| ---------- | ---------------------- | ----- | ----------------- | ---------- |
| **Fase 1** | 3 requisitos críticos  | 2-3h  | ⭐ BAIXA          | 🔥 ALTA    |
| **Fase 2** | 6 requisitos de logs   | 3-4h  | ⭐⭐ MÉDIA        | 🔥 ALTA    |
| **Fase 3** | 1 requisito importante | 4-5h  | ⭐⭐⭐ MÉDIA-ALTA | 🔶 MÉDIA   |
| **Fase 4** | Documentação completa  | 6-8h  | ⭐⭐ MÉDIA        | 🔥 ALTA    |

**Total estimado: 15-20 horas de trabalho**

---

## 🚀 COMEÇANDO AGORA

**Minha recomendação específica:**

1. **HOJE (1-2 horas):** Implementar Fase 1 (política de senha + rate limiting)

   - Correções simples e rápidas
   - Ganho imediato de requisitos atendidos
   - Validação rápida

2. **PRÓXIMOS DIAS (3-4 horas):** Implementar Fase 2 (sistema de logs)

   - Base para todos os logs obrigatórios
   - Resolve 6 requisitos de uma vez

3. **DEPOIS (conforme tempo):** Fase 3 e 4 em paralelo
   - Histórico de senhas (código)
   - GRS e análises (documentação)

---

**🎯 CONCLUSÃO:** Comece pela **FASE 1** - é rápida, impactante e dá momentum para o resto do trabalho!

---

**Data de Criação:** Dezembro 2024  
**Versão:** 1.0
