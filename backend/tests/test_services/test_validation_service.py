"""
Testes para o serviço de validação.
"""

import pytest
from services.validation_service import (
    validar_email_formato,
    validar_periodo_formato,
    validar_contato_formato,
    validar_skill_valor,
    validar_nome_formato,
    validar_cargo_formato,
    validar_senha_formato,
    validar_nota_mec_formato,
    validar_modalidade_formato
)


class TestValidationService:
    """Testes para o serviço de validação."""

    def test_validar_email_formato_valido(self):
        """Testa validação de email com formato válido."""
        emails_validos = [
            'usuario@email.com',
            'teste@dominio.org',
            'user.name@example.co.uk',
            'user+tag@domain.com'
        ]

        for email in emails_validos:
            assert not validar_email_formato(
                email), f"Email {email} deveria ser válido"

    def test_validar_email_formato_invalido(self):
        """Testa validação de email com formato inválido."""
        emails_invalidos = [
            'email_sem_arroba.com',
            'email@sem_ponto',
            '@dominio.com',
            'usuario@',
            '',
            'espaço @email.com'
        ]

        for email in emails_invalidos:
            assert validar_email_formato(
                email), f"Email {email} deveria ser inválido"

    def test_validar_periodo_formato_valido(self):
        """Testa validação de período com formato válido."""
        periodos_validos = ['1º', '2º', '3º', '4º',
                            '5º', '6º', '7º', '8º', '9º', '10º']

        for periodo in periodos_validos:
            assert not validar_periodo_formato(
                periodo), f"Período {periodo} deveria ser válido"

    def test_validar_periodo_formato_invalido(self):
        """Testa validação de período com formato inválido."""
        periodos_invalidos = ['0º', '11º', '1', 'primeiro', '', '1o']

        for periodo in periodos_invalidos:
            assert validar_periodo_formato(
                periodo), f"Período {periodo} deveria ser inválido"

    def test_validar_contato_formato_valido(self):
        """Testa validação de contato com formato válido."""
        contatos_validos = [
            '11999999999',
            '11987654321',
            '(11)99999-9999',
            '(11)98765-4321',
            '+5511999999999'
        ]

        for contato in contatos_validos:
            assert not validar_contato_formato(
                contato), f"Contato {contato} deveria ser válido"

    def test_validar_contato_formato_invalido(self):
        """Testa validação de contato com formato inválido."""
        contatos_invalidos = [
            '123',
            'abc12345678',
            '1199999999',  # Muito curto
            '119999999999',  # Muito longo
            ''
        ]

        for contato in contatos_invalidos:
            assert validar_contato_formato(
                contato), f"Contato {contato} deveria ser inválido"

    def test_validar_skill_valor_valido(self):
        """Testa validação de skill com valor válido."""
        skills_validos = [0, 1, 2, 3, 4, 5]

        for skill in skills_validos:
            assert not validar_skill_valor(
                skill), f"Skill {skill} deveria ser válido"

    def test_validar_skill_valor_invalido(self):
        """Testa validação de skill com valor inválido."""
        skills_invalidos = [-1, 6, 10, '5', None]

        for skill in skills_invalidos:
            assert validar_skill_valor(
                skill), f"Skill {skill} deveria ser inválido"

    def test_validar_nome_formato_valido(self):
        """Testa validação de nome com formato válido."""
        nomes_validos = [
            'João Silva',
            'Maria Santos',
            'José da Silva',
            'Ana Maria dos Santos',
            'Pedro'
        ]

        for nome in nomes_validos:
            assert not validar_nome_formato(
                nome), f"Nome {nome} deveria ser válido"

    def test_validar_nome_formato_invalido(self):
        """Testa validação de nome com formato inválido."""
        nomes_invalidos = [
            '',
            'João123',
            'João@Silva',
            'João Silva!',
            '   ',
            'Jo'
        ]

        for nome in nomes_invalidos:
            assert validar_nome_formato(
                nome), f"Nome {nome} deveria ser inválido"

    def test_validar_cargo_formato_valido(self):
        """Testa validação de cargo com formato válido."""
        cargos_validos = [
            'Gerente',
            'Analista de RH',
            'Diretor de Tecnologia',
            'Coordenador',
            'Supervisor'
        ]

        for cargo in cargos_validos:
            assert not validar_cargo_formato(
                cargo), f"Cargo {cargo} deveria ser válido"

    def test_validar_cargo_formato_invalido(self):
        """Testa validação de cargo com formato inválido."""
        cargos_invalidos = [
            '',
            'Gerente123',
            'Gerente@RH',
            'Ge',
            '   '
        ]

        for cargo in cargos_invalidos:
            assert validar_cargo_formato(
                cargo), f"Cargo {cargo} deveria ser inválido"

    def test_validar_senha_formato_valido(self):
        """Testa validação de senha com formato válido."""
        senhas_validas = [
            'senha123456',
            'MinhaSenh@123',
            'password123',
            '1234567890'
        ]

        for senha in senhas_validas:
            assert not validar_senha_formato(
                senha), f"Senha deveria ser válida"

    def test_validar_senha_formato_invalido(self):
        """Testa validação de senha com formato inválido."""
        senhas_invalidas = [
            '',
            '123',
            'senha',
            '1234567',  # Muito curta
            '   '
        ]

        for senha in senhas_invalidas:
            assert validar_senha_formato(senha), f"Senha deveria ser inválida"

    def test_validar_nota_mec_formato_valido(self):
        """Testa validação de nota MEC com formato válido."""
        notas_validas = [1.0, 2.5, 3.0, 4.5, 5.0]

        for nota in notas_validas:
            assert not validar_nota_mec_formato(
                nota), f"Nota {nota} deveria ser válida"

    def test_validar_nota_mec_formato_invalido(self):
        """Testa validação de nota MEC com formato inválido."""
        notas_invalidas = [0.0, 6.0, -1.0, '5.0', None]

        for nota in notas_invalidas:
            assert validar_nota_mec_formato(
                nota), f"Nota {nota} deveria ser inválida"

    def test_validar_modalidade_formato_valido(self):
        """Testa validação de modalidade com formato válido."""
        modalidades_validas = ['Presencial', 'EAD', 'Híbrido']

        for modalidade in modalidades_validas:
            assert not validar_modalidade_formato(
                modalidade), f"Modalidade {modalidade} deveria ser válida"

    def test_validar_modalidade_formato_invalido(self):
        """Testa validação de modalidade com formato inválido."""
        modalidades_invalidas = ['', 'Online', 'Presencial123', '   ']

        for modalidade in modalidades_invalidas:
            assert validar_modalidade_formato(
                modalidade), f"Modalidade {modalidade} deveria ser inválida"

