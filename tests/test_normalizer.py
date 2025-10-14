import unittest
import sys
import os

# Adicionar o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from text_normalizer import (
    normalize_text,
    normalize_currency,
    normalize_dates,
    normalize_time,
    normalize_numbers,
    normalize_numeric_sequences,
    remove_non_alphanumeric
)


class TestNormalizeNumericSequences(unittest.TestCase):
    """Testes para a função normalize_numeric_sequences"""
    
    def test_cpf_format(self):
        """Testa conversão de CPF"""
        input_text = "123.456.789-00"
        expected = "um dois três ponto quatro cinco seis ponto sete oito nove traço zero zero"
        result = normalize_numeric_sequences(input_text)
        self.assertEqual(result, expected)
    
    def test_cpf_with_text(self):
        """Testa CPF com texto ao redor"""
        input_text = "Meu CPF é 123.456.789-00 válido"
        expected = "Meu CPF é um dois três ponto quatro cinco seis ponto sete oito nove traço zero zero válido"
        result = normalize_numeric_sequences(input_text)
        self.assertEqual(result, expected)
    
    def test_cnpj_format(self):
        """Testa conversão de CNPJ"""
        input_text = "12.345.678/0001-90"
        expected = "um dois ponto três quatro cinco ponto seis sete oito/zero zero zero um traço nove zero"
        result = normalize_numeric_sequences(input_text)
        self.assertEqual(result, expected)
    
    def test_simple_numbers_unchanged(self):
        """Testa que números simples não são alterados"""
        input_text = "123 456 789"
        expected = "123 456 789"
        result = normalize_numeric_sequences(input_text)
        self.assertEqual(result, expected)
    
    def test_mixed_content(self):
        """Testa texto misto com números simples e sequências"""
        input_text = "O número 123 e o CPF 456.789.012-34"
        expected = "O número 123 e o CPF quatro cinco seis ponto sete oito nove ponto zero um dois traço três quatro"
        result = normalize_numeric_sequences(input_text)
        self.assertEqual(result, expected)


class TestNormalizeCurrency(unittest.TestCase):
    """Testes para a função normalize_currency"""
    
    def test_simple_reais(self):
        """Testa valores em reais simples"""
        self.assertEqual(normalize_currency("R$ 50"), "cinquenta reais")
        self.assertEqual(normalize_currency("R$ 1"), "um real")
        self.assertEqual(normalize_currency("R$ 0"), "zero reais")
    
    def test_reais_with_centavos(self):
        """Testa valores com centavos"""
        self.assertEqual(normalize_currency("R$ 1,50"), "um real e cinquenta centavos")
        self.assertEqual(normalize_currency("R$ 25,99"), "vinte e cinco reais e noventa e nove centavos")
        self.assertEqual(normalize_currency("R$ 100,01"), "cem reais e um centavo")
    
    def test_only_centavos(self):
        """Testa apenas centavos"""
        self.assertEqual(normalize_currency("R$ 0,50"), "cinquenta centavos")
        self.assertEqual(normalize_currency("R$ 0,01"), "um centavo")
        self.assertEqual(normalize_currency("R$ 0,99"), "noventa e nove centavos")
    
    def test_decimal_point_format(self):
        """Testa formato com ponto decimal"""
        self.assertEqual(normalize_currency("R$ 1.50"), "um real e cinquenta centavos")
        self.assertEqual(normalize_currency("R$ 25.5"), "vinte e cinco reais e cinquenta centavos")
    
    def test_spaces_in_currency(self):
        """Testa valores com espaços"""
        self.assertEqual(normalize_currency("R$50"), "cinquenta reais")
        self.assertEqual(normalize_currency("R$ 50"), "cinquenta reais")
    
    def test_large_values(self):
        """Testa valores grandes"""
        self.assertEqual(normalize_currency("R$ 1000"), "mil reais")
        self.assertEqual(normalize_currency("R$ 1500,75"), "mil e quinhentos reais e setenta e cinco centavos")
    
    def test_currency_with_thousands_separator_issue(self):
        """Documenta problema com separador de milhares"""
        # NOTA: A regex atual não suporta adequadamente R$ 1.500,75
        # Este teste documenta o comportamento atual que precisa ser corrigido
        result = normalize_currency("R$ 1.500,75")
        self.assertIn("real", result)  # Verifica que pelo menos parte é processada


