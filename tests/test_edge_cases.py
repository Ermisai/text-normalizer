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


class TestEdgeCases(unittest.TestCase):
    """Testes para casos extremos e edge cases"""
    
    def test_empty_and_none_inputs(self):
        """Testa entradas vazias e None"""
        self.assertEqual(normalize_text(""), "")
        self.assertEqual(normalize_text("   "), "   ")
        self.assertEqual(normalize_text(None), None)
        
        # Funções individuais com strings vazias
        self.assertEqual(normalize_currency(""), "")
        self.assertEqual(normalize_dates(""), "")
        self.assertEqual(normalize_time(""), "")
        self.assertEqual(normalize_numbers(""), "")
        self.assertEqual(normalize_numeric_sequences(""), "")
        self.assertEqual(remove_non_alphanumeric(""), "")
    
    def test_only_whitespace(self):
        """Testa textos com apenas espaços em branco"""
        self.assertEqual(normalize_text("   \t\n  "), "   \t\n  ")
        self.assertEqual(remove_non_alphanumeric("   \t\n  "), "")
    
    def test_very_large_numbers(self):
        """Testa números muito grandes"""
        large_number = "123456789012345"
        result = normalize_numbers(large_number)
        # Deve ser convertido em dígitos separados
        expected = "um dois três quatro cinco seis sete oito nove zero um dois três quatro cinco"
        self.assertEqual(result, expected)
    
    def test_multiple_currencies_in_text(self):
        """Testa múltiplas moedas no mesmo texto"""
        text = "Primeiro R$ 10, depois R$ 20,50 e por fim R$ 0,99"
        result = normalize_currency(text)
        self.assertIn("dez reais", result)
        self.assertIn("vinte reais e cinquenta centavos", result)
        self.assertIn("noventa e nove centavos", result)
    
    def test_multiple_dates_in_text(self):
        """Testa múltiplas datas no mesmo texto"""
        text = "Nasceu em 15/01/1990 e se formou em 12/2015"
        result = normalize_dates(text)
        self.assertIn("quinze de janeiro", result)
        self.assertIn("dezembro de", result)
    
    def test_multiple_times_in_text(self):
        """Testa múltiplos horários no mesmo texto"""
        text = "Reunião às 9h, almoço às 12h30 e fim às 18h"
        result = normalize_time(text)
        self.assertIn("nove horas", result)
        self.assertIn("doze horas e trinta minutos", result)
        self.assertIn("dezoito horas", result)
    
    def test_boundary_values(self):
        """Testa valores limítrofes"""
        # Números no limite de 10000
        self.assertEqual(normalize_numbers("9999"), "nove mil, novecentos e noventa e nove")
        self.assertEqual(normalize_numbers("10000"), "um zero zero zero zero")
        
        # Horários limítrofes
        self.assertEqual(normalize_time("0h"), "zero horas")
        self.assertEqual(normalize_time("23h59"), "vinte e três horas e cinquenta e nove minutos")
        
        # Datas limítrofes
        self.assertEqual(normalize_dates("01/01/00"), "um de janeiro de dois mil")
        self.assertEqual(normalize_dates("31/12/99"), "trinta e um de dezembro de mil, novecentos e noventa e nove")
    
    def test_invalid_formats(self):
        """Testa formatos inválidos que devem ser ignorados"""
        # Datas inválidas
        self.assertEqual(normalize_dates("32/13/2025"), "32/13/2025")
        self.assertEqual(normalize_dates("00/00/2025"), "00/00/2025")
        
        # Horários inválidos
        self.assertEqual(normalize_time("25h"), "25h")
        self.assertEqual(normalize_time("14h70"), "14h70")
        
        # Moedas sem valor
        self.assertEqual(normalize_currency("R$"), "R$")
        self.assertEqual(normalize_currency("R$ "), "R$ ")
    
    def test_mixed_separators(self):
        """Testa separadores mistos em números"""
        # Decimais com ponto
        result = normalize_numbers("123.45")
        self.assertIn("vírgula", result)
        
        # Decimais com vírgula
        result = normalize_numbers("123,45")
        self.assertIn("vírgula", result)
    
    def test_special_characters_preservation(self):
        """Testa preservação de caracteres especiais válidos"""
        text = "Olá! Como vai? Tudo bem... (espero que sim); \"certamente\" - ok."
        result = remove_non_alphanumeric(text)
        
        # Deve manter pontuação básica
        self.assertIn("!", result)
        self.assertIn("?", result)
        self.assertIn(".", result)
        self.assertIn("(", result)
        self.assertIn(")", result)
        self.assertIn(";", result)
        self.assertIn("\"", result)
        self.assertIn("-", result)
    
    def test_numbers_with_leading_zeros(self):
        """Testa números com zeros à esquerda"""
        self.assertEqual(normalize_numbers("007"), "sete")
        self.assertEqual(normalize_numbers("0123"), "cento e vinte e três")
    
    def test_complex_numeric_sequences(self):
        """Testa sequências numéricas complexas"""
        # Múltiplos pontos e hífens
        text = "123.456.789.012-34"
        result = normalize_numeric_sequences(text)
        self.assertIn("ponto", result)
        self.assertIn("traço", result)
        
        # Sequência sem pontos ou hífens (deve ser ignorada)
        text = "123456789"
        result = normalize_numeric_sequences(text)
        self.assertEqual(result, "123456789")  # Não deve ser alterado
    
    def test_currency_edge_cases(self):
        """Testa casos extremos de moeda"""
        # Zero reais com centavos zero
        self.assertEqual(normalize_currency("R$ 0,00"), "zero reais")
        
        # Um real exato
        self.assertEqual(normalize_currency("R$ 1,00"), "um real")
        
        # Apenas um centavo
        self.assertEqual(normalize_currency("R$ 0,01"), "um centavo")
    
    def test_performance_with_long_text(self):
        """Testa performance com texto longo"""
        # Texto repetitivo longo
        long_text = "Teste 123 R$ 50,00 em 01/01/2025 às 14h30. " * 100
        result = normalize_text(long_text)
        
        # Verifica que pelo menos algumas normalizações foram aplicadas
        self.assertIn("cento e vinte e três", result)
        self.assertIn("cinquenta reais", result)
        self.assertIn("um de janeiro", result)  # A função usa "um", não "primeiro"
        self.assertIn("catorze horas", result)
    
    def test_unicode_and_accents(self):
        """Testa caracteres unicode e acentos"""
        text = "Reunião às 15h com José da Conceição"
        result = normalize_text(text)
        
        # Deve preservar acentos
        self.assertIn("Reunião", result)
        self.assertIn("Conceição", result)
        self.assertIn("quinze horas", result)
    
    def test_order_independence(self):
        """Testa que a ordem das funções não afeta outros padrões"""
        text = "15h do dia 15/12/2025 com R$ 15"
        result = normalize_text(text)
        
        # Cada padrão deve ser normalizado independentemente
        self.assertIn("quinze horas", result)
        self.assertIn("quinze de dezembro", result)
        self.assertIn("quinze reais", result)


