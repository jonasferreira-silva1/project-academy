#!/usr/bin/env python3
"""
Script simples para testar as validações do sistema.
"""

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
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_validar_email_formato():
    """Testa validação de email."""
    print("🧪 Testando validação de email...")

    # Emails válidos
    emails_validos = [
        'usuario@email.com',
        'teste@dominio.org',
        'user.name@example.co.uk'
    ]

    for email in emails_validos:
        resultado = validar_email_formato(email)
        assert not resultado, f"Email {email} deveria ser válido"
        print(f"  ✅ {email} - Válido")

    # Emails inválidos
    emails_invalidos = [
        'email_sem_arroba.com',
        'email@sem_ponto',
        '@dominio.com'
    ]

    for email in emails_invalidos:
        resultado = validar_email_formato(email)
        assert resultado, f"Email {email} deveria ser inválido"
        print(f"  ✅ {email} - Inválido (correto)")

    print("  ✅ Teste de email passou!")


def test_validar_periodo_formato():
    """Testa validação de período."""
    print("🧪 Testando validação de período...")

    # Períodos válidos
    periodos_validos = ['1º', '2º', '3º', '4º', '5º']

    for periodo in periodos_validos:
        resultado = validar_periodo_formato(periodo)
        assert not resultado, f"Período {periodo} deveria ser válido"
        print(f"  ✅ {periodo} - Válido")

    # Períodos inválidos
    periodos_invalidos = ['0º', '11º', '1', 'primeiro']

    for periodo in periodos_invalidos:
        resultado = validar_periodo_formato(periodo)
        assert resultado, f"Período {periodo} deveria ser inválido"
        print(f"  ✅ {periodo} - Inválido (correto)")

    print("  ✅ Teste de período passou!")


def test_validar_contato_formato():
    """Testa validação de contato."""
    print("🧪 Testando validação de contato...")

    # Contatos válidos
    contatos_validos = [
        '11999999999',
        '11987654321',
        '(11)99999-9999'
    ]

    for contato in contatos_validos:
        resultado = validar_contato_formato(contato)
        assert not resultado, f"Contato {contato} deveria ser válido"
        print(f"  ✅ {contato} - Válido")

    # Contatos inválidos
    contatos_invalidos = [
        '123',
        'abc12345678',
        '1199999999'  # Muito curto
    ]

    for contato in contatos_invalidos:
        resultado = validar_contato_formato(contato)
        assert resultado, f"Contato {contato} deveria ser inválido"
        print(f"  ✅ {contato} - Inválido (correto)")

    print("  ✅ Teste de contato passou!")


def test_validar_skill_valor():
    """Testa validação de skill."""
    print("🧪 Testando validação de skill...")

    # Skills válidos
    skills_validos = [0, 1, 2, 3, 4, 5]

    for skill in skills_validos:
        resultado = validar_skill_valor(skill)
        assert not resultado, f"Skill {skill} deveria ser válido"
        print(f"  ✅ {skill} - Válido")

    # Skills inválidos
    skills_invalidos = [-1, 6, 10]

    for skill in skills_invalidos:
        resultado = validar_skill_valor(skill)
        assert resultado, f"Skill {skill} deveria ser inválido"
        print(f"  ✅ {skill} - Inválido (correto)")

    print("  ✅ Teste de skill passou!")


def test_validar_nome_formato():
    """Testa validação de nome."""
    print("🧪 Testando validação de nome...")

    # Nomes válidos
    nomes_validos = [
        'João Silva',
        'Maria Santos',
        'José da Silva'
    ]

    for nome in nomes_validos:
        resultado = validar_nome_formato(nome)
        assert not resultado, f"Nome {nome} deveria ser válido"
        print(f"  ✅ {nome} - Válido")

    # Nomes inválidos
    nomes_invalidos = [
        '',
        'João123',
        'João@Silva'
    ]

    for nome in nomes_invalidos:
        resultado = validar_nome_formato(nome)
        assert resultado, f"Nome {nome} deveria ser inválido"
        print(f"  ✅ {nome} - Inválido (correto)")

    print("  ✅ Teste de nome passou!")