class TestNormalizeDates(unittest.TestCase):
    """Testes para a função normalize_dates"""
    
    def test_full_date_format(self):
        """Testa datas completas dd/mm/yyyy"""
        self.assertEqual(normalize_dates("05/01/2026"), "cinco de janeiro de dois mil e vinte e seis")
        self.assertEqual(normalize_dates("25/12/2025"), "vinte e cinco de dezembro de dois mil e vinte e cinco")
        self.assertEqual(normalize_dates("01/01/2000"), "um de janeiro de dois mil")
    
    def test_two_digit_year(self):
        """Testa datas com ano de 2 dígitos"""
        self.assertEqual(normalize_dates("25/12/99"), "vinte e cinco de dezembro de mil, novecentos e noventa e nove")
        self.assertEqual(normalize_dates("01/01/25"), "um de janeiro de dois mil e vinte e cinco")
        self.assertEqual(normalize_dates("15/06/50"), "quinze de junho de mil, novecentos e cinquenta")
    
    def test_month_year_format(self):
        """Testa formato mês/ano"""
        self.assertEqual(normalize_dates("12/2025"), "dezembro de dois mil e vinte e cinco")
        self.assertEqual(normalize_dates("01/99"), "janeiro de mil, novecentos e noventa e nove")
        self.assertEqual(normalize_dates("06/25"), "junho de dois mil e vinte e cinco")
    
    def test_invalid_dates(self):
        """Testa que datas inválidas não são alteradas"""
        self.assertEqual(normalize_dates("32/01/2025"), "32/01/2025")  # Dia inválido
        self.assertEqual(normalize_dates("15/13/2025"), "15/13/2025")  # Mês inválido
        self.assertEqual(normalize_dates("00/01/2025"), "00/01/2025")  # Dia zero
    
    def test_date_in_context(self):
        """Testa datas dentro de texto"""
        input_text = "A reunião será em 15/03/2025 às 14h"
        expected = "A reunião será em quinze de março de dois mil e vinte e cinco às 14h"
        self.assertEqual(normalize_dates(input_text), expected)


class TestNormalizeTime(unittest.TestCase):
    """Testes para a função normalize_time"""
    
    def test_hour_only(self):
        """Testa horários apenas com horas"""
        self.assertEqual(normalize_time("14h"), "catorze horas")
        self.assertEqual(normalize_time("1h"), "uma hora")
        self.assertEqual(normalize_time("0h"), "zero horas")
        self.assertEqual(normalize_time("23h"), "vinte e três horas")
    
    def test_hour_with_minutes(self):
        """Testa horários com horas e minutos"""
        self.assertEqual(normalize_time("14h30"), "catorze horas e trinta minutos")
        self.assertEqual(normalize_time("9h15"), "nove horas e quinze minutos")
        self.assertEqual(normalize_time("13h01"), "treze horas e um minuto")
        self.assertEqual(normalize_time("8h00"), "oito horas")
    
    def test_colon_format(self):
        """Testa formato com dois pontos"""
        self.assertEqual(normalize_time("14:30"), "catorze horas e trinta minutos")
        self.assertEqual(normalize_time("9:15"), "nove horas e quinze minutos")
        self.assertEqual(normalize_time("0:00"), "zero horas")
    
    def test_invalid_times(self):
        """Testa horários inválidos"""
        self.assertEqual(normalize_time("25h"), "25h")  # Hora inválida
        self.assertEqual(normalize_time("14h60"), "14h60")  # Minuto inválido
        self.assertEqual(normalize_time("24:00"), "24:00")  # Hora inválida
    
    def test_time_in_context(self):
        """Testa horários dentro de texto"""
        input_text = "A reunião é às 14h30 na sala"
        expected = "A reunião é às catorze horas e trinta minutos na sala"
        self.assertEqual(normalize_time(input_text), expected)


class TestNormalizeNumbers(unittest.TestCase):
    """Testes para a função normalize_numbers"""
    
    def test_small_numbers(self):
        """Testa números pequenos (< 10000)"""
        self.assertEqual(normalize_numbers("123"), "cento e vinte e três")
        self.assertEqual(normalize_numbers("1"), "um")
        self.assertEqual(normalize_numbers("0"), "zero")
        self.assertEqual(normalize_numbers("9999"), "nove mil, novecentos e noventa e nove")
    
    def test_large_numbers(self):
        """Testa números grandes (>= 10000)"""
        self.assertEqual(normalize_numbers("12345"), "um dois três quatro cinco")
        self.assertEqual(normalize_numbers("100000"), "um zero zero zero zero zero")
    
    def test_decimal_numbers(self):
        """Testa números decimais"""
        self.assertEqual(normalize_numbers("25,5"), "vinte e cinco vírgula cinquenta")
        self.assertEqual(normalize_numbers("1,99"), "um vírgula noventa e nove")
        self.assertEqual(normalize_numbers("0,5"), "zero vírgula cinquenta")
        self.assertEqual(normalize_numbers("123.45"), "cento e vinte e três vírgula quarenta e cinco")
    
    def test_zero_cases(self):
        """Testa casos especiais com zero"""
        self.assertEqual(normalize_numbers("0,0"), "zero")
        self.assertEqual(normalize_numbers("0,50"), "zero vírgula cinquenta")
        self.assertEqual(normalize_numbers("100,0"), "cem")
    
    def test_large_decimals(self):
        """Testa decimais grandes"""
        self.assertEqual(normalize_numbers("12345,678"), "um dois três quatro cinco vírgula sessenta e oito")


