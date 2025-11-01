"""
Serviço de Validação de Senha - Funções de validação de senha movidas do app.py.
Código movido para organizar responsabilidades, mantendo a lógica original.
Atualizado para atender requisitos de segurança: mínimo de 10 caracteres e validação forte.
"""

import re


def validar_senha_minima(senha):
    """
    Valida senha mínima conforme política de segurança.
    Requisito: Mínimo de 10 caracteres.
    
    Retorna: True se inválida (senha vazia ou < 10 caracteres), False se válida
    """
    return not senha or len(senha) < 10


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
    
    # Caracteres especiais comuns: !@#$%^&*(),.?":{}|<>
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return False, "A senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?\":{}|<>)."
    
    return True, None


def validar_confirmacao_senha(senha, confirmar_senha):
    """
    Valida confirmação de senha - código movido do app.py.
    Mantém a lógica original: if senha != confirmar_senha
    """
    return senha != confirmar_senha


def validar_campos_obrigatorios_instituicao(nome, email, senha, instituicao_nome, endereco, cursos_selecionados):
    """
    Valida campos obrigatórios para instituição - código movido do app.py.
    Mantém a lógica original: if not nome or not email or not senha or not instituicao_nome or not endereco or not cursos_selecionados
    """
    return not nome or not email or not senha or not instituicao_nome or not endereco or not cursos_selecionados


def validar_campos_obrigatorios_chefe(nome, email, senha, empresa_nome, cargo):
    """
    Valida campos obrigatórios para chefe - código movido do app.py.
    Mantém a lógica original: if not nome or not email or not senha or not empresa_nome or not cargo
    """
    return not nome or not email or not senha or not empresa_nome or not cargo


def validar_campos_obrigatorios_aluno(nome_jovem, data_nascimento, endereco_jovem, contato_jovem, email, curso, formacao, periodo):
    """
    Valida campos obrigatórios para aluno - código movido do app.py.
    Mantém a lógica original: if not nome_jovem or not data_nascimento or not endereco_jovem or not contato_jovem or not email or not curso or not formacao or not periodo
    """
    return not nome_jovem or not data_nascimento or not endereco_jovem or not contato_jovem or not email or not curso or not formacao or not periodo


def validar_campos_obrigatorios_aluno_edicao(nome_jovem, data_nascimento, contato_jovem, email, endereco_jovem, formacao, periodo):
    """
    Valida campos obrigatórios para edição de aluno - código movido do app.py.
    Mantém a lógica original: if not nome_jovem or not data_nascimento or not contato_jovem or not email or not endereco_jovem or not formacao or not periodo
    """
    return not nome_jovem or not data_nascimento or not contato_jovem or not email or not endereco_jovem or not formacao or not periodo
