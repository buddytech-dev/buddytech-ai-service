import pandas as pd

emails = pd.read_csv('results_sentiment_emails.csv')
meetings = pd.read_csv('results_sentiment_meetings.csv')
nba = pd.read_csv('results_next_best_action.csv')
xgb = pd.read_csv('results_xgboost.csv')
log = pd.read_csv('results_logistic.csv')

print("="*60)
print("📊 RESUMO DOS RESULTADOS - BuddyTech AI Service")
print("="*60)

print("\n📧 SENTIMENTO EMAILS:")
print(emails['label'].value_counts())
for label in ['positive', 'neutral', 'negative']:
    count = (emails['label'] == label).sum()
    pct = count/len(emails)*100 if len(emails) > 0 else 0
    print(f"  • {label.upper()}: {count} ({pct:.0f}%)")

print("\n📞 SENTIMENTO MEETINGS:")
print(meetings['label'].value_counts())
for label in ['positive', 'neutral', 'negative']:
    count = (meetings['label'] == label).sum()
    pct = count/len(meetings)*100 if len(meetings) > 0 else 0
    print(f"  • {label.upper()}: {count} ({pct:.0f}%)")

print("\n🎯 PRÓXIMA MELHOR AÇÃO:")
action_counts = nba['next_best_action'].value_counts()
for action, count in action_counts.items():
    print(f"  • {action}: {count}")

print("\n📈 SCORES DE VITÓRIA (LOGISTIC):")
print(f"  • Média: {log['predicted_prob_won'].mean():.2%}")
print(f"  • Mínimo: {log['predicted_prob_won'].min():.2%}")
print(f"  • Máximo: {log['predicted_prob_won'].max():.2%}")

print("\n📈 SCORES DE VITÓRIA (XGBOOST):")
print(f"  • Média: {xgb['predicted_prob_won'].mean():.2%}")
print(f"  • Mínimo: {xgb['predicted_prob_won'].min():.2%}")
print(f"  • Máximo: {xgb['predicted_prob_won'].max():.2%}")

print("\n✅ ANÁLISE CONCLUÍDA!")
print("="*60)
