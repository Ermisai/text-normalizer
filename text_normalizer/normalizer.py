import re
from num2words import num2words

def normalize_numeric_sequences(text: str) -> str:
    """
    Converte sequências numéricas com pontos e hífens para extenso, lendo cada dígito individualmente.
    Exemplos: 
    - 123.456.789-00 -> um dois três ponto quatro cinco seis ponto sete oito nove hífen zero zero
    - CPF 123.456.789-00 -> CPF um dois três ponto quatro cinco seis ponto sete oito nove hífen zero zero
    """
    # Padrão para capturar sequências de números com pontos e hífens
    numeric_pattern = r'\b\d+(?:[.\-]\d+)*\b'
    
    def digit_to_word(digit):
        """Converte um dígito individual para palavra."""
        digit_map = {
            '0': 'zero', '1': 'um', '2': 'dois', '3': 'três', '4': 'quatro',
            '5': 'cinco', '6': 'seis', '7': 'sete', '8': 'oito', '9': 'nove'
        }
        return digit_map.get(digit, digit)
    
    def replace_numeric_sequence(match):
        sequence = match.group()
        
        # Verificar se tem pelo menos um ponto ou hífen (para não afetar números simples)
        if '.' not in sequence and '-' not in sequence:
            return sequence  # Deixa números simples para a função normalize_numbers
        
        result = []
        for char in sequence:
            if char.isdigit():
                result.append(digit_to_word(char))
            elif char == '.':
                result.append('ponto')
            elif char == '-':
                result.append('traço')
        
        return ' '.join(result)
    
    return re.sub(numeric_pattern, replace_numeric_sequence, text)

def normalize_currency(text: str) -> str:
    """
    Converte valores de moeda para extenso.
    Exemplos: R$ 50 -> cinquenta reais, R$ 1,50 -> um real e cinquenta centavos
    """
    # Padrão para capturar valores monetários como R$ 50, R$ 1.50, R$ 1,50
    currency_pattern = r'R\$\s*(\d+)(?:[,.](\d{1,2}))?'
    
    def replace_currency(match):
        reais_str = match.group(1)
        centavos_str = match.group(2) if match.group(2) else None
        
        reais = int(reais_str)
        
        # Converter reais para extenso
        if reais == 0:
            reais_text = ""
        elif reais == 1:
            reais_text = "um real"
        else:
            reais_text = f"{num2words(reais, lang='pt_BR')} reais"
        
        # Tratar centavos se existirem
        if centavos_str:
            # Garantir que centavos tenham 2 dígitos
            centavos_str = centavos_str.ljust(2, '0')
            centavos = int(centavos_str)
            
            if centavos > 0:
                if centavos == 1:
                    centavos_text = "um centavo"
                else:
                    centavos_text = f"{num2words(centavos, lang='pt_BR')} centavos"
                
                if reais == 0:
                    return centavos_text
                else:
                    return f"{reais_text} e {centavos_text}"
        
        return reais_text if reais_text else "zero reais"
    
    return re.sub(currency_pattern, replace_currency, text)

