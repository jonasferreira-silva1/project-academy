@echo off
echo ============================================================
echo EXECUTANDO TESTES COMPLETOS DA FASE 2 - SISTEMA DE LOGS
echo ============================================================
echo.

echo 1. Parando containers...
docker-compose down

echo.
echo 2. Reconstruindo container backend...
docker-compose build backend

echo.
echo 3. Iniciando containers...
docker-compose up -d

echo.
echo 4. Aguardando inicializacao (10 segundos)...
timeout /t 10 /nobreak

echo.
echo 5. Executando testes...
docker exec project-academy-backend-1 python3 -c "import sys; sys.path.insert(0, '/app'); from services.file_log_service import *; import time; print('=== TESTE FASE 2 ==='); print('1. Diretorio:', LOG_DIR.exists()); print('2. Criando log...'); registrar_log_seguranca('teste', 'Sistema', 'Teste', 'INFO'); time.sleep(1); print('3. Arquivo criado:', LOG_FILE.exists()); print('4. Verificando conteudo...'); exec(open(LOG_FILE).read()) if LOG_FILE.exists() else print('ERRO'); print('SUCESSO' if LOG_FILE.exists() else 'ERRO')"

echo.
echo 6. Testando todas as funcoes...
docker exec project-academy-backend-1 python3 -c "import sys; sys.path.insert(0, '/app'); from services.file_log_service import *; import time; print('Testando funcoes...'); registrar_log_cadastro_usuario('Teste', 'chefe'); registrar_log_alteracao_usuario('Teste', 'dados', 'teste'); registrar_log_erro_autenticacao('teste@email.com'); registrar_log_5_falhas_consecutivas('teste@email.com'); registrar_log_evento_aplicacao('teste', 'Usuario', 'Teste'); time.sleep(1); print('Linhas no arquivo:', len(open(LOG_FILE).readlines()) if LOG_FILE.exists() else 0))"

echo.
echo 7. Mostrando ultimas linhas do log...
docker exec project-academy-backend-1 tail -20 /app/logs/security.log

echo.
echo ============================================================
echo TESTES CONCLUIDOS!
echo ============================================================
pause

