"""
Testes para o serviço de logging em arquivo (Fase 2).
Verifica se os logs estão sendo criados e escritos corretamente.
"""

import os
import time
from pathlib import Path
from datetime import datetime


def test_file_log_service_exists():
    """Testa se o serviço de log existe e pode ser importado."""
    try:
        from services.file_log_service import (
            registrar_log_seguranca,
            registrar_log_cadastro_usuario,
            registrar_log_alteracao_usuario,
            registrar_log_exclusao_usuario,
            registrar_log_erro_autenticacao,
            registrar_log_5_falhas_consecutivas,
            registrar_log_evento_aplicacao
        )
        print("✅ Serviço de log pode ser importado com sucesso")
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar serviço de log: {e}")
        return False


def test_log_directory_creation():
    """Testa se o diretório de logs é criado automaticamente."""
    from services.file_log_service import LOG_DIR
    
    if LOG_DIR.exists():
        print(f"✅ Diretório de logs existe: {LOG_DIR}")
        return True
    else:
        print(f"❌ Diretório de logs não existe: {LOG_DIR}")
        return False


def test_log_file_creation():
    """Testa se o arquivo de log é criado quando um log é registrado."""
    from services.file_log_service import (
        registrar_log_seguranca,
        LOG_FILE
    )
    
    # Limpar arquivo se existir
    if LOG_FILE.exists():
        LOG_FILE.unlink()
    
    # Registrar um log de teste
    resultado = registrar_log_seguranca(
        'teste',
        'Sistema',
        'Teste de criação de arquivo de log',
        'INFO'
    )
    
    # Aguardar um pouco para garantir escrita
    time.sleep(0.5)
    
    if LOG_FILE.exists():
        print(f"✅ Arquivo de log criado: {LOG_FILE}")
        return True
    else:
        print(f"❌ Arquivo de log não foi criado: {LOG_FILE}")
        return False


def test_log_format():
    """Testa se o formato do log está correto."""
    from services.file_log_service import (
        registrar_log_seguranca,
        LOG_FILE
    )
    
    # Limpar arquivo
    if LOG_FILE.exists():
        LOG_FILE.unlink()
    
    # Registrar um log
    registrar_log_seguranca(
        'teste_formato',
        'UsuarioTeste',
        'Teste de formato de log',
        'INFO'
    )
    
    time.sleep(0.5)
    
    # Ler o arquivo
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Verificar se contém elementos esperados
        tem_timestamp = '[' in conteudo and ']' in conteudo
        tem_nivel = '[INFO]' in conteudo or '[WARNING]' in conteudo or '[ERROR]' in conteudo
        tem_usuario = 'UsuarioTeste' in conteudo or 'security_file_logger' in conteudo
        tem_descricao = 'Teste de formato de log' in conteudo or 'teste_formato' in conteudo
        
        if tem_timestamp and tem_nivel and (tem_usuario or tem_descricao):
            print(f"✅ Formato do log está correto")
            print(f"   Exemplo: {conteudo.strip()[:100]}...")
            return True
        else:
            print(f"❌ Formato do log está incorreto")
            print(f"   Conteúdo: {conteudo}")
            return False
    else:
        print(f"❌ Arquivo de log não existe para verificar formato")
        return False


def test_log_cadastro_usuario():
    """Testa função específica de log de cadastro."""
    from services.file_log_service import (
        registrar_log_cadastro_usuario,
        LOG_FILE
    )
    
    # Limpar arquivo
    if LOG_FILE.exists():
        LOG_FILE.unlink()
    
    # Registrar log de cadastro
    registrar_log_cadastro_usuario('TesteUsuario', 'chefe')
    
    time.sleep(0.5)
    
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        if 'cadastro_usuario' in conteudo and 'TesteUsuario' in conteudo:
            print(f"✅ Log de cadastro funcionando corretamente")
            return True
        else:
            print(f"❌ Log de cadastro não encontrado no arquivo")
            return False
    else:
        print(f"❌ Arquivo de log não foi criado")
        return False


def test_log_alteracao_usuario():
    """Testa função específica de log de alteração."""
    from services.file_log_service import (
        registrar_log_alteracao_usuario,
        LOG_FILE
    )
    
    # Registrar log de alteração
    registrar_log_alteracao_usuario('TesteUsuario', 'dados', 'Alteração de email')
    
    time.sleep(0.5)
    
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        if 'alteracao_usuario' in conteudo and 'TesteUsuario' in conteudo:
            print(f"✅ Log de alteração funcionando corretamente")
            return True
        else:
            print(f"❌ Log de alteração não encontrado no arquivo")
            return False
    else:
        print(f"❌ Arquivo de log não foi criado")
        return False