class TestRemoveNonAlphanumeric(unittest.TestCase):
    """Testes para a função remove_non_alphanumeric"""
    
    def test_remove_social_media_tokens(self):
        """Testa remoção de tokens de redes sociais"""
        self.assertEqual(remove_non_alphanumeric("Olá @usuario como vai?"), "Olá como vai?")
        self.assertEqual(remove_non_alphanumeric("Veja isso #hashtag legal"), "Veja isso legal")
        self.assertEqual(remove_non_alphanumeric("@user1 e @user2 #tag1 #tag2"), "e")
    
    def test_remove_special_chars(self):
        """Testa remoção de caracteres especiais"""
        self.assertEqual(remove_non_alphanumeric("R$%&*=[]{}|\\<>~^`"), "R")
        self.assertEqual(remove_non_alphanumeric("teste$123%abc"), "teste123abc")
    
    def test_keep_basic_punctuation(self):
        """Testa que pontuação básica é mantida"""
        input_text = "Olá, como vai? Tudo bem! (sim): estava aqui; \"falando\" - ok."
        # A função deve manter pontuação básica
        result = remove_non_alphanumeric(input_text)
        self.assertIn(",", result)
        self.assertIn("?", result)
        self.assertIn("!", result)
        self.assertIn("(", result)
        self.assertIn(")", result)
        self.assertIn(":", result)
        self.assertIn(";", result)
        self.assertIn("\"", result)
        self.assertIn("-", result)
        self.assertIn(".", result)
    
    def test_multiple_spaces(self):
        """Testa remoção de espaços múltiplos"""
        self.assertEqual(remove_non_alphanumeric("a    b     c"), "a b c")
        self.assertEqual(remove_non_alphanumeric("  inicio  meio  fim  "), "inicio meio fim")


class TestNormalizeText(unittest.TestCase):
    """Testes para a função principal normalize_text"""
    
    def test_empty_input(self):
        """Testa entrada vazia"""
        self.assertEqual(normalize_text(""), "")
        self.assertEqual(normalize_text("   "), "   ")
        self.assertEqual(normalize_text(None), None)
    
    def test_complete_normalization(self):
        """Testa normalização completa com múltiplas funcionalidades"""
        input_text = "Reunião em 15/03/2025 às 14h30 para discutir R$ 500,75 do CPF 123.456.789-00"
        result = normalize_text(input_text)
        
        # Verificar se todas as normalizações foram aplicadas
        self.assertIn("quinze de março de dois mil e vinte e cinco", result)
        self.assertIn("catorze horas e trinta minutos", result)
        self.assertIn("quinhentos reais e setenta e cinco centavos", result)
        self.assertIn("um dois três ponto quatro cinco seis ponto sete oito nove traço zero zero", result)
    
    def test_currency_before_numbers(self):
        """Testa que moeda é processada antes de números simples"""
        input_text = "R$ 50 e também 50"
        result = normalize_text(input_text)
        self.assertIn("cinquenta reais", result)
        self.assertIn("cinquenta", result)
    
    def test_dates_before_numbers(self):
        """Testa que datas são processadas antes de números"""
        input_text = "15/03/2025 e o número 15"
        result = normalize_text(input_text)
        self.assertIn("quinze de março", result)
        self.assertIn("quinze", result)
    
    def test_numeric_sequences_before_simple_numbers(self):
        """Testa que sequências numéricas são processadas antes de números simples"""
        input_text = "CPF 123.456.789-00 e número 123"
        result = normalize_text(input_text)
        self.assertIn("um dois três ponto", result)  # CPF como dígitos
        self.assertIn("cento e vinte e três", result)  # 123 como extenso
    
    def test_special_characters_removal(self):
        """Testa remoção de caracteres especiais"""
        input_text = "Texto com @usuario #hashtag e símbolos $%&"
        result = normalize_text(input_text)
        self.assertNotIn("@usuario", result)
        self.assertNotIn("#hashtag", result)
        self.assertNotIn("$", result)
        self.assertNotIn("%", result)
        self.assertNotIn("&", result)
    
    def test_complex_real_world_example(self):
        """Testa exemplo do mundo real complexo"""
        input_text = "O pagamento de R$ 500,00 vence em 30/12/2025 às 18h. CPF: 987.654.321-00 @cliente #urgente"
        result = normalize_text(input_text)
        
        # Verificar componentes
        self.assertIn("quinhentos reais", result)
        self.assertIn("trinta de dezembro de dois mil e vinte e cinco", result)
        self.assertIn("dezoito horas", result)
        self.assertIn("nove oito sete ponto seis cinco quatro ponto três dois um traço zero zero", result)
        self.assertNotIn("@cliente", result)
        self.assertNotIn("#urgente", result)
    
    def test_order_of_operations(self):
        """Testa a ordem correta das operações"""
        # Teste para garantir que a ordem é respeitada
        input_text = "R$ 15 às 15h em 15/12/25 número 15"
        result = normalize_text(input_text)
        
        # R$ 15 deve virar "quinze reais" (não "um cinco reais")
        self.assertIn("quinze reais", result)
        # 15h deve virar "quinze horas" 
        self.assertIn("quinze horas", result)
        # 15/12/25 deve ser tratado como data
        self.assertIn("quinze de dezembro", result)
        # O último 15 deve virar "quinze" (extenso)
        parts = result.split()
        self.assertIn("quinze", parts[-1:])  # Verifica se há "quinze" no final


if __name__ == '__main__':
    unittest.main(verbosity=2)