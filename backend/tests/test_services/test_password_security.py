"""
Testes para validação de segurança de senha (Fase 1).
Valida política de senha: 10 caracteres, maiúscula, minúscula, número, especial.
"""

import pytest
from services.password_validation_service import (
    validar_senha_minima,
    validar_senha_forte
)
from services.rate_limit_service import (
    verificar_rate_limit,
    resetar_rate_limit,
    MAX_LOGIN_ATTEMPTS,
    BLOCK_DURATION
)


class TestPasswordMinima:
    """Testes para validação de tamanho mínimo de senha (10 caracteres)."""

    def test_senha_menor_que_10_caracteres_invalida(self):
        """Testa que senhas com menos de 10 caracteres são inválidas."""
        senhas_invalidas = [
            '',           # Vazia
            '1234567',    # 7 caracteres
            '12345678',   # 8 caracteres
            '123456789',  # 9 caracteres
        ]
        
        for senha in senhas_invalidas:
            assert validar_senha_minima(senha), \
                f"Senha '{senha}' deveria ser inválida (tem {len(senha)} caracteres)"

    def test_senha_com_10_caracteres_valida(self):
        """Testa que senhas com exatamente 10 caracteres são válidas."""
        senha = '1234567890'
        assert not validar_senha_minima(senha), \
            f"Senha '{senha}' deveria ser válida (tem 10 caracteres)"

    def test_senha_com_mais_de_10_caracteres_valida(self):
        """Testa que senhas com mais de 10 caracteres são válidas."""
        senhas_validas = [
            '12345678901',      # 11 caracteres
            'MinhaSenha123!',   # 14 caracteres
            'A' * 20,           # 20 caracteres
        ]
        
        for senha in senhas_validas:
            assert not validar_senha_minima(senha), \
                f"Senha '{senha}' deveria ser válida (tem {len(senha)} caracteres)"


class TestPasswordForte:
    """Testes para validação de senha forte completa."""

    def test_senha_forte_completa_valida(self):
        """Testa que senhas que atendem todos os critérios são válidas."""
        senhas_validas = [
            'MinhaSenha123!',      # 14 chars: maiúscula, minúscula, número, especial
            'Senha@2024#',         # 11 chars
            'Test123!ABC',         # 10 chars (mínimo)
            'P@ssw0rd!',          # 9 chars (invalida por tamanho)
            'MyP@ss1234',         # 10 chars
        ]
        
        for senha in senhas_validas:
            # Filtrar senhas com menos de 10 caracteres
            if len(senha) >= 10:
                valida, mensagem = validar_senha_forte(senha)
                assert valida, \
                    f"Senha '{senha}' deveria ser válida. Erro: {mensagem}"

    def test_senha_sem_maiuscula_invalida(self):
        """Testa que senhas sem letra maiúscula são inválidas."""
        senhas_invalidas = [
            'minhasenha123!',     # Sem maiúscula
            'senha1234!@#',       # Sem maiúscula
            'abcdefg123!',        # Sem maiúscula
        ]
        
        for senha in senhas_invalidas:
            if len(senha) >= 10:
                valida, mensagem = validar_senha_forte(senha)
                assert not valida, \
                    f"Senha '{senha}' deveria ser inválida (sem maiúscula)"
                assert 'maiúscula' in mensagem.lower(), \
                    f"Mensagem de erro deveria mencionar maiúscula: {mensagem}"

    def test_senha_sem_minuscula_invalida(self):
        """Testa que senhas sem letra minúscula são inválidas."""
        senhas_invalidas = [
            'MINHASENHA123!',     # Sem minúscula
            'SENHA1234!@#',       # Sem minúscula
            'ABCDEFG123!',        # Sem minúscula
        ]
        
        for senha in senhas_invalidas:
            if len(senha) >= 10:
                valida, mensagem = validar_senha_forte(senha)
                assert not valida, \
                    f"Senha '{senha}' deveria ser inválida (sem minúscula)"
                assert 'minúscula' in mensagem.lower(), \
                    f"Mensagem de erro deveria mencionar minúscula: {mensagem}"

    def test_senha_sem_numero_invalida(self):
        """Testa que senhas sem número são inválidas."""
        senhas_invalidas = [
            'MinhaSenha!',        # Sem número
            'Senha@Segura#',      # Sem número
            'MinhaSenhaTeste!',   # Sem número
        ]
        
        for senha in senhas_invalidas:
            if len(senha) >= 10:
                valida, mensagem = validar_senha_forte(senha)
                assert not valida, \
                    f"Senha '{senha}' deveria ser inválida (sem número)"
                assert 'número' in mensagem.lower() or 'numero' in mensagem.lower(), \
                    f"Mensagem de erro deveria mencionar número: {mensagem}"

    def test_senha_sem_caractere_especial_invalida(self):
        """Testa que senhas sem caractere especial são inválidas."""
        senhas_invalidas = [
            'MinhaSenha123',      # Sem especial
            'SenhaSegura2024',    # Sem especial
            'MinhaSenhaTeste123', # Sem especial
        ]
        
        for senha in senhas_invalidas:
            if len(senha) >= 10:
                valida, mensagem = validar_senha_forte(senha)
                assert not valida, \
                    f"Senha '{senha}' deveria ser inválida (sem caractere especial)"
                assert 'especial' in mensagem.lower(), \
                    f"Mensagem de erro deveria mencionar caractere especial: {mensagem}"

    def test_senha_menor_que_10_caracteres_invalida(self):
        """Testa que senhas com menos de 10 caracteres são inválidas, mesmo com outros critérios."""
        senhas_invalidas = [
            'Senha123!',          # 9 caracteres (tem todos os critérios, mas é curta)
            'Pass123!',           # 8 caracteres
            'Senha1!',            # 7 caracteres
        ]
        
        for senha in senhas_invalidas:
            valida, mensagem = validar_senha_forte(senha)
            assert not valida, \
                f"Senha '{senha}' deveria ser inválida (menos de 10 caracteres)"
            assert '10' in mensagem or 'dez' in mensagem.lower(), \
                f"Mensagem de erro deveria mencionar 10 caracteres: {mensagem}"

    def test_senha_vazia_invalida(self):
        """Testa que senha vazia é inválida."""
        valida, mensagem = validar_senha_forte('')
        assert not valida, "Senha vazia deveria ser inválida"
        assert mensagem is not None, "Deveria retornar mensagem de erro"