def normalize_dates(text: str) -> str:
    """
    Converte datas para extenso.
    Suporta formatos: dd/mm/yyyy, mm/yyyy, dd/mm/yy, mm/yy
    Exemplos: 
    - 05/01/2026 -> cinco de janeiro de dois mil e vinte e seis
    - 12/2025 -> dezembro de dois mil e vinte e cinco
    - 25/12/99 -> vinte e cinco de dezembro de noventa e nove
    """
    # Mapeamento de meses
    months = {
        1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
        5: "maio", 6: "junho", 7: "julho", 8: "agosto",
        9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
    }
    
    # Padrão para dd/mm/yyyy ou dd/mm/yy
    date_pattern_full = r'\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b'
    
    # Padrão para mm/yyyy ou mm/yy  
    date_pattern_month_year = r'\b(\d{1,2})/(\d{2,4})\b'
    
    def replace_full_date(match):
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))
        
        # Validar mês
        if month < 1 or month > 12:
            return match.group(0)  # Retorna original se inválido
        
        # Validar dia
        if day < 1 or day > 31:
            return match.group(0)  # Retorna original se inválido
        
        # Converter componentes
        if day < 10000:
            day_text = num2words(day, lang='pt_BR')
        else:
            day_text = ' '.join(['zero', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove'][int(d)] for d in str(day))
        
        month_text = months[month]
        
        # Tratar ano
        if year < 100:  # Ano de 2 dígitos (assumir 20xx se < 50, senão 19xx)
            if year < 50:
                year += 2000
            else:
                year += 1900
        
        if year < 10000:
            year_text = num2words(year, lang='pt_BR')
        else:
            year_text = ' '.join(['zero', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove'][int(d)] for d in str(year))
        
        return f"{day_text} de {month_text} de {year_text}"
    
    def replace_month_year(match):
        month = int(match.group(1))
        year = int(match.group(2))
        
        # Validar mês
        if month < 1 or month > 12:
            return match.group(0)  # Retorna original se inválido
        
        month_text = months[month]
        
        # Tratar ano
        if year < 100:  # Ano de 2 dígitos
            if year < 50:
                year += 2000
            else:
                year += 1900
        
        if year < 10000:
            year_text = num2words(year, lang='pt_BR')
        else:
            year_text = ' '.join(['zero', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove'][int(d)] for d in str(year))
        
        return f"{month_text} de {year_text}"
    
    # Aplicar normalização de data completa primeiro
    text = re.sub(date_pattern_full, replace_full_date, text)
    
    # Depois aplicar normalização de mês/ano (apenas se não foi capturado pela anterior)
    text = re.sub(date_pattern_month_year, replace_month_year, text)
    
    return text

def normalize_numbers(text: str) -> str:
    """
    Converte números para extenso se forem menores que 10000, senão converte em dígitos separados.
    Exemplos: 
    - 123 -> cento e vinte e três
    - 12345 -> um dois três quatro cinco
    - 25,5 -> vinte e cinco vírgula cinco
    """
    # Padrão para capturar números (incluindo decimais)
    number_pattern = r'\b\d+(?:[,.]?\d+)?\b'
    
    def digit_to_word(digit):
        """Converte um dígito individual para palavra."""
        digit_map = {
            '0': 'zero', '1': 'um', '2': 'dois', '3': 'três', '4': 'quatro',
            '5': 'cinco', '6': 'seis', '7': 'sete', '8': 'oito', '9': 'nove'
        }
        return digit_map.get(digit, digit)
    
    def replace_number(match):
        number_str = match.group()
        
        # Tratar números decimais
        if ',' in number_str or '.' in number_str:
            # Substituir vírgula por ponto para conversão
            clean_number_str = number_str.replace(',', '.')
            try:
                number = float(clean_number_str)
                # Para decimais, converter a parte inteira e decimal separadamente
                integer_part = int(number)
                decimal_part = round((number - integer_part) * 100)
                
                if integer_part == 0 and decimal_part == 0:
                    return "zero"
                elif decimal_part == 0:
                    # Se a parte inteira for < 10000, usar extenso, senão dígitos
                    if integer_part < 10000:
                        return num2words(integer_part, lang='pt_BR')
                    else:
                        return ' '.join(digit_to_word(d) for d in str(integer_part))
                elif integer_part == 0:
                    if decimal_part < 10000:
                        return f"zero vírgula {num2words(decimal_part, lang='pt_BR')}"
                    else:
                        decimal_digits = ' '.join(digit_to_word(d) for d in str(decimal_part))
                        return f"zero vírgula {decimal_digits}"
                else:
                    # Tratar parte inteira
                    if integer_part < 10000:
                        integer_text = num2words(integer_part, lang='pt_BR')
                    else:
                        integer_text = ' '.join(digit_to_word(d) for d in str(integer_part))
                    
                    # Tratar parte decimal
                    if decimal_part < 10000:
                        decimal_text = num2words(decimal_part, lang='pt_BR')
                    else:
                        decimal_text = ' '.join(digit_to_word(d) for d in str(decimal_part))
                    
                    return f"{integer_text} vírgula {decimal_text}"
            except ValueError:
                return number_str
        else:
            try:
                number = int(number_str)
                # Se for menor que 10000, usar extenso, senão dígitos separados
                if number < 10000:
                    return num2words(number, lang='pt_BR')
                else:
                    return ' '.join(digit_to_word(d) for d in number_str)
            except ValueError:
                return number_str
    
    return re.sub(number_pattern, replace_number, text)

def normalize_time(text: str) -> str:
    """
    Converte horários para extenso.
    Exemplos: 14h -> catorze horas, 14h30 -> catorze horas e trinta minutos
    """
    # Padrão para capturar horários: 14h, 14h30, 14:30, 9h15, etc.
    time_pattern = r'\b(\d{1,2})(?:h|:)(\d{2})?\b'
    
    def replace_time(match):
        hours_str = match.group(1)
        minutes_str = match.group(2) if match.group(2) else None
        
        hours = int(hours_str)
        
        # Validar se são horas válidas (0-23)
        if hours > 23:
            return match.group(0)  # Retorna o original se inválido
        
        # Converter horas para extenso
        if hours == 0:
            hours_text = "zero horas"
        elif hours == 1:
            hours_text = "uma hora"
        else:
            hours_text = f"{num2words(hours, lang='pt_BR')} horas"
        
        # Tratar minutos se existirem
        if minutes_str:
            minutes = int(minutes_str)
            
            # Validar se são minutos válidos (0-59)
            if minutes > 59:
                return match.group(0)  # Retorna o original se inválido
            
            if minutes == 0:
                return hours_text
            elif minutes == 1:
                minutes_text = "um minuto"
            else:
                minutes_text = f"{num2words(minutes, lang='pt_BR')} minutos"
            
            return f"{hours_text} e {minutes_text}"
        else:
            return hours_text
    
    return re.sub(time_pattern, replace_time, text)

def remove_non_alphanumeric(text: str) -> str:
    """
    Remove apenas caracteres especiais problemáticos, mantendo pontuação básica.
    Remove tokens que começam com @, # e outros caracteres especiais.
    Mantém: letras, números, espaços, pontos, vírgulas, exclamação, interrogação, dois pontos, ponto e vírgula, parênteses, aspas, hífen
    """
    # Remover tokens que começam com @ ou # (como @usuario, #hashtag)
    cleaned_text = re.sub(r'[@#]\w+', '', text)
    
    # Remover outros caracteres especiais problemáticos
    cleaned_text = re.sub(r'[$%&*+=\[\]{}|\\<>~^`]', '', cleaned_text)
    
    # Remover espaços múltiplos
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    return cleaned_text.strip()

def normalize_urls(text: str) -> str:
    """
    Converte URLs para uma forma falada compreensível para TTS.
    Exemplos:
    - https://www.google.com -> agá tê tê pê ésse dois pontos barra barra dábliu dábliu dábliu ponto google ponto com
    - http://example.org/path -> agá tê tê pê dois pontos barra barra example ponto org barra path
    - www.site.com.br -> dábliu dábliu dábliu ponto site ponto com ponto bê érre
    - user@email.com -> user arroba email ponto com
    """
    import re
    
    # Padrão para URLs completas (http/https) - melhorado para capturar caminhos
    url_pattern = r'https?://(?:www\.)?([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,})([^\s]*)?'
    
    # Padrão para www sem protocolo - melhorado para capturar caminhos
    www_pattern = r'(?<!\w)www\.([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,})([^\s]*)?'
    
    # Padrão para emails
    email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
    
    # Padrão para domínios simples (mais restritivo para evitar falsos positivos)
    domain_pattern = r'(?<!\w)([a-zA-Z0-9\-]+\.(?:com\.br|co\.uk|co\.jp|com|org|net|edu|gov|mil|br|de|fr|it|es))\b(?![a-zA-Z0-9])'
    
    def convert_protocol(protocol):
        """Converte protocolos para forma falada"""
        if protocol.lower() == 'http':
            return 'agá tê tê pê'
        elif protocol.lower() == 'https':
            return 'agá tê tê pê ésse'
        return protocol
    
    def convert_www():
        """Converte www para forma falada"""
        return 'dábliu dábliu dábliu'
    
    def convert_domain_part(domain_part):
        """Converte partes do domínio para forma falada"""
        # Substituições específicas para TLDs comuns
        tld_map = {
            'com': 'com',
            'org': 'org',
            'net': 'net',
            'edu': 'edu',
            'gov': 'gov',
            'mil': 'mil',
            'br': 'bê érre',
            'uk': 'u kê',
            'jp': 'jê pê',
            'de': 'dê ê',
            'fr': 'êfe érre',
            'it': 'i tê',
            'es': 'ê ésse'
        }
        
        # Separar por pontos
        parts = domain_part.split('.')
        result_parts = []
        
        for part in parts:
            if part.lower() in tld_map:
                result_parts.append(tld_map[part.lower()])
            else:
                # Para nomes de domínio, manter como está mas separar hífens
                clean_part = part.replace('-', ' hífen ')
                result_parts.append(clean_part)
        
        return ' ponto '.join(result_parts)
    
    def convert_path(path):
        """Converte caminhos de URL para forma falada"""
        if not path or path == '/':
            return ''
        
        # Remover barra inicial
        path = path.lstrip('/')
        
        # Substituir caracteres especiais
        path = path.replace('/', ' barra ')
        path = path.replace('?', ' interrogação ')
        path = path.replace('&', ' e comercial ')
        path = path.replace('=', ' igual ')
        path = path.replace('#', ' sustenido ')
        path = path.replace('%', ' por cento ')
        path = path.replace('-', ' hífen ')
        path = path.replace('_', ' sublinhado ')
        
        return ' ' + path if path else ''
    
    def replace_full_url(match):
        """Substitui URLs completas (com protocolo)"""
        full_url = match.group(0)
        domain = match.group(1) if match.group(1) else ''
        path = match.group(2) if match.group(2) else ''
        
        # Extrair protocolo
        protocol = 'https' if full_url.lower().startswith('https') else 'http'
        protocol_text = convert_protocol(protocol)
        
        # Verificar se tem www
        www_text = ''
        if 'www.' in full_url.lower():
            www_text = convert_www() + ' ponto '
        
        domain_text = convert_domain_part(domain)
        path_text = convert_path(path)
        
        return f"{protocol_text} dois pontos barra barra {www_text}{domain_text}{path_text}"
    
    def replace_www_url(match):
        """Substitui URLs que começam com www"""
        domain = match.group(1)
        path = match.group(2) if match.group(2) else ''
        
        www_text = convert_www() + ' ponto '
        domain_text = convert_domain_part(domain)
        path_text = convert_path(path)
        
        return f"{www_text}{domain_text}{path_text}"
    
    def replace_email(match):
        """Substitui endereços de email"""
        email = match.group(0)
        local, domain = email.split('@')
        
        # Limpar caracteres especiais do local
        local = local.replace('.', ' ponto ')
        local = local.replace('_', ' sublinhado ')
        local = local.replace('-', ' hífen ')
        local = local.replace('+', ' mais ')
        
        domain_text = convert_domain_part(domain)
        
        return f"{local} arroba {domain_text}"
    
    def replace_domain(match):
        """Substitui domínios simples"""
        domain = match.group(1)
        return convert_domain_part(domain)
    
    # Aplicar substituições em ordem de prioridade
    # 1. URLs completas (têm prioridade sobre outros padrões)
    text = re.sub(url_pattern, replace_full_url, text, flags=re.IGNORECASE)
    
    # 2. URLs com www (que não foram capturadas acima)
    text = re.sub(www_pattern, replace_www_url, text, flags=re.IGNORECASE)
    
    # 3. Emails
    text = re.sub(email_pattern, replace_email, text)
    
    # 4. Domínios simples (menor prioridade para evitar falsos positivos)
    text = re.sub(domain_pattern, replace_domain, text, flags=re.IGNORECASE)
    
    return text

def normalize_text(text: str) -> str:
    """
    Aplica todas as normalizações ao texto de entrada:
    1. Normaliza valores de moeda
    2. Normaliza datas
    3. Normaliza sequências numéricas (CPF, etc.)
    4. Normaliza horários
    5. Normaliza URLs e emails
    6. Converte números para extenso
    7. Remove caracteres não alfanuméricos
    """
    if not text or not text.strip():
        return text
    
    # Aplicar normalizações em ordem
    normalized = text
    
    # 1. Normalizar moeda primeiro (antes de normalizar números)
    normalized = normalize_currency(normalized)
    
    # 2. Normalizar datas (antes de normalizar números)
    normalized = normalize_dates(normalized)
    
    # 3. Normalizar sequências numéricas (antes de normalizar números simples)
    normalized = normalize_numeric_sequences(normalized)
    
    # 4. Normalizar horários (antes de normalizar números)
    normalized = normalize_time(normalized)
    
    # 5. Normalizar URLs e emails (antes de normalizar números)
    normalized = normalize_urls(normalized)
    
    # 6. Normalizar números
    normalized = normalize_numbers(normalized)
    
    # 7. Limpar caracteres não alfanuméricos
    normalized = remove_non_alphanumeric(normalized)
    
    return normalized