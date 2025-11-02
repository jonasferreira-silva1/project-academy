"""
Modelo de Histórico de Senhas - Armazena as últimas senhas dos usuários.
Implementado para atender requisito: não permitir reutilizar as últimas 3 senhas.
"""

from datetime import datetime
from models.base import db


class PasswordHistory(db.Model):
    """
    Modelo que armazena o histórico de senhas dos usuários.
    Permite verificar se uma nova senha já foi utilizada recentemente.
    """
    __tablename__ = 'password_history'

    id = db.Column(db.Integer, primary_key=True)
    
    # Tipo e ID do usuário (polimórfico - pode ser chefe ou instituição)
    user_type = db.Column(db.String(20), nullable=False, index=True)  # 'chefe' ou 'instituicao'
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Hash da senha (usando werkzeug para consistência)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Data de criação da entrada no histórico
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False, index=True)

    def __repr__(self):
        return f'<PasswordHistory {self.user_type}:{self.user_id} at {self.created_at}>'

    @staticmethod
    def obter_historico_usuario(user_type, user_id, limite=3):
        """
        Obtém o histórico de senhas de um usuário, ordenado por data (mais recente primeiro).
        
        Args:
            user_type (str): Tipo do usuário ('chefe' ou 'instituicao')
            user_id (int): ID do usuário
            limite (int): Número máximo de registros a retornar (padrão: 3)
        
        Returns:
            list: Lista de objetos PasswordHistory ordenados por data (mais recente primeiro)
        """
        return PasswordHistory.query.filter_by(
            user_type=user_type,
            user_id=user_id
        ).order_by(
            PasswordHistory.created_at.desc()
        ).limit(limite).all()

    @staticmethod
    def limpar_historico_antigo(user_type, user_id, manter=3):
        """
        Remove entradas antigas do histórico, mantendo apenas as N mais recentes.
        
        Args:
            user_type (str): Tipo do usuário ('chefe' ou 'instituicao')
            user_id (int): ID do usuário
            manter (int): Número de senhas a manter no histórico (padrão: 3)
        
        Returns:
            int: Número de registros removidos
        """
        # Obter todas as senhas ordenadas por data (mais recente primeiro)
        todas_senhas = PasswordHistory.query.filter_by(
            user_type=user_type,
            user_id=user_id
        ).order_by(
            PasswordHistory.created_at.desc()
        ).all()

        # Se há mais de 'manter' senhas, remover as mais antigas
        if len(todas_senhas) > manter:
            senhas_para_remover = todas_senhas[manter:]
            for senha in senhas_para_remover:
                db.session.delete(senha)
            return len(senhas_para_remover)
        return 0

