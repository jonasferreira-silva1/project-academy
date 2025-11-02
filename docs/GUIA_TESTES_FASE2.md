# 🧪 GUIA DE TESTES - FASE 2: SISTEMA DE LOGS EM ARQUIVO

Este guia explica como testar manualmente o sistema de logs implementado na Fase 2.

---

## 📋 PRÉ-REQUISITOS

1. Docker e Docker Compose instalados
2. Containers em execução: `docker-compose up -d`
3. Acesso ao terminal do container backend

---

## 🚀 EXECUTANDO OS TESTES

### Opção 1: Teste Automatizado (Recomendado)

O arquivo `backend/testar_logs_fase2.py` contém testes automatizados. Para executá-lo:

```bash
# No terminal do HOST, navegue até a pasta do projeto
cd project-academy

# Copie o arquivo para o container e execute
docker cp backend/testar_logs_fase2.py project-academy-backend-1:/app/testar_logs_fase2.py
docker exec project-academy-backend-1 python testar_logs_fase2.py
```

### Opção 2: Testes Manuais Passo a Passo

#### 1. Verificar se o diretório de logs existe

```bash
docker exec project-academy-backend-1 ls -la /app/logs
```

**Resultado esperado:**
```
total 8
drwxr-xr-x 2 root root 4096 Dec XX XX:XX .
drwxr-xr-x 1 root root 4096 Dec XX XX:XX ..
```

#### 2. Acessar o terminal interativo do container

```bash
docker exec -it project-academy-backend-1 bash
```

#### 3. Testar criação de log manualmente

Dentro do container, execute:

```python
python3
```

Depois execute:

```python
from services.file_log_service import (
    registrar_log_seguranca,
    registrar_log_cadastro_usuario,
    registrar_log_erro_autenticacao,
    registrar_log_5_falhas_consecutivas,
    registrar_log_evento_aplicacao,
    LOG_FILE
)

# Teste 1: Log genérico
registrar_log_seguranca('teste', 'UsuarioTeste', 'Teste de log', 'INFO')

# Teste 2: Log de cadastro
registrar_log_cadastro_usuario('Joao Silva', 'chefe')

# Teste 3: Log de erro de autenticação
registrar_log_erro_autenticacao('teste@email.com')

# Teste 4: Log de 5 falhas
registrar_log_5_falhas_consecutivas('teste@email.com')

# Teste 5: Log de evento
registrar_log_evento_aplicacao('inclusao_curso', 'InstituicaoTeste', 'Curso criado')

# Verificar arquivo
import time
time.sleep(0.5)
with open(LOG_FILE, 'r') as f:
    print(f.read())
```

**Resultado esperado:** Arquivo criado com várias linhas de log.

#### 4. Verificar conteúdo do arquivo de log

```bash
# Dentro do container
cat /app/logs/security.log

# Ou no host (se volume estiver montado)
cat backend/logs/security.log
```

**Resultado esperado:** Linhas no formato:
```
[2024-12-XX XX:XX:XX] [INFO] [security_file_logger] [teste] Usuario: UsuarioTeste | Teste de log
[2024-12-XX XX:XX:XX] [INFO] [security_file_logger] [cadastro_usuario] Usuario: Joao Silva | Cadastro de novo usuário do tipo 'chefe' realizado com sucesso
...
```

---

## ✅ CHECKLIST DE TESTES

Marque cada teste conforme for executando:

### Testes Básicos

- [ ] **Diretório de logs criado**
  - Comando: `docker exec project-academy-backend-1 ls -la /app/logs`
  - Resultado: Diretório existe

- [ ] **Arquivo de log criado automaticamente**
  - Ação: Registrar qualquer log
  - Resultado: Arquivo `/app/logs/security.log` existe

- [ ] **Formato do log correto**
  - Verificar: Timestamp, nível, ação, usuário, descrição presentes

### Testes de Funções Específicas

- [ ] **Log de cadastro de usuário**
  - Função: `registrar_log_cadastro_usuario()`
  - Verificar: Contém 'cadastro_usuario' e nome do usuário

