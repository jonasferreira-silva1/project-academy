#!/usr/bin/env python3
"""
Script para executar testes do projeto DashTalent.
"""

import subprocess
import sys
import os


def run_tests():
    """Executa todos os testes do projeto."""
    print("🧪 Executando testes do DashTalent...")
    print("=" * 50)

    # Comando para executar pytest
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",  # Verbose
        "--tb=short",  # Traceback curto
        "--cov=.",  # Coverage
        "--cov-report=html:htmlcov",  # Relatório HTML
        "--cov-report=term-missing",  # Relatório no terminal
        "--cov-fail-under=80"  # Mínimo 80% de coverage
    ]

    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ Todos os testes passaram!")
        print("📊 Relatório de cobertura gerado em: htmlcov/index.html")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Alguns testes falharam! Código de saída: {e.returncode}")
        return False


def run_specific_test(test_path):
    """Executa um teste específico."""
    print(f"🧪 Executando teste específico: {test_path}")
    print("=" * 50)

    cmd = [sys.executable, "-m", "pytest", test_path, "-v"]

    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✅ Teste {test_path} passou!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Teste {test_path} falhou! Código de saída: {e.returncode}")
        return False


def run_tests_with_coverage():
    """Executa testes com relatório de cobertura."""
    print("🧪 Executando testes com cobertura...")
    print("=" * 50)

    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "--cov=.",
        "--cov-report=html:htmlcov",
        "--cov-report=term-missing",
        "--cov-fail-under=70"  # Mínimo 70% de coverage
    ]

    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ Testes executados com sucesso!")
        print("📊 Relatório de cobertura: htmlcov/index.html")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Testes falharam! Código de saída: {e.returncode}")
        return False


def main():
    """Função principal."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--coverage":
            success = run_tests_with_coverage()
        elif sys.argv[1] == "--help":
            print("Uso: python run_tests.py [opção]")
            print("\nOpções:")
            print("  --coverage    Executa testes com relatório de cobertura")
            print("  --help        Mostra esta ajuda")
            print("  <caminho>     Executa teste específico")
            print("\nExemplos:")
            print("  python run_tests.py")
            print("  python run_tests.py --coverage")
            print("  python run_tests.py tests/test_services/test_validation_service.py")
            return
        else:
            # Executar teste específico
            success = run_specific_test(sys.argv[1])
    else:
        # Executar todos os testes
        success = run_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
