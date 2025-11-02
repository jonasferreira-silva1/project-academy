"""
Serviço de Logging em Arquivo - Gerencia logs de segurança em arquivo local.
Implementado para atender requisitos de segurança: logs devem ser salvos em arquivo.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


# Configurar diretório de logs
LOG_DIR = Path('/app/logs')
LOG_FILE = LOG_DIR / 'security.log'

# Criar diretório de logs se não existir
LOG_DIR.mkdir(exist_ok=True)


def _setup_file_logger():
    """
    Configura o logger para escrever em arquivo.
    Retorna o logger configurado.
    """
    logger = logging.getLogger('security_file_logger')
    
    # Evitar múltiplos handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # Handler para arquivo
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Formato: [YYYY-MM-DD HH:MM:SS] [NÍVEL] [USUÁRIO] [DESCRIÇÃO]
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger


def registrar_log_seguranca(acao, usuario_nome, descricao, nivel='INFO'):
    """
    Registra log de segurança em arquivo.
    
    Args:
        acao (str): Ação realizada (ex: 'cadastro_usuario', 'erro_autenticacao')
        usuario_nome (str): Nome do usuário ou 'Sistema' se não houver usuário
        descricao (str): Descrição detalhada do evento
        nivel (str): Nível do log ('INFO', 'WARNING', 'ERROR'). Default: 'INFO'
    
    Exemplo:
        registrar_log_seguranca(
            'cadastro_usuario',
            'João Silva',
            'Cadastro de novo usuário realizado com sucesso'
        )
    """
    try:
        logger = _setup_file_logger()
        
        # Montar mensagem completa
        mensagem = f"[{acao}] Usuario: {usuario_nome} | {descricao}"
        
        # Registrar no nível apropriado
        nivel_log = getattr(logging, nivel.upper(), logging.INFO)
        logger.log(nivel_log, mensagem)
        
        return True
    except Exception as e:
        # Em caso de erro, tenta logar no console como fallback
        print(f"ERRO ao registrar log em arquivo: {e}")
        return False


def registrar_log_cadastro_usuario(usuario_nome, tipo_usuario):
    """
    Registra log de cadastro de novo usuário.
    
    Args:
        usuario_nome (str): Nome do usuário cadastrado
        tipo_usuario (str): Tipo do usuário ('chefe' ou 'instituicao')
    """
    descricao = f"Cadastro de novo usuário do tipo '{tipo_usuario}' realizado com sucesso"
    registrar_log_seguranca(
        'cadastro_usuario',
        usuario_nome,
        descricao,
        'INFO'
    )


def registrar_log_alteracao_usuario(usuario_nome, tipo_alteracao, detalhes=''):
    """
    Registra log de alteração de dados/senha de usuário.
    
    Args:
        usuario_nome (str): Nome do usuário
        tipo_alteracao (str): Tipo de alteração ('dados', 'senha', 'dados_senha')
        detalhes (str): Detalhes adicionais da alteração
    """
    descricao = f"Alteração de {tipo_alteracao} do usuário"
    if detalhes:
        descricao += f" - {detalhes}"
    registrar_log_seguranca(
        'alteracao_usuario',
        usuario_nome,
        descricao,
        'INFO'
    )


def registrar_log_exclusao_usuario(usuario_nome, tipo_usuario):
    """
    Registra log de exclusão de usuário.
    
    Args:
        usuario_nome (str): Nome do usuário excluído
        tipo_usuario (str): Tipo do usuário ('chefe' ou 'instituicao')
    """
    descricao = f"Exclusão de usuário do tipo '{tipo_usuario}' realizada"
    registrar_log_seguranca(
        'exclusao_usuario',
        usuario_nome,
        descricao,
        'WARNING'
    )


def registrar_log_erro_autenticacao(usuario_nome_ou_email):
    """
    Registra log de erro de autenticação.
    
    Args:
        usuario_nome_ou_email (str): Email ou nome do usuário que tentou fazer login
    """
    descricao = f"Tentativa de autenticação falhou - credenciais inválidas"
    registrar_log_seguranca(
        'erro_autenticacao',
        usuario_nome_ou_email,
        descricao,
        'WARNING'
    )


def registrar_log_5_falhas_consecutivas(usuario_nome_ou_email):
    """
    Registra log de 5 falhas consecutivas de autenticação no mesmo dia.
    
    Args:
        usuario_nome_ou_email (str): Email ou nome do usuário
    """
    descricao = "ALERTA: 5 falhas consecutivas de autenticação detectadas no mesmo dia - possível tentativa de acesso não autorizado"
    registrar_log_seguranca(
        '5_falhas_consecutivas',
        usuario_nome_ou_email,
        descricao,
        'ERROR'
    )


def registrar_log_evento_aplicacao(evento, usuario_nome, descricao):
    """
    Registra log de eventos da aplicação (ex: inclusão de curso, alteração de skill, etc.).
    
    Args:
        evento (str): Nome do evento (ex: 'inclusao_curso', 'alteracao_skill')
        usuario_nome (str): Nome do usuário que realizou a ação
        descricao (str): Descrição detalhada do evento
    """
    registrar_log_seguranca(
        f'evento_aplicacao_{evento}',
        usuario_nome,
        descricao,
        'INFO'
    )

