"""
Testes simplificados da Fase 1 - Sem dependência de banco de dados.
Executa testes unitários de validação de senha e rate limiting.
"""

import sys
import os

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def testar_validacao_senha():
    """Testa validação de senha."""
    print("\n" + "="*60)
    print("TESTANDO VALIDACAO DE SENHA")
    print("="*60)
    
    from services.password_validation_service import validar_senha_minima, validar_senha_forte
    
    resultados = {'passou': 0, 'falhou': 0}
    
    # Teste 1: Senha menor que 10 caracteres
    try:
        assert validar_senha_minima('Senha123!'), "Senha com 9 caracteres deveria ser inválida"
        print("✓ Teste 1: Senha < 10 caracteres inválida - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"✗ Teste 1: Senha < 10 caracteres inválida - FALHOU: {e}")
        resultados['falhou'] += 1
    
    # Teste 2: Senha com 10 caracteres válida
    try:
        assert not validar_senha_minima('MinhaSenha'), "Senha com 10 caracteres deveria ser válida"
        print("✓ Teste 2: Senha com 10 caracteres válida - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"✗ Teste 2: Senha com 10 caracteres válida - FALHOU: {e}")
        resultados['falhou'] += 1
    
    # Teste 3: Senha forte completa
    try:
        valida, msg = validar_senha_forte('MinhaSenha123!')
        assert valida, f"Senha forte deveria ser válida. Erro: {msg}"
        print("✓ Teste 3: Senha forte completa válida - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"✗ Teste 3: Senha forte completa válida - FALHOU: {e}")
        resultados['falhou'] += 1
    
    # Teste 4: Senha sem maiúscula
    try:
        valida, msg = validar_senha_forte('minhasenha123!')
        assert not valida, "Senha sem maiúscula deveria ser inválida"
        assert 'maiúscula' in msg.lower(), f"Mensagem deveria mencionar maiúscula: {msg}"
        print("✓ Teste 4: Senha sem maiúscula inválida - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"✗ Teste 4: Senha sem maiúscula inválida - FALHOU: {e}")
        resultados['falhou'] += 1
    
    # Teste 5: Senha sem minúscula
    try:
        valida, msg = validar_senha_forte('MINHASENHA123!')
        assert not valida, "Senha sem minúscula deveria ser inválida"
        assert 'minúscula' in msg.lower(), f"Mensagem deveria mencionar minúscula: {msg}"
        print("✓ Teste 5: Senha sem minúscula inválida - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"✗ Teste 5: Senha sem minúscula inválida - FALHOU: {e}")
        resultados['falhou'] += 1
    
    # Teste 6: Senha sem número
    try:
        valida, msg = validar_senha_forte('MinhaSenha!')
        assert not valida, "Senha sem número deveria ser inválida"
        assert 'número' in msg.lower() or 'numero' in msg.lower(), f"Mensagem deveria mencionar número: {msg}"
        print("✓ Teste 6: Senha sem número inválida - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"✗ Teste 6: Senha sem número inválida - FALHOU: {e}")
        resultados['falhou'] += 1
    
    # Teste 7: Senha sem caractere especial
    try:
        valida, msg = validar_senha_forte('MinhaSenha123')
        assert not valida, "Senha sem caractere especial deveria ser inválida"
        assert 'especial' in msg.lower(), f"Mensagem deveria mencionar caractere especial: {msg}"
        print("✓ Teste 7: Senha sem caractere especial inválida - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"✗ Teste 7: Senha sem caractere especial inválida - FALHOU: {e}")
        resultados['falhou'] += 1
    
    # Teste 8: Senha vazia
    try:
        valida, msg = validar_senha_forte('')
        assert not valida, "Senha vazia deveria ser inválida"
        assert msg is not None, "Deveria retornar mensagem de erro"
        print("✓ Teste 8: Senha vazia inválida - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"✗ Teste 8: Senha vazia inválida - FALHOU: {e}")
        resultados['falhou'] += 1
    
    return resultados


def testar_rate_limiting():
    """Testa rate limiting."""
    print("\n" + "="*60)
    print("TESTANDO RATE LIMITING")
    print("="*60)
    
    from services.rate_limit_service import (
        MAX_LOGIN_ATTEMPTS,
        BLOCK_DURATION,
        verificar_rate_limit,
        resetar_rate_limit
    )
    
    resultados = {'passou': 0, 'falhou': 0}
    
    # Teste 1: MAX_LOGIN_ATTEMPTS = 5
    try:
        assert MAX_LOGIN_ATTEMPTS == 5, f"MAX_LOGIN_ATTEMPTS deveria ser 5, mas é {MAX_LOGIN_ATTEMPTS}"
        print(f"✓ Teste 1: MAX_LOGIN_ATTEMPTS = 5 - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"✗ Teste 1: MAX_LOGIN_ATTEMPTS = 5 - FALHOU: {e}")
        resultados['falhou'] += 1
    
    # Teste 2: BLOCK_DURATION = 600 (10 minutos)
    try:
        assert BLOCK_DURATION == 600, f"BLOCK_DURATION deveria ser 600 segundos, mas é {BLOCK_DURATION}"
        print(f"✓ Teste 2: BLOCK_DURATION = 600 segundos - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"✗ Teste 2: BLOCK_DURATION = 600 segundos - FALHOU: {e}")
        resultados['falhou'] += 1
    
    # Teste 3: Permite até 5 tentativas
    try:
        email_teste = 'teste_rate@exemplo.com'
        resetar_rate_limit(email_teste)
        
        bloqueou_antes = False
        for i in range(5):
            permitido, mensagem, tentativas_restantes = verificar_rate_limit(email_teste)
            if not permitido:
                bloqueou_antes = True
                break
        
        assert not bloqueou_antes, "Não deveria bloquear antes de 5 tentativas"
        print("✓ Teste 3: Permite até 5 tentativas - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"✗ Teste 3: Permite até 5 tentativas - FALHOU: {e}")
        resultados['falhou'] += 1
    
    # Teste 4: Bloqueia na 6ª tentativa
    try:
        email_teste = 'teste_bloqueio@exemplo.com'
        resetar_rate_limit(email_teste)
        
        # Fazer 5 tentativas
        for i in range(5):
            verificar_rate_limit(email_teste)
        
        # 6ª tentativa deve bloquear
        permitido, mensagem, _ = verificar_rate_limit(email_teste)
        assert not permitido, "6ª tentativa deveria bloquear"
        assert 'bloqueado' in mensagem.lower() or 'minutos' in mensagem.lower(), \
            f"Mensagem deveria mencionar bloqueio: {mensagem}"
        print("✓ Teste 4: Bloqueia na 6ª tentativa - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"✗ Teste 4: Bloqueia na 6ª tentativa - FALHOU: {e}")
        resultados['falhou'] += 1
    
    return resultados


def main():
    """Executa todos os testes."""
    print("\n" + "="*60)
    print("EXECUTANDO TESTES DA FASE 1 - SEGURANCA")
    print("="*60)
    
    total_passou = 0
    total_falhou = 0
    
    # Testes de senha
    resultados_senha = testar_validacao_senha()
    total_passou += resultados_senha['passou']
    total_falhou += resultados_senha['falhou']
    
    # Testes de rate limiting
    resultados_rate = testar_rate_limiting()
    total_passou += resultados_rate['passou']
    total_falhou += resultados_rate['falhou']
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    print(f"✓ Testes que passaram: {total_passou}")
    print(f"✗ Testes que falharam: {total_falhou}")
    total = total_passou + total_falhou
    print(f"Total: {total} testes")
    
    if total > 0:
        porcentagem = (total_passou / total * 100)
        print(f"Taxa de sucesso: {porcentagem:.1f}%")
    
    print("="*60)
    
    if total_falhou == 0:
        print("\n✓ TODOS OS TESTES PASSARAM!")
        print("Fase 1 implementada com sucesso!")
        return 0
    else:
        print(f"\n⚠ ATENCAO: {total_falhou} teste(s) falharam")
        print("Revise os erros acima e corrija os problemas.")
        return 1


if __name__ == '__main__':
    sys.exit(main())

