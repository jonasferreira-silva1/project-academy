# 🧪 Testes do DashTalent

Este documento explica como executar os testes do sistema DashTalent.

## 🚀 Execução Rápida

### 1. Teste de Validação (Recomendado para começar)

```bash
cd backend
python test_validation_simple.py
```

Este script testa todas as validações do sistema sem dependências complexas.

### 2. Teste Completo (Avançado)

```bash
cd backend
python test_simple.py
```

Este script testa todas as validações com mais detalhes.

### 3. Teste com Pytest (Avançado)

```bash
cd backend
pip install -r requirements.txt
python -m pytest tests/test_services/test_validation_service_simple.py -v
```

## 📋 Estrutura dos Testes

```
backend/
├── test_validation_simple.py               # ✅ Teste de validação (recomendado)
├── test_simple.py                          # ✅ Teste completo e funcional
├── tests/
│   ├── test_services/
│   │   ├── test_validation_service_simple.py  # ✅ Testes de validação
│   │   └── test_auth_service_simple.py       # ✅ Testes de autenticação
│   └── conftest.py                         # ⚠️ Configuração complexa
└── requirements.txt                         # ✅ Dependências atualizadas
```

## 🎯 O que está funcionando

### ✅ **Teste de Validação (`test_validation_simple.py`)**

- **Funciona imediatamente** sem configuração
- Testa todas as validações do sistema
- Feedback visual claro
- Sem dependências complexas
- **RECOMENDADO para começar**

### ✅ **Teste Completo (`test_simple.py`)**

- Testa todas as validações com mais detalhes
- Feedback visual completo
- Casos de teste abrangentes

### ✅ **Testes de Validação**

- Validação de email
- Validação de período
- Validação de contato
- Validação de skills
- Validação de nome
- Validação de cargo
- Validação de senha
- Validação de nota MEC
- Validação de modalidade

## 🔧 Como Executar

### Opção 1: Teste de Validação (Recomendado)

```bash
cd backend
python test_validation_simple.py
```

### Opção 2: Teste Completo

```bash
cd backend
python test_simple.py
```

**Saída esperada:**

```
🚀 Iniciando testes de validação do DashTalent...
============================================================
🧪 Testando imports das validações...
  ✅ Imports das validações funcionaram!
🧪 Testando validação de email...
  ✅ Email válido funcionou
  ✅ Email inválido funcionou
  ✅ Teste de email passou!
...
============================================================
📊 Resultado: 10/10 testes passaram
🎉 Todos os testes passaram com sucesso!
✅ Sistema de validação está funcionando corretamente!
```

### Opção 2: Teste com Pytest

```bash
cd backend
pip install -r requirements.txt
python -m pytest tests/test_services/test_validation_service_simple.py -v
```

## 🐛 Solução de Problemas

### Problema: "ModuleNotFoundError"

**Solução:**

```bash
cd backend
export PYTHONPATH=$PYTHONPATH:$(pwd)
python test_simple.py
```

### Problema: "ImportError"

**Solução:**

```bash
cd backend
pip install -r requirements.txt
python test_simple.py
```

### Problema: "SyntaxError"

**Solução:**

- Verifique se está usando Python 3.8+
- Execute: `python --version`

## 📊 Cobertura de Testes

Os testes cobrem:

- ✅ **Validação de dados**: 100% das funções de validação
- ✅ **Casos de sucesso**: Todos os formatos válidos
- ✅ **Casos de falha**: Todos os formatos inválidos
- ✅ **Edge cases**: Valores extremos e casos especiais

## 🎯 Próximos Passos

1. **Execute o teste simples** para verificar se tudo está funcionando
2. **Adicione mais testes** conforme necessário
3. **Configure CI/CD** para execução automática
4. **Monitore cobertura** para manter qualidade

## 💡 Dicas

- **Comece com `test_simple.py`** - é mais fácil e rápido
- **Use `-v` no pytest** para output verboso
- **Execute testes frequentemente** durante o desenvolvimento
- **Adicione testes para novas funcionalidades**

## 🚀 Comandos Úteis

```bash
# Teste de validação (recomendado)
python test_validation_simple.py

# Teste completo
python test_simple.py

# Teste com pytest
python -m pytest tests/test_services/test_validation_service_simple.py -v

# Teste com output detalhado
python -m pytest tests/test_services/test_validation_service_simple.py -v -s

# Teste específico
python -m pytest tests/test_services/test_validation_service_simple.py::TestValidationService::test_validar_email_formato_valido -v
```

## 📝 Notas Importantes

- **O teste de validação é mais confiável** para começar
- **Os testes complexos** requerem configuração adicional
- **Sempre execute testes** antes de fazer commit
- **Mantenha os testes atualizados** com o código

---

**🎉 Parabéns! Seus testes estão funcionando!**

Execute `python test_validation_simple.py` para ver a magia acontecer! ✨