- [ ] **Log de alteração de usuário**
  - Função: `registrar_log_alteracao_usuario()`
  - Verificar: Contém 'alteracao_usuario' e tipo de alteração

- [ ] **Log de erro de autenticação**
  - Função: `registrar_log_erro_autenticacao()`
  - Verificar: Contém 'erro_autenticacao' e email

- [ ] **Log de 5 falhas consecutivas**
  - Função: `registrar_log_5_falhas_consecutivas()`
  - Verificar: Contém '5_falhas_consecutivas' e nível ERROR

- [ ] **Log de evento da aplicação**
  - Função: `registrar_log_evento_aplicacao()`
  - Verificar: Contém 'evento_aplicacao_' e descrição

### Testes de Integração

- [ ] **Log de cadastro via interface**
  - Ação: Cadastrar novo usuário (chefe ou instituição) via web
  - Verificar: Log aparece no arquivo

- [ ] **Log de alteração via interface**
  - Ação: Alterar perfil do usuário via web
  - Verificar: Log aparece no arquivo

- [ ] **Log de erro de login**
  - Ação: Tentar fazer login com credenciais inválidas
  - Verificar: Log aparece no arquivo

- [ ] **Log de 5 falhas consecutivas**
  - Ação: Fazer 5 tentativas de login falhadas seguidas
  - Verificar: Log de 5 falhas aparece no arquivo

- [ ] **Log de evento da aplicação**
  - Ações:
    - Cadastrar novo curso
    - Cadastrar novo aluno
    - Alterar skills de aluno
    - Indicar aluno
  - Verificar: Logs aparecem no arquivo

---

## 🔍 VERIFICAÇÕES ADICIONAIS

### Verificar Persistência

1. **Reiniciar container:**
   ```bash
   docker-compose restart backend
   ```

2. **Verificar se logs persistiram:**
   ```bash
   docker exec project-academy-backend-1 cat /app/logs/security.log
   ```
   
   **Resultado esperado:** Logs anteriores ainda estão presentes

### Verificar Volume Docker

1. **No host, verificar se volume existe:**
   ```bash
   ls -la backend/logs/
   ```
   
   **Resultado esperado:** Pasta existe e contém `security.log`

### Verificar Permissões

1. **Verificar permissões do arquivo:**
   ```bash
   docker exec project-academy-backend-1 ls -la /app/logs/security.log
   ```
   
   **Resultado esperado:** Arquivo existe e é legível

---

## 📊 RESULTADOS ESPERADOS

Após executar todos os testes, você deve ter:

✅ Diretório `/app/logs` criado  
✅ Arquivo `/app/logs/security.log` criado  
✅ Logs escritos no formato correto  
✅ Todas as funções de log funcionando  
✅ Logs sendo gerados durante uso normal da aplicação  
✅ Logs persistem após reiniciar o container  

---

## 🐛 RESOLUÇÃO DE PROBLEMAS

### Problema: Diretório não é criado

**Solução:**
```bash
docker exec project-academy-backend-1 mkdir -p /app/logs
```

### Problema: Arquivo não é criado

**Solução:**
- Verificar se a função está sendo chamada
- Verificar permissões: `chmod 777 /app/logs`
- Verificar logs do container: `docker logs project-academy-backend-1`

### Problema: Logs não aparecem

**Solução:**
- Verificar se o código foi rebuildado: `docker-compose build backend`
- Verificar se o container foi reiniciado: `docker-compose restart backend`
- Verificar imports: `docker exec project-academy-backend-1 python -c "from services.file_log_service import *"`

---

## 📝 NOTAS

- Os logs são escritos de forma síncrona, mas pode haver um pequeno delay (0.5s)
- O arquivo cresce indefinidamente - considere implementar rotação de logs no futuro
- Logs são apenas anexados, nunca sobrescritos

---

**Documentação relacionada:**
- `docs/REGISTRO_MUDANCAS.md` - Seção FASE 2
- `docs/RESUMO_FASE2.md` - Resumo executivo