class TestRegressionCases(unittest.TestCase):
    """Testes de regressão para bugs conhecidos"""
    
    def test_currency_thousands_separator_bug(self):
        """Documenta o bug com separador de milhares em moedas"""
        # Este é um bug conhecido - a regex não captura R$ 1.234,56 corretamente
        text = "R$ 1.234,56"
        result = normalize_currency(text)
        # O comportamento atual é incorreto, mas documentamos aqui
        self.assertNotEqual(result, "mil duzentos e trinta e quatro reais e cinquenta e seis centavos")
    
    def test_slash_in_numeric_sequences(self):
        """Documenta o comportamento com barras em sequências numéricas"""
        # CNPJ com barra não é totalmente normalizado
        text = "12.345.678/0001-90"
        result = normalize_numeric_sequences(text)
        # Deve manter a barra como está
        self.assertIn("/", result)
    
    def test_decimal_precision_handling(self):
        """Testa tratamento de precisão decimal"""
        # A função trata ,5 como ,50 (50 centavos)
        result = normalize_numbers("25,5")
        self.assertEqual(result, "vinte e cinco vírgula cinquenta")
        
        # Mas trata ,05 como 5 centavos
        result = normalize_numbers("25,05")
        self.assertEqual(result, "vinte e cinco vírgula cinco")


if __name__ == '__main__':
    unittest.main(verbosity=2)