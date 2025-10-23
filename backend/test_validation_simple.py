#!/usr/bin/env python3
"""
Teste simples para validações do sistema DashTalent.
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_validation_imports():
    """Testa se as validações podem ser importadas."""
    print("🧪 Testando imports das validações...")

    try:
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
        print("  ✅ Imports das validações funcionaram!")
        return True
    except ImportError as e:
        print(f"  ❌ Erro ao importar validações: {e}")
        return False


def test_email_validation():
    """Testa validação de email."""
    print("🧪 Testando validação de email...")

    try:
        from services.validation_service import validar_email_formato

        # Teste com email válido
        resultado = validar_email_formato('usuario@email.com')
        assert not resultado, "Email válido deveria retornar False"
        print("  ✅ Email válido funcionou")

        # Teste com email inválido
        resultado = validar_email_formato('email_sem_arroba.com')
        assert resultado, "Email inválido deveria retornar True"
        print("  ✅ Email inválido funcionou")

        print("  ✅ Teste de email passou!")
        return True

    except Exception as e:
        print(f"  ❌ Erro no teste de email: {e}")
        return False


def test_periodo_validation():
    """Testa validação de período."""
    print("🧪 Testando validação de período...")

    try:
        from services.validation_service import validar_periodo_formato

        # Teste com período válido
        resultado = validar_periodo_formato('1º')
        assert not resultado, "Período válido deveria retornar False"
        print("  ✅ Período válido funcionou")

        # Teste com período inválido
        resultado = validar_periodo_formato('0º')
        assert resultado, "Período inválido deveria retornar True"
        print("  ✅ Período inválido funcionou")

        print("  ✅ Teste de período passou!")
        return True

    except Exception as e:
        print(f"  ❌ Erro no teste de período: {e}")
        return False


def test_contato_validation():
    """Testa validação de contato."""
    print("🧪 Testando validação de contato...")

    try:
        from services.validation_service import validar_contato_formato

        # Teste com contato válido
        resultado = validar_contato_formato('11999999999')
        assert not resultado, "Contato válido deveria retornar False"
        print("  ✅ Contato válido funcionou")

        # Teste com contato inválido
        resultado = validar_contato_formato('123')
        assert resultado, "Contato inválido deveria retornar True"
        print("  ✅ Contato inválido funcionou")

        print("  ✅ Teste de contato passou!")
        return True

    except Exception as e:
        print(f"  ❌ Erro no teste de contato: {e}")
        return False


def test_skill_validation():
    """Testa validação de skill."""
    print("🧪 Testando validação de skill...")

    try:
        from services.validation_service import validar_skill_valor

        # Teste com skill válido
        resultado = validar_skill_valor(3)
        assert not resultado, "Skill válido deveria retornar False"
        print("  ✅ Skill válido funcionou")

        # Teste com skill inválido
        resultado = validar_skill_valor(6)
        assert resultado, "Skill inválido deveria retornar True"
        print("  ✅ Skill inválido funcionou")

        print("  ✅ Teste de skill passou!")
        return True

    except Exception as e:
        print(f"  ❌ Erro no teste de skill: {e}")
        return False


def test_nome_validation():
    """Testa validação de nome."""
    print("🧪 Testando validação de nome...")

    try:
        from services.validation_service import validar_nome_formato

        # Teste com nome válido
        resultado = validar_nome_formato('João Silva')
        assert not resultado, "Nome válido deveria retornar False"
        print("  ✅ Nome válido funcionou")

        # Teste com nome inválido
        resultado = validar_nome_formato('')
        assert resultado, "Nome inválido deveria retornar True"
        print("  ✅ Nome inválido funcionou")

        print("  ✅ Teste de nome passou!")
        return True

    except Exception as e:
        print(f"  ❌ Erro no teste de nome: {e}")
        return False


def test_cargo_validation():
    """Testa validação de cargo."""
    print("🧪 Testando validação de cargo...")

    try:
        from services.validation_service import validar_cargo_formato

        # Teste com cargo válido
        resultado = validar_cargo_formato('Gerente')
        assert not resultado, "Cargo válido deveria retornar False"
        print("  ✅ Cargo válido funcionou")

        # Teste com cargo inválido
        resultado = validar_cargo_formato('')
        assert resultado, "Cargo inválido deveria retornar True"
        print("  ✅ Cargo inválido funcionou")

        print("  ✅ Teste de cargo passou!")
        return True

    except Exception as e:
        print(f"  ❌ Erro no teste de cargo: {e}")
        return False


def test_senha_validation():
    """Testa validação de senha."""
    print("🧪 Testando validação de senha...")

    try:
        from services.validation_service import validar_senha_formato

        # Teste com senha válida
        resultado = validar_senha_formato('senha123456')
        assert not resultado, "Senha válida deveria retornar False"
        print("  ✅ Senha válida funcionou")

        # Teste com senha inválida
        resultado = validar_senha_formato('123')
        assert resultado, "Senha inválida deveria retornar True"
        print("  ✅ Senha inválida funcionou")

        print("  ✅ Teste de senha passou!")
        return True

    except Exception as e:
        print(f"  ❌ Erro no teste de senha: {e}")
        return False


def test_nota_mec_validation():
    """Testa validação de nota MEC."""
    print("🧪 Testando validação de nota MEC...")

    try:
        from services.validation_service import validar_nota_mec_formato

        # Teste com nota válida
        resultado = validar_nota_mec_formato(4.5)
        assert not resultado, "Nota válida deveria retornar False"
        print("  ✅ Nota válida funcionou")

        # Teste com nota inválida
        resultado = validar_nota_mec_formato(6.0)
        assert resultado, "Nota inválida deveria retornar True"
        print("  ✅ Nota inválida funcionou")

        print("  ✅ Teste de nota MEC passou!")
        return True

    except Exception as e:
        print(f"  ❌ Erro no teste de nota MEC: {e}")
        return False


def test_modalidade_validation():
    """Testa validação de modalidade."""
    print("🧪 Testando validação de modalidade...")

    try:
        from services.validation_service import validar_modalidade_formato

        # Teste com modalidade válida
        resultado = validar_modalidade_formato('Presencial')
        assert not resultado, "Modalidade válida deveria retornar False"
        print("  ✅ Modalidade válida funcionou")

        # Teste com modalidade inválida
        resultado = validar_modalidade_formato('')
        assert resultado, "Modalidade inválida deveria retornar True"
        print("  ✅ Modalidade inválida funcionou")

        print("  ✅ Teste de modalidade passou!")
        return True

    except Exception as e:
        print(f"  ❌ Erro no teste de modalidade: {e}")
        return False


def main():
    """Função principal."""
    print("🚀 Iniciando testes de validação do DashTalent...")
    print("=" * 60)

    testes = [
        test_validation_imports,
        test_email_validation,
        test_periodo_validation,
        test_contato_validation,
        test_skill_validation,
        test_nome_validation,
        test_cargo_validation,
        test_senha_validation,
        test_nota_mec_validation,
        test_modalidade_validation
    ]

    sucessos = 0
    total = len(testes)

    for teste in testes:
        try:
            if teste():
                sucessos += 1
        except Exception as e:
            print(f"❌ Erro inesperado no teste: {e}")

    print("\n" + "=" * 60)
    print(f"📊 Resultado: {sucessos}/{total} testes passaram")

    if sucessos == total:
        print("🎉 Todos os testes passaram com sucesso!")
        print("✅ Sistema de validação está funcionando corretamente!")
        return True
    else:
        print(f"⚠️ {total - sucessos} testes falharam")
        return False


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
