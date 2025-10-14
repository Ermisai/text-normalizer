#!/usr/bin/env python3
"""
Exemplo prático de normalização de URLs para TTS
Este script demonstra como a normalização de URLs facilita a síntese de texto para áudio
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from text_normalizer import normalize_text, normalize_urls

def demo_url_normalization():
    """Demonstra a normalização de URLs para síntese de voz"""
    
    print("=== DEMONSTRAÇÃO: NORMALIZAÇÃO DE URLs PARA TTS ===\n")
    
    # Exemplos de URLs e emails comuns
    test_cases = [
        "Visite nosso site: https://www.exemplo.com.br",
        "Acesse http://github.com/usuario/projeto para ver o código",
        "Envie um email para contato@empresa.org",
        "Site principal: www.minhaempresa.net/produtos",
        "Documentação em https://docs.site.com/api/v2?lang=pt&format=json",
        "Canal no YouTube: https://youtube.com/watch?v=abc123#comentarios",
        "Perfil social: user_name@social.co.uk",
        "Compre por R$ 99,90 em loja.com até 25/12/2025 às 18h30",
        "Suporte técnico: help@support-center.com ou ligue 11 99999-9999"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"Exemplo {i}:")
        print(f"  Original: {text}")
        
        # Normalizar apenas URLs
        url_normalized = normalize_urls(text)
        print(f"  URLs:     {url_normalized}")
        
        # Normalização completa
        full_normalized = normalize_text(text)
        print(f"  Completo: {full_normalized}")
        print()

def compare_tts_output():
    """Compara como o texto soaria em TTS antes e depois da normalização"""
    
    print("=== COMPARAÇÃO PARA TTS ===\n")
    
    complex_text = """
    Para acessar nossa plataforma, visite https://www.plataforma.com.br/login
    ou envie email para suporte@help.com. 
    
    O custo é de R$ 299,90 por mês. Promoção válida até 31/12/2025.
    
    Dúvidas? Ligue para 11 98765-4321 das 9h às 18h.
    """
    
    print("TEXTO ORIGINAL para TTS:")
    print(complex_text)
    print("\n" + "="*60 + "\n")
    
    print("TEXTO NORMALIZADO para TTS:")
    normalized = normalize_text(complex_text.strip())
    print(normalized)
    
    print("\n" + "="*60 + "\n")
    
    # Análise dos benefícios
    print("BENEFÍCIOS PARA TTS:")
    print("✅ URLs são pronunciadas letra por letra de forma compreensível")
    print("✅ Emails ficam claros com 'arroba' em vez de '@'")
    print("✅ Valores monetários são lidos por extenso")
    print("✅ Datas ficam mais naturais")
    print("✅ Telefones são pronunciados dígito por dígito")
    print("✅ Horários são lidos como 'nove horas' em vez de '9h'")

def test_edge_cases():
    """Testa casos extremos de URLs"""
    
    print("\n=== CASOS EXTREMOS DE URLs ===\n")
    
    edge_cases = [
        "FTP não suportado: ftp://files.example.com",
        "URL maiúscula: HTTPS://SITE.COM/PATH",
        "Subdomínio: api.v2.service.company.com",
        "Email com símbolos: user+tag@domain-name.co.uk", 
        "URL com porta: http://localhost:8080/app",
        "IP não é normalizado: 192.168.1.1",
        "Domínio falso: arquivo.com não é URL"
    ]
    
    for case in edge_cases:
        print(f"Entrada:  {case}")
        result = normalize_urls(case)
        print(f"Saída:    {result}")
        print()

if __name__ == "__main__":
    demo_url_normalization()
    compare_tts_output()
    test_edge_cases()
    
    print("\n🎤 Seu texto está pronto para TTS!")
    print("💡 Dica: Use normalize_text() para normalização completa")
    print("🔧 Use normalize_urls() para normalizar apenas URLs e emails")