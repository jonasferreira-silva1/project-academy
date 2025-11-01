#!/usr/bin/env python3
"""
Script para executar testes da Fase 1 de segurança.
Facilita execução rápida dos testes de validação de senha e rate limiting.
"""

import sys
import os

# Adicionar diretório atual ao path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("="*60)
    print("🧪 EXECUTANDO TESTES DA FASE 1 - SEGURANÇA")
    print("="*60)
    print()
    
    try:
        # Tentar importar e executar testes
        from tests.test_services.test_password_security import executar_todos_testes
        
        print("📦 Carregando módulos de teste...")
        print()
        
        # Executar testes
        resultados = executar_todos_testes()
        
        print()
        print("="*60)
        
        # Resultado final
        total = resultados['passou'] + resultados['falhou']
        porcentagem = (resultados['passou'] / total * 100) if total > 0 else 0
        
        if resultados['falhou'] == 0:
            print("✅ TODOS OS TESTES PASSARAM!")
            print(f"📊 {resultados['passou']}/{total} testes passaram ({porcentagem:.1f}%)")
            print()
            print("🎉 Fase 1 implementada com sucesso!")
            return 0
        else:
            print("⚠️ ALGUNS TESTES FALHARAM")
            print(f"✅ Passaram: {resultados['passou']}/{total}")
            print(f"❌ Falharam: {resultados['falhou']}/{total}")
            print(f"📊 {porcentagem:.1f}% de sucesso")
            print()
            print("⚠️ Revise os erros acima e corrija os problemas.")
            return 1
            
    except ImportError as e:
        print(f"❌ ERRO: Não foi possível importar módulos de teste")
        print(f"   Detalhes: {e}")
        print()
        print("💡 Dicas:")
        print("   1. Certifique-se de estar no diretório 'backend'")
        print("   2. Verifique se todos os arquivos foram salvos")
        print("   3. Tente executar: pytest tests/test_services/test_password_security.py -v")
        return 1
    except Exception as e:
        print(f"❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

