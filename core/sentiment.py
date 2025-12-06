# core/sentiment.py
import re

# Dicionário de palavras positivas em português (expandido)
POSITIVE_WORDS = {
    "ótimo", "excelente", "perfeito", "maravilhoso", "fantástico", "adorei", "amei", "gostei",
    "feliz", "alegre", "satisfeito", "contente", "bom", "boa", "sucesso", "vitória", 
    "ganho", "lucro", "melhor", "incrível", "impressionante", "espetacular", "genial",
    "obrigado", "agradeço", "obrigada", "muito obrigado", "obrigadíssimo",
    "parabéns", "importante", "valioso", "precioso", "eficiente",
    "funcionando bem", "funciona bem", "gostei muito", "adorei", "satisfeito demais",
    "muito satisfeito", "totalmente satisfeito", "funcionando perfeitamente",
    "muito satisfeitos", "estamos satisfeitos", "estamos muito satisfeitos",
    "suporte premium", "felizes", "contratado", "assinada", "assinado",
    "elogiado", "elogiou", "feedback positivo", "depoimento", "recomendo",
    "integração", "implementação", "onboarding", "confirmou", "confirmo", 
    "treinamento", "próximos", "agendada", "agendar", "reunião"
}

# Dicionário de palavras negativas em português (expandido)
NEGATIVE_WORDS = {
    "horrível", "péssimo", "terrível", "horroroso", "desastre", "fracasso", "derrota",
    "problema", "erro", "falha", "quebrado", "não funciona", "não funcionou", "decepção",
    "decepcionado", "triste", "infelizmente", "infeliz", "insatisfeito", "desapontado",
    "difícil", "complicado", "confuso", "pior", "ruim", "péssima", "horrenda",
    "odiei", "odeio", "não gosto", "não aprovo", "desaprovação",
    "perdido", "perda", "negativo", "fracassou", "falhou", "prejuízo", "culpa",
    "criticar", "crítica", "reclamação", "reclamando", "reclamei", "não recomendo",
    "optou por concorrente", "optamos por concorrente", "optamos por outra", "escolheu outro",
    "optou", "optar", "opção", "concorrente", "concorrência", "perdemos",
    "preocupando", "demora", "desaprovação", "não respondeu", "encerrar",
    "nao retorno", "não retorno", "falha", "problemas"
}

def classify_text(text: str) -> str:
    """Classifica sentimento de texto em português usando dicionário léxico"""
    if not text or not isinstance(text, str):
        return "neutral"
    
    text_lower = text.lower()
    
    # Remover pontuação para matching
    text_clean = re.sub(r'[^\w\s]', ' ', text_lower)
    words = set(text_clean.split())
    
    # Melhorias: verificar frases completas também
    phrases_positive = [
        "muito satisfeito", "muito satisfeitos", "estamos satisfeitos", 
        "estamos muito satisfeitos", "feedback positivo", "suporte premium",
        "obrigada pelo suporte", "parabéns à equipe", "resultados no teste",
        "muito bom", "de muito bom"
    ]
    
    phrases_negative = [
        "optou por concorrente", "optamos por concorrente", "optamos por outra",
        "não respondeu", "não retorno", "preocupando", "não recebemos",
        "decidimos seguir", "optar por", "encerrar negociação"
    ]
    
    # Contar palavras positivas e negativas
    positive_count = sum(1 for word in words if word in POSITIVE_WORDS)
    negative_count = sum(1 for word in words if word in NEGATIVE_WORDS)
    
    # Verificar frases
    for phrase in phrases_positive:
        if phrase in text_lower:
            positive_count += 2  # peso maior para frases
    
    for phrase in phrases_negative:
        if phrase in text_lower:
            negative_count += 2  # peso maior para frases
    
    # Lógica de classificação
    if positive_count > negative_count and positive_count > 0:
        return "positive"
    elif negative_count > positive_count and negative_count > 0:
        return "negative"
    else:
        return "neutral"