class TestRateLimiting:
    """Testes para rate limiting (5 tentativas, 10 minutos)."""

    def test_max_attempts_configurado_para_5(self):
        """Testa que MAX_LOGIN_ATTEMPTS está configurado para 5."""
        assert MAX_LOGIN_ATTEMPTS == 5, \
            f"MAX_LOGIN_ATTEMPTS deveria ser 5, mas é {MAX_LOGIN_ATTEMPTS}"

    def test_block_duration_configurado_para_10_minutos(self):
        """Testa que BLOCK_DURATION está configurado para 600 segundos (10 minutos)."""
        assert BLOCK_DURATION == 600, \
            f"BLOCK_DURATION deveria ser 600 segundos (10 minutos), mas é {BLOCK_DURATION}"

    def test_permite_ate_5_tentativas(self):
        """Testa que permite até 5 tentativas antes de bloquear."""
        email_teste = 'teste@exemplo.com'
        
        # Resetar contador
        resetar_rate_limit(email_teste)
        
        # Fazer 5 tentativas (todas devem ser permitidas)
        for i in range(5):
            permitido, mensagem, tentativas_restantes = verificar_rate_limit(email_teste)
            assert permitido, \
                f"Tentativa {i+1} deveria ser permitida. Mensagem: {mensagem}"
            assert tentativas_restantes == (5 - (i + 1)), \
                f"Tentativas restantes deveriam ser {5 - (i + 1)}, mas são {tentativas_restantes}"
        
        # A 6ª tentativa deve bloquear
        permitido, mensagem, _ = verificar_rate_limit(email_teste)
        assert not permitido, \
            f"6ª tentativa deveria bloquear. Mensagem: {mensagem}"
        assert 'bloqueado' in mensagem.lower() or 'minutos' in mensagem.lower(), \
            f"Mensagem de bloqueio deveria mencionar bloqueio ou minutos: {mensagem}"

    def test_reseta_rate_limit_apos_sucesso(self):
        """Testa que o rate limit é resetado após login bem-sucedido."""
        email_teste = 'teste_reset@exemplo.com'
        
        # Fazer algumas tentativas
        for i in range(3):
            verificar_rate_limit(email_teste)
        
        # Resetar (simulando login bem-sucedido)
        resetar_rate_limit(email_teste)
        
        # Tentativa após reset deve ter contador zerado
        permitido, mensagem, tentativas_restantes = verificar_rate_limit(email_teste)
        assert permitido, "Tentativa após reset deveria ser permitida"
        assert tentativas_restantes == 4, \
            f"Após reset, deveria ter 4 tentativas restantes, mas tem {tentativas_restantes}"


