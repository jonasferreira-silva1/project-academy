"""
Testes para o serviço de histórico de senhas (Fase 3).
Verifica se o sistema impede reutilização das últimas 3 senhas.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, '/app')


def testar_historico_senhas():
    """Executa testes do sistema de histórico de senhas."""
    # Importar app para criar contexto
    from app import app
    
    print("\n" + "="*70)
    print("TESTE FASE 3: SISTEMA DE HISTÓRICO DE SENHAS")
    print("="*70 + "\n")
    
    resultados = []
    
    # Criar contexto de aplicação Flask
    with app.app_context():
        try:
            from services.password_history_service import (
                verificar_senha_no_historico,
                salvar_senha_no_historico,
                salvar_senha_texto_plano_no_historico,
                obter_historico_completo
            )
            from domain import PasswordHistory, db, Chefe
            from werkzeug.security import generate_password_hash
            
            print("TESTE 1: Verificando importação do serviço...")
            print("   ✅ Serviço importado com sucesso")
            resultados.append(True)
            print()
            
            # Criar um usuário de teste (se não existir)
            print("TESTE 2: Preparando ambiente de teste...")
            email_teste = 'teste_historico@email.com'
            chefe_teste = Chefe.query.filter_by(email=email_teste).first()
            
            if not chefe_teste:
                chefe_teste = Chefe(
                    nome='Teste Historico',
                    email=email_teste,
                    senha=generate_password_hash('SenhaInicial123!'),
                    nome_empresa='Empresa Teste',
                    cargo='CEO'
                )
                db.session.add(chefe_teste)
                db.session.commit()
                print(f"   ✅ Usuário de teste criado (ID: {chefe_teste.id_chefe})")
            else:
                print(f"   ✅ Usuário de teste já existe (ID: {chefe_teste.id_chefe})")
            
            # Limpar histórico anterior do teste
            PasswordHistory.query.filter_by(
                user_type='chefe',
                user_id=chefe_teste.id_chefe
            ).delete()
            db.session.commit()
            
            resultados.append(True)
            print()
            
            # Teste 3: Salvar senhas no histórico
            print("TESTE 3: Salvando senhas no histórico...")
            senha1 = 'SenhaInicial123!'
            senha2 = 'SenhaSegunda456@'
            senha3 = 'SenhaTerceira789#'
            senha4 = 'SenhaQuarta012$'
            
            salvar_senha_texto_plano_no_historico('chefe', chefe_teste.id_chefe, senha1)
            time.sleep(0.5)
            salvar_senha_texto_plano_no_historico('chefe', chefe_teste.id_chefe, senha2)
            time.sleep(0.5)
            salvar_senha_texto_plano_no_historico('chefe', chefe_teste.id_chefe, senha3)
            time.sleep(0.5)
            
            historico = obter_historico_completo('chefe', chefe_teste.id_chefe)
            if len(historico) >= 3:
                print(f"   ✅ {len(historico)} senhas salvas no histórico")
                resultados.append(True)
            else:
                print(f"   ❌ Esperado 3+ senhas, encontrado {len(historico)}")
                resultados.append(False)
            print()
            
            # Teste 4: Verificar que senha antiga está no histórico
            print("TESTE 4: Verificando se senhas antigas estão no histórico...")
            esta1, msg1 = verificar_senha_no_historico('chefe', chefe_teste.id_chefe, senha1)
            esta2, msg2 = verificar_senha_no_historico('chefe', chefe_teste.id_chefe, senha2)
            esta3, msg3 = verificar_senha_no_historico('chefe', chefe_teste.id_chefe, senha3)
            
            if esta1 and esta2 and esta3:
                print("   ✅ Todas as 3 senhas antigas foram detectadas no histórico")
                resultados.append(True)
            else:
                print(f"   ❌ Erro: senha1={esta1}, senha2={esta2}, senha3={esta3}")
                resultados.append(False)
            print()
            
            # Teste 5: Verificar que senha nova NÃO está no histórico
            print("TESTE 5: Verificando que senha nova não está no histórico...")
            esta4, msg4 = verificar_senha_no_historico('chefe', chefe_teste.id_chefe, senha4)
            if not esta4:
                print("   ✅ Senha nova não está no histórico (pode ser usada)")
                resultados.append(True)
            else:
                print(f"   ❌ Senha nova está no histórico (não deveria estar)")
                resultados.append(False)
            print()
            
            # Teste 6: Verificar limpeza automática (manter apenas 3)
            print("TESTE 6: Verificando limpeza automática do histórico...")
            salvar_senha_texto_plano_no_historico('chefe', chefe_teste.id_chefe, senha4)
            time.sleep(0.5)
            
            historico_final = obter_historico_completo('chefe', chefe_teste.id_chefe)
            if len(historico_final) <= 3:
                print(f"   ✅ Histórico mantém apenas {len(historico_final)} senhas (limpeza automática funcionando)")
                resultados.append(True)
            else:
                print(f"   ⚠️  Histórico tem {len(historico_final)} senhas (esperado máximo 3)")
                resultados.append(False)
            print()
            
            # Resumo
            print("="*70)
            print("RESUMO DOS TESTES")
            print("="*70)
            
            nomes = [
                "Importação do serviço",
                "Preparação do ambiente",
                "Salvamento de senhas",
                "Deteccção de senhas antigas",
                "Validação de senha nova",
                "Limpeza automática"
            ]
            
            for nome, resultado in zip(nomes, resultados):
                status = "✅ PASSOU" if resultado else "❌ FALHOU"
                print(f"{status} - {nome}")
            
            print()
            total = len(resultados)
            passou = sum(resultados)
            falhou = total - passou
            print("-"*70)
            print(f"Total: {total} testes | Passou: {passou} | Falhou: {falhou}")
            print("-"*70)
            
            if falhou == 0:
                print("\n🎉 TODOS OS TESTES PASSARAM! Sistema de histórico de senhas está funcionando.")
                return True
            else:
                print(f"\n⚠️  {falhou} teste(s) falharam.")
                return False
                
        except ImportError as e:
            print(f"❌ ERRO ao importar: {e}")
            return False
        except Exception as e:
            print(f"❌ ERRO durante teste: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    sucesso = testar_historico_senhas()
    sys.exit(0 if sucesso else 1)
