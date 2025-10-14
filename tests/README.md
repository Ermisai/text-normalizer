# Testes para o Text Normalizer

Este diretório contém uma suíte abrangente de testes para o módulo `text_normalizer`.

## Estrutura dos Testes

### `test_normalizer.py`
Testes principais que cobrem todas as funcionalidades básicas:

- **TestNormalizeNumericSequences**: Testa conversão de sequências numéricas (CPF, CNPJ)
- **TestNormalizeCurrency**: Testa normalização de valores monetários 
- **TestNormalizeDates**: Testa conversão de datas para extenso
- **TestNormalizeTime**: Testa conversão de horários para extenso
- **TestNormalizeNumbers**: Testa conversão de números para extenso
- **TestRemoveNonAlphanumeric**: Testa remoção de caracteres especiais
- **TestNormalizeText**: Testa a função principal que aplica todas as normalizações

### `test_edge_cases.py` 
Testes para casos extremos e edge cases:

- **TestEdgeCases**: Casos limítrofes, entradas vazias, valores grandes, etc.
- **TestRegressionCases**: Documenta bugs conhecidos e comportamentos específicos

## Cobertura dos Testes

Os testes cobrem:

✅ **Normalização de sequências numéricas**
- CPF (123.456.789-00)
- CNPJ (12.345.678/0001-90)
- Outras sequências com pontos e hífens

✅ **Normalização de moeda**
- Valores simples (R$ 50)
- Valores com centavos (R$ 1,50)
- Apenas centavos (R$ 0,99)
- Diferentes formatos de separador decimal

✅ **Normalização de datas**
- Formato completo (dd/mm/yyyy)
- Formato mês/ano (mm/yyyy)
- Anos de 2 dígitos
- Validação de datas inválidas

✅ **Normalização de horários**
- Apenas horas (14h)
- Horas e minutos (14h30)
- Formato com dois pontos (14:30)
- Validação de horários inválidos

✅ **Normalização de números**
- Números pequenos (< 10000) → extenso
- Números grandes (≥ 10000) → dígitos separados
- Números decimais
- Casos especiais (zero, números com zeros à esquerda)

✅ **Remoção de caracteres especiais**
- Tokens de redes sociais (@usuario, #hashtag)
- Caracteres especiais problemáticos
- Preservação de pontuação básica

✅ **Integração completa**
- Ordem correta das operações
- Múltiplas normalizações no mesmo texto
- Textos complexos do mundo real

## Como Executar os Testes

### Executar todos os testes:
```bash
cd /home/lucas/text-normalizer
python -m pytest tests/ -v
```

### Executar testes específicos:
```bash
# Apenas testes básicos
python -m pytest tests/test_normalizer.py -v

# Apenas casos extremos
python -m pytest tests/test_edge_cases.py -v

# Executar um teste específico
python -m pytest tests/test_normalizer.py::TestNormalizeCurrency::test_simple_reais -v
```

### Executar com relatório de cobertura:
```bash
python -m pytest tests/ --cov=text_normalizer --cov-report=html
```

## Casos de Teste Documentados

### Bugs Conhecidos
- **Separador de milhares em moedas**: R$ 1.234,56 não é processado corretamente
- **Barras em sequências numéricas**: CNPJs com `/` mantêm a barra original
- **Precisão decimal**: 25,5 é tratado como 25,50 (cinquenta centavos)

### Casos Extremos Testados
- Entradas vazias e None
- Números muito grandes (> 10^14)
- Múltiplas ocorrências no mesmo texto
- Valores limítrofes (9999 vs 10000)
- Caracteres Unicode e acentos
- Performance com textos longos

## Estatísticas

- **Total de testes**: 58
- **Classes de teste**: 10
- **Funcionalidades testadas**: 7
- **Taxa de aprovação**: 100%

## Próximos Passos

Para melhorar a cobertura de testes, considere adicionar:

1. Testes de performance mais detalhados
2. Testes de concorrência (se aplicável)
3. Testes com diferentes locales
4. Testes de integração com sistemas externos
5. Correção dos bugs documentados nos testes de regressão