# Funções auxiliares para testes manuais
def executar_todos_testes():
    """Executa todos os testes e imprime resultados."""
    import sys
    
    resultados = {
        'passou': 0,
        'falhou': 0,
        'erros': []
    }
    
    # Testes de senha mínima
    print("\n=== TESTANDO VALIDAÇÃO DE TAMANHO MÍNIMO ===")
    teste_minima = TestPasswordMinima()
    
    try:
        teste_minima.test_senha_menor_que_10_caracteres_invalida()
        print("✅ Teste: senha < 10 caracteres inválida - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"❌ Teste: senha < 10 caracteres inválida - FALHOU: {e}")
        resultados['falhou'] += 1
        resultados['erros'].append(str(e))
    
    try:
        teste_minima.test_senha_com_10_caracteres_valida()
        print("✅ Teste: senha com 10 caracteres válida - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"❌ Teste: senha com 10 caracteres válida - FALHOU: {e}")
        resultados['falhou'] += 1
        resultados['erros'].append(str(e))
    
    # Testes de senha forte
    print("\n=== TESTANDO VALIDAÇÃO DE SENHA FORTE ===")
    teste_forte = TestPasswordForte()
    
    testes_forte = [
        ('senha forte completa válida', teste_forte.test_senha_forte_completa_valida),
        ('senha sem maiúscula inválida', teste_forte.test_senha_sem_maiuscula_invalida),
        ('senha sem minúscula inválida', teste_forte.test_senha_sem_minuscula_invalida),
        ('senha sem número inválida', teste_forte.test_senha_sem_numero_invalida),
        ('senha sem caractere especial inválida', teste_forte.test_senha_sem_caractere_especial_invalida),
        ('senha < 10 caracteres inválida', teste_forte.test_senha_menor_que_10_caracteres_invalida),
        ('senha vazia inválida', teste_forte.test_senha_vazia_invalida),
    ]
    
    for nome, teste in testes_forte:
        try:
            teste()
            print(f"✅ Teste: {nome} - PASSOU")
            resultados['passou'] += 1
        except AssertionError as e:
            print(f"❌ Teste: {nome} - FALHOU: {e}")
            resultados['falhou'] += 1
            resultados['erros'].append(str(e))
    
    # Testes de rate limiting
    print("\n=== TESTANDO RATE LIMITING ===")
    teste_rate = TestRateLimiting()
    
    try:
        teste_rate.test_max_attempts_configurado_para_5()
        print("✅ Teste: MAX_LOGIN_ATTEMPTS = 5 - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"❌ Teste: MAX_LOGIN_ATTEMPTS = 5 - FALHOU: {e}")
        resultados['falhou'] += 1
        resultados['erros'].append(str(e))
    
    try:
        teste_rate.test_block_duration_configurado_para_10_minutos()
        print("✅ Teste: BLOCK_DURATION = 600 segundos - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"❌ Teste: BLOCK_DURATION = 600 segundos - FALHOU: {e}")
        resultados['falhou'] += 1
        resultados['erros'].append(str(e))
    
    try:
        teste_rate.test_permite_ate_5_tentativas()
        print("✅ Teste: permite até 5 tentativas - PASSOU")
        resultados['passou'] += 1
    except AssertionError as e:
        print(f"❌ Teste: permite até 5 tentativas - FALHOU: {e}")
        resultados['falhou'] += 1
        resultados['erros'].append(str(e))
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    print(f"✅ Testes que passaram: {resultados['passou']}")
    print(f"❌ Testes que falharam: {resultados['falhou']}")
    print(f"📊 Total: {resultados['passou'] + resultados['falhou']} testes")
    
    if resultados['erros']:
        print("\n⚠️ ERROS ENCONTRADOS:")
        for erro in resultados['erros']:
            print(f"  - {erro}")
    
    print("="*60)
    
    return resultados


if __name__ == '__main__':
    executar_todos_testes()

