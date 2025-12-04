# core/suggestions.py
"""
Módulo de sugestões de próximos passos para leads.
Combina probabilidade de vitória + sentimento para gerar recomendações práticas.
"""

def bucket_prob(prob_pct: float) -> str:
    """Classifica probabilidade em faixas: high, medium, low"""
    if prob_pct >= 80: 
        return "high"
    if prob_pct >= 50: 
        return "medium"
    return "low"

def bucket_sent(sent_score: float) -> str:
    """
    Classifica sentimento médio/último em faixas:
    - positivo se >= 0.3
    - negativo se <= -0.3
    - neutro caso contrário
    """
    if sent_score >= 0.3: 
        return "positive"
    if sent_score <= -0.3: 
        return "negative"
    return "neutral"

def suggest_next_step(prob_pct: float, sent_score: float) -> str:
    """
    Gera sugestão de próximo passo com base em probabilidade + sentimento.
    """
    p = bucket_prob(prob_pct)
    s = bucket_sent(sent_score)

    if p == "high" and s == "positive":
        return "Send final proposal and schedule closing call."
    if p == "high" and s == "neutral":
        return "Confirm decision-makers and share a success case."
    if p == "high" and s == "negative":
        return "Address objections directly and offer a tailored discount."

    if p == "medium" and s == "positive":
        return "Invite to a technical demo to accelerate commitment."
    if p == "medium" and s == "neutral":
        return "Schedule alignment meeting and clarify scope."
    if p == "medium" and s == "negative":
        return "Send objection-handling FAQ and propose Q&A call."

    if p == "low" and s == "positive":
        return "Share educational content and nurture with a light touch."
    if p == "low" and s == "neutral":
        return "Qualify further and verify fit before investing time."
    # low + negative
    return "Pause outreach and revisit later with a new angle."
