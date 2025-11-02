"""
Serviço de Histórico de Senhas - Gerencia histórico das últimas senhas dos usuários.
Implementado para atender requisito: não permitir reutilizar as últimas 3 senhas.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from domain import db, PasswordHistory


def verificar_senha_no_historico(user_type, user_id, nova_senha):
    """
    Verifica se a nova senha está no histórico das últimas 3 senhas do usuário.
    
    Args:
        user_type (str): Tipo do usuário ('chefe' ou 'instituicao')
        user_id (int): ID do usuário
        nova_senha (str): Nova senha a ser verificada (em texto plano)
    
    Returns:
        tuple: (esta_no_historico: bool, mensagem: str)
            - Se True: senha está no histórico e não pode ser reutilizada
            - Se False: senha não está no histórico e pode ser usada
    """
    # Obter histórico das últimas 3 senhas
    historico = PasswordHistory.obter_historico_usuario(user_type, user_id, limite=3)
    
    # Verificar se algum hash do histórico corresponde à nova senha
    # Nota: NÃO gerar novo hash aqui - comparar diretamente com os hashes do histórico
    for entrada_historico in historico:
        # Usar check_password_hash para comparar (werkzeug compara hashes corretamente)
        if check_password_hash(entrada_historico.password_hash, nova_senha):
            return True, "Você não pode reutilizar uma das suas últimas 3 senhas. Por favor, escolha uma senha diferente."
    
    return False, None


def salvar_senha_no_historico(user_type, user_id, senha_atual_hash):
    """
    Salva a senha atual (hash) no histórico antes de alterar para uma nova senha.
    
    Args:
        user_type (str): Tipo do usuário ('chefe' ou 'instituicao')
        user_id (int): ID do usuário
        senha_atual_hash (str): Hash da senha atual (já em formato hash)
    
    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    try:
        # Criar nova entrada no histórico
        nova_entrada = PasswordHistory(
            user_type=user_type,
            user_id=user_id,
            password_hash=senha_atual_hash  # Já está em formato hash
        )
        
        db.session.add(nova_entrada)
        db.session.commit()
        
        # Limpar histórico antigo, mantendo apenas as 3 mais recentes
        PasswordHistory.limpar_historico_antigo(user_type, user_id, manter=3)
        db.session.commit()
        
        return True
    except Exception as e:
        db.session.rollback()
        print(f"ERRO ao salvar senha no histórico: {e}")
        return False


def salvar_senha_texto_plano_no_historico(user_type, user_id, senha_texto_plano):
    """
    Salva uma senha (em texto plano) no histórico após gerar o hash.
    Útil quando se tem a senha em texto plano antes de salvar.
    
    Args:
        user_type (str): Tipo do usuário ('chefe' ou 'instituicao')
        user_id (int): ID do usuário
        senha_texto_plano (str): Senha em texto plano
    
    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    try:
        # Gerar hash da senha
        senha_hash = generate_password_hash(senha_texto_plano)
        
        # Salvar no histórico
        nova_entrada = PasswordHistory(
            user_type=user_type,
            user_id=user_id,
            password_hash=senha_hash
        )
        
        db.session.add(nova_entrada)
        db.session.commit()
        
        # Limpar histórico antigo, mantendo apenas as 3 mais recentes
        PasswordHistory.limpar_historico_antigo(user_type, user_id, manter=3)
        db.session.commit()
        
        return True
    except Exception as e:
        db.session.rollback()
        print(f"ERRO ao salvar senha no histórico: {e}")
        return False


def obter_historico_completo(user_type, user_id):
    """
    Obtém o histórico completo de senhas de um usuário (para debug/admin).
    
    Args:
        user_type (str): Tipo do usuário ('chefe' ou 'instituicao')
        user_id (int): ID do usuário
    
    Returns:
        list: Lista de objetos PasswordHistory ordenados por data (mais recente primeiro)
    """
    return PasswordHistory.obter_historico_usuario(user_type, user_id, limite=None)

