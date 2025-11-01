# 🧪 GUIA DE TESTES - FASE 1
## Política de Senha e Rate Limiting

**Data:** Dezembro 2024  
**Objetivo:** Validar todas as implementações da Fase 1

---

## 📋 ÍNDICE

1. [Testes Automatizados](#testes-automatizados)
2. [Testes Manuais - Validação de Senha](#testes-manuais-senha)
3. [Testes Manuais - Rate Limiting](#testes-manuais-rate-limiting)
4. [Checklist Completo](#checklist-completo)

---

## 🤖 TESTES AUTOMATIZADOS

### Como Executar

#### Opção 1: Usando pytest (Recomendado)

```bash
# No diretório do backend
cd backend

# Executar todos os testes da Fase 1
pytest tests/test_services/test_password_security.py -v

# Executar teste específico
pytest tests/test_services/test_password_security.py::TestPasswordMinima -v

# Ver saída detalhada
pytest tests/test_services/test_password_security.py -v -s
```

#### Opção 2: Executar diretamente

```bash
cd backend
python tests/test_services/test_password_security.py
```

### Testes Incluídos

- ✅ Validação de tamanho mínimo (10 caracteres)
- ✅ Validação de senha forte (maiúscula, minúscula, número, especial)
- ✅ Rate limiting (5 tentativas, 10 minutos)

---

## 🔐 TESTES MANUAIS - VALIDAÇÃO DE SENHA

### Teste 1: Cadastro com Senha Fraca (Tamanho < 10)

**Objetivo:** Verificar que senhas com menos de 10 caracteres são rejeitadas.

**Passos:**
1. Acesse `/cadastro`
2. Preencha todos os campos obrigatórios
3. Digite uma senha com **9 caracteres**: `Senha123!`
4. Confirme a senha
5. Clique em "Cadastrar"

**Resultado Esperado:**
- ❌ Cadastro não deve ser criado
- ⚠️ Mensagem de erro: "A senha deve ter no mínimo 10 caracteres."
- 🎯 **Status:** ✅ Passou ou ❌ Falhou

---

### Teste 2: Cadastro sem Letra Maiúscula

**Objetivo:** Verificar que senhas sem maiúscula são rejeitadas.

**Passos:**
1. Acesse `/cadastro`
2. Preencha todos os campos
3. Digite senha **sem maiúscula**: `minhasenha123!` (11 caracteres)
4. Confirme a senha
5. Clique em "Cadastrar"

**Resultado Esperado:**
- ❌ Cadastro não deve ser criado
- ⚠️ Mensagem de erro: "A senha deve conter pelo menos uma letra maiúscula."
- 🎯 **Status:** ✅ Passou ou ❌ Falhou

---

### Teste 3: Cadastro sem Letra Minúscula

**Objetivo:** Verificar que senhas sem minúscula são rejeitadas.

**Passos:**
1. Acesse `/cadastro`
2. Preencha todos os campos
3. Digite senha **sem minúscula**: `MINHASENHA123!` (14 caracteres)
4. Confirme a senha
5. Clique em "Cadastrar"

**Resultado Esperado:**
- ❌ Cadastro não deve ser criado
- ⚠️ Mensagem de erro: "A senha deve conter pelo menos uma letra minúscula."
- 🎯 **Status:** ✅ Passou ou ❌ Falhou

---

### Teste 4: Cadastro sem Número

**Objetivo:** Verificar que senhas sem número são rejeitadas.

**Passos:**
1. Acesse `/cadastro`
2. Preencha todos os campos
3. Digite senha **sem número**: `MinhaSenha!@#` (13 caracteres)
4. Confirme a senha
5. Clique em "Cadastrar"

**Resultado Esperado:**
- ❌ Cadastro não deve ser criado
- ⚠️ Mensagem de erro: "A senha deve conter pelo menos um número."
- 🎯 **Status:** ✅ Passou ou ❌ Falhou

---

### Teste 5: Cadastro sem Caractere Especial

**Objetivo:** Verificar que senhas sem caractere especial são rejeitadas.

**Passos:**
1. Acesse `/cadastro`
2. Preencha todos os campos
3. Digite senha **sem especial**: `MinhaSenha123` (13 caracteres)
4. Confirme a senha
5. Clique em "Cadastrar"

**Resultado Esperado:**
- ❌ Cadastro não deve ser criado
- ⚠️ Mensagem de erro: "A senha deve conter pelo menos um caractere especial."
- 🎯 **Status:** ✅ Passou ou ❌ Falhou

---

### Teste 6: Cadastro com Senha Forte (Sucesso)

**Objetivo:** Verificar que senhas que atendem todos os critérios são aceitas.

**Passos:**
1. Acesse `/cadastro`
2. Preencha todos os campos
3. Digite senha **forte**: `MinhaSenha123!` (14 caracteres)
   - ✅ 10+ caracteres
   - ✅ Tem maiúscula (M, S)
   - ✅ Tem minúscula (inha, enha)
   - ✅ Tem número (123)
   - ✅ Tem especial (!)
4. Confirme a senha
5. Clique em "Cadastrar"

**Resultado Esperado:**
- ✅ Cadastro deve ser criado com sucesso
- ✅ Redirecionamento para página de login
- ⚠️ Mensagem: "Cadastro realizado com sucesso! Faça login agora."
- 🎯 **Status:** ✅ Passou ou ❌ Falhou

---

### Teste 7: Alteração de Senha no Perfil

**Objetivo:** Verificar validação forte na alteração de senha.

**Passos:**
1. Faça login na aplicação
2. Acesse `/perfil`
3. Digite uma nova senha **fraca**: `Senha123!` (9 caracteres)
4. Clique em "Salvar" ou "Atualizar"

**Resultado Esperado:**
- ❌ Senha não deve ser alterada
- ⚠️ Mensagem de erro específica do problema (tamanho, maiúscula, etc.)
- 🎯 **Status:** ✅ Passou ou ❌ Falhou

---

### Teste 8: Recuperação de Senha

**Objetivo:** Verificar validação forte na recuperação de senha.

**Passos:**
1. Acesse `/esqueceu-senha` ou similar
2. Digite um email cadastrado
3. Verifique código recebido por email
4. Digite nova senha **fraca**: `Senha123!` (9 caracteres)
5. Confirme a senha

**Resultado Esperado:**
- ❌ Senha não deve ser alterada
- ⚠️ Mensagem de erro: "A senha deve ter no mínimo 10 caracteres."
- 🎯 **Status:** ✅ Passou ou ❌ Falhou

---

## 🔒 TESTES MANUAIS - RATE LIMITING

### Teste 9: 5 Tentativas de Login Permitidas

**Objetivo:** Verificar que são permitidas exatamente 5 tentativas antes do bloqueio.

**Passos:**
1. Acesse `/login`
2. Digite um email válido
3. Digite uma **senha incorreta**
4. Clique em "Login"
5. Repita os passos 2-4 mais **4 vezes** (total de 5 tentativas)

**Resultado Esperado:**
- ✅ Primeiras 4 tentativas: Permitidas com mensagem de erro
- ✅ 5ª tentativa: Permitida (última antes do bloqueio)
- ⚠️ Mensagens devem informar tentativas restantes
- 🎯 **Status:** ✅ Passou ou ❌ Falhou

---

### Teste 10: Bloqueio Após 5 Tentativas

**Objetivo:** Verificar que o 6º tentativa de login bloqueia o acesso.

**Passos:**
1. Continue do Teste 9 (5 tentativas já realizadas)
2. Tente fazer login **mais uma vez** (6ª tentativa)
3. Verifique a mensagem exibida

**Resultado Esperado:**
- ❌ Login não deve ser permitido
- ⚠️ Mensagem: "Muitas tentativas de login. Bloqueado por 10 minutos."
- ⏰ Bloqueio deve durar **10 minutos** (600 segundos)
- 🎯 **Status:** ✅ Passou ou ❌ Falhou

---

### Teste 11: Verificar Duração do Bloqueio (10 minutos)

**Objetivo:** Verificar que o bloqueio dura exatamente 10 minutos.

**Passos:**
1. Continue do Teste 10 (usuário bloqueado)
2. Anote o horário do bloqueio
3. Tente fazer login imediatamente - deve estar bloqueado
4. Aguarde 9 minutos e tente novamente - ainda deve estar bloqueado
5. Aguarde até completar 10 minutos
6. Tente fazer login novamente

**Resultado Esperado:**
- ❌ Login bloqueado nos primeiros 10 minutos
- ✅ Após 10 minutos: Login deve ser permitido (mas ainda com senha errada)
- ⚠️ Mensagem deve indicar tempo restante durante o bloqueio
- 🎯 **Status:** ✅ Passou ou ❌ Falhou

**Nota:** Este teste é demorado (10 minutos). Para testes rápidos, ajuste temporariamente `BLOCK_DURATION` para 60 segundos.

---

### Teste 12: Reset de Bloqueio Após Login Bem-Sucedido

**Objetivo:** Verificar que login bem-sucedido reseta o contador de tentativas.

**Passos:**
1. Faça **4 tentativas** de login com senha errada
2. Na 5ª tentativa, digite a **senha correta**
3. Faça login com sucesso
4. Faça logout
5. Tente fazer login novamente com senha errada

**Resultado Esperado:**
- ✅ Login bem-sucedido na 5ª tentativa
- ✅ Após logout, tentativas são resetadas
- ✅ Nova tentativa com senha errada não deve considerar tentativas anteriores
- 🎯 **Status:** ✅ Passou ou ❌ Falhou

---

## 📊 CHECKLIST COMPLETO

### Validação de Senha

- [ ] **Teste 1:** Senha < 10 caracteres rejeitada no cadastro
- [ ] **Teste 2:** Senha sem maiúscula rejeitada
- [ ] **Teste 3:** Senha sem minúscula rejeitada
- [ ] **Teste 4:** Senha sem número rejeitada
- [ ] **Teste 5:** Senha sem caractere especial rejeitada
- [ ] **Teste 6:** Senha forte aceita no cadastro
- [ ] **Teste 7:** Validação forte funciona na alteração de perfil
- [ ] **Teste 8:** Validação forte funciona na recuperação de senha

### Rate Limiting

- [ ] **Teste 9:** 5 tentativas são permitidas antes do bloqueio
- [ ] **Teste 10:** 6ª tentativa bloqueia o acesso
- [ ] **Teste 11:** Bloqueio dura 10 minutos (verificar)
- [ ] **Teste 12:** Login bem-sucedido reseta contador

### Testes Automatizados

- [ ] Executar `pytest tests/test_services/test_password_security.py -v`
- [ ] Todos os testes devem passar
- [ ] Verificar relatório de cobertura (opcional)

---

## 📝 TEMPLATE DE RELATÓRIO DE TESTES

```markdown
# Relatório de Testes - Fase 1

**Data:** [DATA]
**Testador:** [NOME]
**Ambiente:** [DESCRIÇÃO]

## Resultados

### Validação de Senha
- Teste 1: [✅/❌] - [OBSERVAÇÕES]
- Teste 2: [✅/❌] - [OBSERVAÇÕES]
- ...
- Teste 8: [✅/❌] - [OBSERVAÇÕES]

### Rate Limiting
- Teste 9: [✅/❌] - [OBSERVAÇÕES]
- Teste 10: [✅/❌] - [OBSERVAÇÕES]
- Teste 11: [✅/❌] - [OBSERVAÇÕES]
- Teste 12: [✅/❌] - [OBSERVAÇÕES]

### Testes Automatizados
- Total de testes: [NÚMERO]
- Passaram: [NÚMERO]
- Falharam: [NÚMERO]

## Problemas Encontrados
1. [DESCRIÇÃO DO PROBLEMA]

## Observações
[QUAISQUER OBSERVAÇÕES RELEVANTES]
```

---

## 🚀 EXECUTANDO TESTES RÁPIDOS

Para um teste rápido sem executar todos os cenários:

### Teste Mínimo (5 minutos)

1. ✅ Cadastro com senha forte: `MinhaSenha123!`
2. ❌ Cadastro com senha fraca: `Senha123!` (9 caracteres)
3. ❌ 6 tentativas de login com senha errada (verificar bloqueio)

Se esses 3 testes passarem, a implementação básica está funcionando!

---

## ⚠️ PROBLEMAS COMUNS

### Problema: Testes falham mas aplicação funciona
**Solução:** Verificar se os arquivos foram salvos e a aplicação foi reiniciada.

### Problema: Validação não aparece no frontend
**Solução:** Validação está no backend. Teste enviando requisição diretamente ou desabilitando JavaScript.

### Problema: Rate limiting não funciona
**Solução:** Verificar se `rate_limit_service.py` foi atualizado e aplicação reiniciada.

---

**Boa sorte com os testes! 🎉**

