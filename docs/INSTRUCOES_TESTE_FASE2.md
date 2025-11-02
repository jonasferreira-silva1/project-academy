# 🧪 INSTRUÇÕES PARA TESTAR A FASE 2

## ⚠️ IMPORTANTE: Reconstruir o Container

Antes de testar, você precisa reconstruir o container para incluir o novo código:

```bash
# 1. Parar os containers
docker-compose down

# 2. Reconstruir o backend com as novas mudanças
docker-compose build backend

# 3. Iniciar os containers novamente
docker-compose up -d

# 4. Aguardar alguns segundos para inicializar
sleep 5
```

---

## 🚀 TESTE SIMPLES E DIRETO

Execute estes comandos na ordem:

### Passo 1: Acessar o container
```bash
docker exec -it project-academy-backend-1 bash
```

### Passo 2: Dentro do container, testar o sistema de logs
```bash
python3 -c "
from services.file_log_service import registrar_log_seguranca, LOG_FILE
import time

print('Testando sistema de logs...')
registrar_log_seguranca('teste', 'Sistema', 'Teste do sistema de logs', 'INFO')
time.sleep(1)

if LOG_FILE.exists():
    print(f'✅ Arquivo de log criado: {LOG_FILE}')
    print('\n📄 Primeiras linhas do log:')
    with open(LOG_FILE, 'r') as f:
        linhas = f.readlines()
        for linha in linhas[-5:]:
            print(f'   {linha.strip()}')
else:
    print(f'❌ Arquivo não foi criado: {LOG_FILE}')
"
```

### Passo 3: Testar todas as funções de log
```bash
python3 -c "
from services.file_log_service import *
import time

print('Testando todas as funções de log...\n')

# 1. Log de cadastro
registrar_log_cadastro_usuario('Joao Silva', 'chefe')
print('✅ Log de cadastro registrado')

# 2. Log de alteração
registrar_log_alteracao_usuario('Joao Silva', 'dados', 'Alteração de email')
print('✅ Log de alteração registrado')

# 3. Log de erro de autenticação
registrar_log_erro_autenticacao('teste@email.com')
print('✅ Log de erro de autenticação registrado')

# 4. Log de 5 falhas
registrar_log_5_falhas_consecutivas('teste@email.com')
print('✅ Log de 5 falhas registrado')

# 5. Log de evento
registrar_log_evento_aplicacao('teste_evento', 'UsuarioTeste', 'Evento de teste')
print('✅ Log de evento registrado')

time.sleep(1)

# Verificar arquivo
if LOG_FILE.exists():
    with open(LOG_FILE, 'r') as f:
        linhas = f.readlines()
    print(f'\n📊 Total de linhas no log: {len(linhas)}')
    print('\n📄 Últimas 10 linhas:')
    for linha in linhas[-10:]:
        print(f'   {linha.strip()}')
else:
    print('\n❌ Arquivo de log não existe!')
"
```

### Passo 4: Verificar arquivo completo
```bash
cat /app/logs/security.log
```

---

## ✅ RESULTADOS ESPERADOS

Você deve ver:

1. ✅ Arquivo `/app/logs/security.log` criado
2. ✅ Múltiplas linhas de log no arquivo
3. ✅ Formato correto: `[YYYY-MM-DD HH:MM:SS] [NÍVEL] [security_file_logger] [ação] Usuario: ...`
4. ✅ Todas as funções de log funcionando
5. ✅ Logs contendo as informações corretas (usuário, ação, descrição)

---

## 🔍 TESTE VIA INTERFACE WEB

Após verificar que os logs básicos funcionam:

1. **Cadastrar novo usuário:**
   - Acesse: http://localhost:5000/cadastro
   - Cadastre um novo chefe ou instituição
   - Verifique o log: `docker exec project-academy-backend-1 cat /app/logs/security.log | grep cadastro_usuario`

2. **Fazer login com erro:**
   - Tente fazer login com credenciais inválidas
   - Verifique o log: `docker exec project-academy-backend-1 cat /app/logs/security.log | grep erro_autenticacao`

3. **Fazer 5 tentativas falhadas:**
   - Tente fazer login 5 vezes seguidas com credenciais inválidas
   - Verifique o log: `docker exec project-academy-backend-1 cat /app/logs/security.log | grep 5_falhas`

4. **Alterar perfil:**
   - Faça login com sucesso
   - Altere dados do perfil
   - Verifique o log: `docker exec project-academy-backend-1 cat /app/logs/security.log | grep alteracao_usuario`

5. **Criar curso (se for instituição):**
   - Cadastre um novo curso
   - Verifique o log: `docker exec project-academy-backend-1 cat /app/logs/security.log | grep inclusao_curso`

---

## 🐛 SE ALGO NÃO FUNCIONAR

### Erro: "No module named 'services.file_log_service'"
**Solução:** O container não foi reconstruído. Execute:
```bash
docker-compose build backend
docker-compose up -d
```

### Erro: "Permission denied" ao criar arquivo
**Solução:** Verifique permissões:
```bash
docker exec project-academy-backend-1 mkdir -p /app/logs
docker exec project-academy-backend-1 chmod 777 /app/logs
```

### Arquivo de log não aparece
**Solução:** Verifique se o volume está montado corretamente:
```bash
docker exec project-academy-backend-1 ls -la /app/logs
```

Se o diretório não existir, crie:
```bash
docker exec project-academy-backend-1 mkdir -p /app/logs
```

---

## 📝 PRÓXIMOS PASSOS

Depois que todos os testes passarem:

1. ✅ Documentar resultados dos testes
2. ✅ Confirmar que todos os requisitos estão atendidos
3. ✅ Prosseguir para Fase 3 (Histórico de Senhas)

---

**Execute estes testes e me informe os resultados!** 🚀