def test_validar_cargo_formato():
    """Testa validação de cargo."""
    print("🧪 Testando validação de cargo...")

    # Cargos válidos
    cargos_validos = [
        'Gerente',
        'Analista de RH',
        'Diretor de Tecnologia'
    ]

    for cargo in cargos_validos:
        resultado = validar_cargo_formato(cargo)
        assert not resultado, f"Cargo {cargo} deveria ser válido"
        print(f"  ✅ {cargo} - Válido")

    # Cargos inválidos
    cargos_invalidos = [
        '',
        'Gerente123',
        'Ge'
    ]

    for cargo in cargos_invalidos:
        resultado = validar_cargo_formato(cargo)
        assert resultado, f"Cargo {cargo} deveria ser inválido"
        print(f"  ✅ {cargo} - Inválido (correto)")

    print("  ✅ Teste de cargo passou!")


def test_validar_senha_formato():
    """Testa validação de senha."""
    print("🧪 Testando validação de senha...")

    # Senhas válidas
    senhas_validas = [
        'senha123456',
        'MinhaSenh@123',
        'password123'
    ]

    for senha in senhas_validas:
        resultado = validar_senha_formato(senha)
        assert not resultado, f"Senha deveria ser válida"
        print(f"  ✅ Senha válida")

    # Senhas inválidas
    senhas_invalidas = [
        '',
        '123',
        'senha'
    ]

    for senha in senhas_invalidas:
        resultado = validar_senha_formato(senha)
        assert resultado, f"Senha deveria ser inválida"
        print(f"  ✅ Senha inválida (correto)")

    print("  ✅ Teste de senha passou!")


def test_validar_nota_mec_formato():
    """Testa validação de nota MEC."""
    print("🧪 Testando validação de nota MEC...")

    # Notas válidas
    notas_validas = [1.0, 2.5, 3.0, 4.5, 5.0]

    for nota in notas_validas:
        resultado = validar_nota_mec_formato(nota)
        assert not resultado, f"Nota {nota} deveria ser válida"
        print(f"  ✅ {nota} - Válida")

    # Notas inválidas
    notas_invalidas = [0.0, 6.0, -1.0]

    for nota in notas_invalidas:
        resultado = validar_nota_mec_formato(nota)
        assert resultado, f"Nota {nota} deveria ser inválida"
        print(f"  ✅ {nota} - Inválida (correto)")

    print("  ✅ Teste de nota MEC passou!")


def test_validar_modalidade_formato():
    """Testa validação de modalidade."""
    print("🧪 Testando validação de modalidade...")

    # Modalidades válidas
    modalidades_validas = ['Presencial', 'EAD', 'Híbrido']

    for modalidade in modalidades_validas:
        resultado = validar_modalidade_formato(modalidade)
        assert not resultado, f"Modalidade {modalidade} deveria ser válida"
        print(f"  ✅ {modalidade} - Válida")

    # Modalidades inválidas
    modalidades_invalidas = ['', 'Online', 'Presencial123']

    for modalidade in modalidades_invalidas:
        resultado = validar_modalidade_formato(modalidade)
        assert resultado, f"Modalidade {modalidade} deveria ser inválida"
        print(f"  ✅ {modalidade} - Inválida (correto)")

    print("  ✅ Teste de modalidade passou!")


def main():
    """Função principal."""
    print("🚀 Iniciando testes simples do DashTalent...")
    print("=" * 50)

    try:
        test_validar_email_formato()
        test_validar_periodo_formato()
        test_validar_contato_formato()
        test_validar_skill_valor()
        test_validar_nome_formato()
        test_validar_cargo_formato()
        test_validar_senha_formato()
        test_validar_nota_mec_formato()
        test_validar_modalidade_formato()

        print("\n🎉 Todos os testes passaram com sucesso!")
        print("✅ Sistema de validação está funcionando corretamente!")

    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

