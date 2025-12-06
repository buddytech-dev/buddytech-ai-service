#!/usr/bin/env python3
# Script para visualizar resultados em texto e tabelas sem matplotlib

import csv
from pathlib import Path

base_path = Path(__file__).parent.parent

def read_csv(filename):
    with open(base_path / filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Carregar dados
emails = read_csv('results_sentiment_emails.csv')
meetings = read_csv('results_sentiment_meetings.csv')
nba = read_csv('results_next_best_action.csv')
xgb = read_csv('results_xgboost.csv')
log = read_csv('results_logistic.csv')

print("\n" + "="*80)
print("📊 BuddyTech AI Service - RESUMO DETALHADO DOS RESULTADOS")
print("="*80)

# Análise de Sentimentos
print("\n📧 SENTIMENTO NOS EMAILS:")
print("-" * 80)
email_sentiments = {}
for email in emails:
    label = email['label']
    email_sentiments[label] = email_sentiments.get(label, 0) + 1

for label in ['positive', 'neutral', 'negative']:
    count = email_sentiments.get(label, 0)
    pct = (count / len(emails) * 100) if emails else 0
    print(f"  {label.upper():.<30} {count:>3} ({pct:>5.1f}%)")

print("\n📞 SENTIMENTO NAS REUNIÕES (MEETINGS):")
print("-" * 80)
meeting_sentiments = {}
for meeting in meetings:
    label = meeting['label']
    meeting_sentiments[label] = meeting_sentiments.get(label, 0) + 1

for label in ['positive', 'neutral', 'negative']:
    count = meeting_sentiments.get(label, 0)
    pct = (count / len(meetings) * 100) if meetings else 0
    print(f"  {label.upper():.<30} {count:>3} ({pct:>5.1f}%)")

# Análise de Scores
print("\n📈 PROBABILIDADES DE VITÓRIA - REGRESSÃO LOGÍSTICA:")
print("-" * 80)
log_probs = [float(row['predicted_prob_won']) for row in log]
if log_probs:
    print(f"  Probabilidade Mínima....... {min(log_probs):>8.2%}")
    print(f"  Probabilidade Máxima....... {max(log_probs):>8.2%}")
    print(f"  Probabilidade Média........ {sum(log_probs)/len(log_probs):>8.2%}")
    print(f"  Mediana..................... {sorted(log_probs)[len(log_probs)//2]:>8.2%}")

print("\n📈 PROBABILIDADES DE VITÓRIA - XGBOOST:")
print("-" * 80)
xgb_probs = [float(row['predicted_prob_won']) for row in xgb]
if xgb_probs:
    print(f"  Probabilidade Mínima....... {min(xgb_probs):>8.2%}")
    print(f"  Probabilidade Máxima....... {max(xgb_probs):>8.2%}")
    print(f"  Probabilidade Média........ {sum(xgb_probs)/len(xgb_probs):>8.2%}")
    print(f"  Mediana..................... {sorted(xgb_probs)[len(xgb_probs)//2]:>8.2%}")

# Próxima Melhor Ação
print("\n🎯 PRÓXIMA MELHOR AÇÃO (RECOMENDAÇÕES):")
print("-" * 80)
nba_actions = {}
for row in nba:
    action = row['next_best_action']
    nba_actions[action] = nba_actions.get(action, 0) + 1

for action, count in sorted(nba_actions.items(), key=lambda x: x[1], reverse=True):
    pct = (count / len(nba) * 100) if nba else 0
    print(f"  {count:>3} leads - {action} ({pct:>5.1f}%)")

# Score Final
print("\n📊 SCORE FINAL (COMBINADO):")
print("-" * 80)
final_scores = [float(row['final_score']) for row in nba]
if final_scores:
    print(f"  Score Mínimo............... {min(final_scores):>8.3f}")
    print(f"  Score Máximo............... {max(final_scores):>8.3f}")
    print(f"  Score Médio................ {sum(final_scores)/len(final_scores):>8.3f}")
    print(f"  Mediana.................... {sorted(final_scores)[len(final_scores)//2]:>8.3f}")

# Comparação de Modelos
print("\n⚖️  COMPARAÇÃO DE MODELOS:")
print("-" * 80)
log_mean = sum(log_probs) / len(log_probs) if log_probs else 0
xgb_mean = sum(xgb_probs) / len(xgb_probs) if xgb_probs else 0
diff = ((xgb_mean - log_mean) / log_mean * 100) if log_mean > 0 else 0

print(f"  Regressão Logística........ {log_mean:>8.2%}")
print(f"  XGBoost.................... {xgb_mean:>8.2%}")
print(f"  Diferença (XGB vs Log)..... {diff:>8.1f}%")
print(f"  Modelo melhor.............. {'XGBoost' if xgb_mean > log_mean else 'Logística':>8}")

# Resumo Executivo
print("\n" + "="*80)
print("📋 RESUMO EXECUTIVO:")
print("="*80)
print(f"  Total de Leads Analisados....... {len(nba)}")
print(f"  Sentimentos Positivos........... {sum([email_sentiments.get('positive', 0), meeting_sentiments.get('positive', 0)])} ({(sum([email_sentiments.get('positive', 0), meeting_sentiments.get('positive', 0)])/2/len(emails)*100 if emails else 0):.0f}%)")
print(f"  Sentimentos Negativos........... {sum([email_sentiments.get('negative', 0), meeting_sentiments.get('negative', 0)])} ({(sum([email_sentiments.get('negative', 0), meeting_sentiments.get('negative', 0)])/2/len(emails)*100 if emails else 0):.0f}%)")
print(f"  Leads para Proposta/Comercial.. {nba_actions.get('Avançar para proposta/comercial', 0)}")
print(f"  Leads para Follow-up........... {nba_actions.get('Agendar reunião de follow-up', 0)}")
print(f"  Leads para Nutrir/Descartar.... {nba_actions.get('Nutrir com conteúdo ou descartar lead', 0)}")
print("\n" + "="*80)