def test_log_erro_autenticacao():
    """Testa função específica de log de erro de autenticação."""
    from services.file_log_service import (
        registrar_log_erro_autenticacao,
        LOG_FILE
    )
    
    # Registrar log de erro
    registrar_log_erro_autenticacao('teste@email.com')
    
    time.sleep(0.5)
    
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        if 'erro_autenticacao' in conteudo and 'teste@email.com' in conteudo:
            print(f"✅ Log de erro de autenticação funcionando corretamente")
            return True
        else:
            print(f"❌ Log de erro de autenticação não encontrado")
            return False
    else:
        print(f"❌ Arquivo de log não foi criado")
        return False


def test_log_5_falhas():
    """Testa função específica de log de 5 falhas consecutivas."""
    from services.file_log_service import (
        registrar_log_5_falhas_consecutivas,
        LOG_FILE
    )
    
    # Registrar log de 5 falhas
    registrar_log_5_falhas_consecutivas('teste@email.com')
    
    time.sleep(0.5)
    
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        if '5_falhas_consecutivas' in conteudo and 'teste@email.com' in conteudo:
            print(f"✅ Log de 5 falhas consecutivas funcionando corretamente")
            return True
        else:
            print(f"❌ Log de 5 falhas não encontrado")
            return False
    else:
        print(f"❌ Arquivo de log não foi criado")
        return False


def test_log_evento_aplicacao():
    """Testa função específica de log de eventos da aplicação."""
    from services.file_log_service import (
        registrar_log_evento_aplicacao,
        LOG_FILE
    )
    
    # Registrar log de evento
    registrar_log_evento_aplicacao(
        'teste_evento',
        'UsuarioTeste',
        'Evento de teste da aplicação'
    )
    
    time.sleep(0.5)
    
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        if 'evento_aplicacao_teste_evento' in conteudo and 'UsuarioTeste' in conteudo:
            print(f"✅ Log de evento da aplicação funcionando corretamente")
            return True
        else:
            print(f"❌ Log de evento não encontrado")
            return False
    else:
        print(f"❌ Arquivo de log não foi criado")
        return False


def test_multiple_logs():
    """Testa se múltiplos logs são escritos no mesmo arquivo."""
    from services.file_log_service import (
        registrar_log_seguranca,
        LOG_FILE
    )
    
    # Limpar arquivo
    if LOG_FILE.exists():
        LOG_FILE.unlink()
    
    # Registrar múltiplos logs
    for i in range(3):
        registrar_log_seguranca(
            f'teste_{i}',
            f'Usuario{i}',
            f'Log de teste número {i}',
            'INFO'
        )
    
    time.sleep(0.5)
    
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        if len(linhas) >= 3:
            print(f"✅ Múltiplos logs estão sendo escritos corretamente ({len(linhas)} linhas)")
            return True
        else:
            print(f"❌ Esperado 3+ linhas, encontrado {len(linhas)}")
            return False
    else:
        print(f"❌ Arquivo de log não foi criado")
        return False


def executar_todos_testes():
    """Executa todos os testes e retorna o resultado."""
    print("\n" + "="*60)
    print("TESTES DO SISTEMA DE LOGS EM ARQUIVO - FASE 2")
    print("="*60 + "\n")
    
    testes = [
        ("Importação do serviço", test_file_log_service_exists),
        ("Criação do diretório de logs", test_log_directory_creation),
        ("Criação do arquivo de log", test_log_file_creation),
        ("Formato do log", test_log_format),
        ("Log de cadastro de usuário", test_log_cadastro_usuario),
        ("Log de alteração de usuário", test_log_alteracao_usuario),
        ("Log de erro de autenticação", test_log_erro_autenticacao),
        ("Log de 5 falhas consecutivas", test_log_5_falhas),
        ("Log de evento da aplicação", test_log_evento_aplicacao),
        ("Múltiplos logs no arquivo", test_multiple_logs),
    ]
    
    resultados = []
    for nome, teste in testes:
        print(f"\n🧪 {nome}...")
        try:
            resultado = teste()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"❌ Erro ao executar teste: {e}")
            resultados.append((nome, False))
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    total = len(resultados)
    passou = sum(1 for _, r in resultados if r)
    falhou = total - passou
    
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{status} - {nome}")
    
    print("\n" + "-"*60)
    print(f"Total: {total} | Passou: {passou} | Falhou: {falhou}")
    print("-"*60)
    
    if falhou == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM! Sistema de logs está funcionando.")
    else:
        print(f"\n⚠️  {falhou} teste(s) falharam. Revise os erros acima.")
    
    return falhou == 0


if __name__ == "__main__":
    sucesso = executar_todos_testes()
    exit(0 if sucesso else 1)

