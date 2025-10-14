# 🧠 Text Normalizer (Português - BR)

Biblioteca Python para **normalização de texto em português**, focada em conversão de valores numéricos, datas, horários e moedas para forma escrita por extenso.

Ideal para aplicações de **voz (TTS)**, **NLP** ou **pré-processamento de dados textuais**, onde a leitura natural é importante.

---

## 🧬 Funcionalidades Implementadas

### 1. Normalização de Moeda (R$)

- `R$ 50` → `cinquenta reais`
- `R$ 1,50` → `um real e cinquenta centavos`
- `R$ 100,99` → `cem reais e noventa e nove centavos`
- `R$ 0,05` → `cinco centavos`

### 2. Normalização de Datas

- `05/01/2026` → `cinco de janeiro de dois mil e vinte e seis`
- `25/12/1999` → `vinte e cinco de dezembro de mil novecentos e noventa e nove`
- `12/2025` → `dezembro de dois mil e vinte e cinco`
- `06/95` → `junho de mil novecentos e noventa e cinco`

### 3. Normalização de Horários

- `14h` → `quatorze horas`
- `14h30` → `quatorze horas e trinta minutos`
- `9h15` → `nove horas e quinze minutos`
- `12:00` → `doze horas`
- `1h` → `uma hora`
- `0h30` → `zero horas e trinta minutos`

### 4. Conversão de Números para Extenso

**Regras:**

- Números < 10.000: convertidos para extenso
- Números ≥ 10.000: convertidos em dígitos separados
- Números em moeda: sempre convertidos para extenso

**Exemplos:**

- `123` → `cento e vinte e três`
- `1000` → `mil`
- `12345` → `um dois três quatro cinco`
- `999999` → `nove nove nove nove nove nove`
- `25,5` → `vinte e cinco vírgula cinco`

### 5. Remoção de Caracteres Especiais

- Remove apenas caracteres problemáticos: @, #, $, %, &, *, etc.
- Mantém pontuação básica: pontos, vírgulas, exclamação, interrogação, parênteses, etc.
- `Olá! #hashtag @usuario` → `Olá!`

---

## 🧠 Exemplo de Uso Completo

```python
from text_normalizer.normalizer import normalize_text

texto = "Reunião 05/01/2026 às 14h30, código 12345"
print(normalize_text(texto))
# ➞ "Reunião cinco de janeiro de dois mil e vinte e seis às quatorze horas e trinta minutos, código um dois três quatro cinco"
```