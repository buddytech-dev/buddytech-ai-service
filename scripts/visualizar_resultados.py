import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 10

# Diretório base
base_path = Path(__file__).parent.parent

# Carregar dados
xgb_df = pd.read_csv(base_path / 'results_xgboost.csv')
log_df = pd.read_csv(base_path / 'results_logistic.csv')
nba_df = pd.read_csv(base_path / 'results_next_best_action.csv')
sent_emails = pd.read_csv(base_path / 'results_sentiment_emails.csv')
sent_meetings = pd.read_csv(base_path / 'results_sentiment_meetings.csv')

# Criar figura com subplots
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Título principal
fig.suptitle('BuddyTech AI Service - Análise de Resultados', fontsize=18, fontweight='bold', y=0.98)

# 1. XGBoost - Distribuição de probabilidades
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(xgb_df['predicted_prob_won'], bins=15, color='#2E86AB', edgecolor='black', alpha=0.7)
ax1.set_xlabel('Probabilidade de Vitória', fontweight='bold')
ax1.set_ylabel('Frequência', fontweight='bold')
ax1.set_title('XGBoost - Distribuição de Probabilidades', fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.axvline(xgb_df['predicted_prob_won'].mean(), color='red', linestyle='--', linewidth=2, label=f'Média: {xgb_df["predicted_prob_won"].mean():.1%}')
ax1.legend()

# 2. Logística - Distribuição de probabilidades
ax2 = fig.add_subplot(gs[0, 1])
ax2.hist(log_df['predicted_prob_won'], bins=15, color='#A23B72', edgecolor='black', alpha=0.7)
ax2.set_xlabel('Probabilidade de Vitória', fontweight='bold')
ax2.set_ylabel('Frequência', fontweight='bold')
ax2.set_title('Regressão Logística - Distribuição', fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.axvline(log_df['predicted_prob_won'].mean(), color='red', linestyle='--', linewidth=2, label=f'Média: {log_df["predicted_prob_won"].mean():.1%}')
ax2.legend()

# 3. Comparação de Modelos
ax3 = fig.add_subplot(gs[0, 2])
models = ['Logistic', 'XGBoost']
means = [log_df['predicted_prob_won'].mean(), xgb_df['predicted_prob_won'].mean()]
colors_bar = ['#A23B72', '#2E86AB']
bars = ax3.bar(models, means, color=colors_bar, alpha=0.7, edgecolor='black', linewidth=2)
ax3.set_ylabel('Prob. Média de Vitória', fontweight='bold')
ax3.set_title('Comparação entre Modelos', fontweight='bold')
ax3.set_ylim(0, 1)
ax3.grid(True, alpha=0.3, axis='y')
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{means[i]:.1%}', ha='center', va='bottom', fontweight='bold')

# 4. Score Final - Distribuição
ax4 = fig.add_subplot(gs[1, 0])
ax4.hist(nba_df['final_score'], bins=20, color='#F18F01', edgecolor='black', alpha=0.7)
ax4.set_xlabel('Score Final', fontweight='bold')
ax4.set_ylabel('Frequência', fontweight='bold')
ax4.set_title('Score Final - Distribuição', fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.axvline(nba_df['final_score'].mean(), color='red', linestyle='--', linewidth=2, label=f'Média: {nba_df["final_score"].mean():.2f}')
ax4.legend()

# 5. Próxima Melhor Ação - Distribuição
ax5 = fig.add_subplot(gs[1, 1])
action_counts = nba_df['next_best_action'].value_counts()
colors_action = ['#06A77D', '#D62828', '#F77F00']
wedges, texts, autotexts = ax5.pie(action_counts.values, labels=None, autopct='%1.0f%%',
                                     colors=colors_action[:len(action_counts)], startangle=90,
                                     textprops={'fontweight': 'bold', 'fontsize': 10})
ax5.set_title('Próxima Melhor Ação', fontweight='bold')
# Adicionar legenda com nomes abreviados
labels_short = [label[:20] + '...' if len(label) > 20 else label for label in action_counts.index]
ax5.legend(labels_short, loc='upper left', bbox_to_anchor=(1, 1), fontsize=9)

# 6. Sentimento Emails
ax6 = fig.add_subplot(gs[1, 2])
sentiment_counts_email = sent_emails['label'].value_counts()
colors_sentiment = {'positive': '#06A77D', 'neutral': '#FFB703', 'negative': '#D62828'}
email_colors = [colors_sentiment.get(label, '#999999') for label in sentiment_counts_email.index]
wedges, texts, autotexts = ax6.pie(sentiment_counts_email.values, 
                                     labels=sentiment_counts_email.index,
                                     autopct='%1.0f%%',
                                     colors=email_colors,
                                     startangle=90,
                                     textprops={'fontweight': 'bold'})
ax6.set_title('Sentimento - Emails', fontweight='bold')

# 7. Sentimento Meetings
ax7 = fig.add_subplot(gs[2, 0])
sentiment_counts_meet = sent_meetings['label'].value_counts()
meet_colors = [colors_sentiment.get(label, '#999999') for label in sentiment_counts_meet.index]
wedges, texts, autotexts = ax7.pie(sentiment_counts_meet.values, 
                                     labels=sentiment_counts_meet.index,
                                     autopct='%1.0f%%',
                                     colors=meet_colors,
                                     startangle=90,
                                     textprops={'fontweight': 'bold'})
ax7.set_title('Sentimento - Meetings', fontweight='bold')

# 8. Lead Score vs Final Score
ax8 = fig.add_subplot(gs[2, 1])
scatter = ax8.scatter(nba_df['lead_score'], nba_df['final_score'], 
           alpha=0.6, s=100, c=nba_df['final_score'], cmap='RdYlGn', edgecolors='black')
ax8.set_xlabel('Lead Score', fontweight='bold')
ax8.set_ylabel('Final Score', fontweight='bold')
ax8.set_title('Lead Score vs Final Score', fontweight='bold')
ax8.grid(True, alpha=0.3)
z = np.polyfit(nba_df['lead_score'], nba_df['final_score'], 1)
p = np.poly1d(z)
ax8.plot(sorted(nba_df['lead_score']), p(sorted(nba_df['lead_score'])), "r--", alpha=0.8, linewidth=2)
plt.colorbar(scatter, ax=ax8, label='Score')

# 9. Tabela de Resumo
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('tight')
ax9.axis('off')

summary_data = [
    ['Métrica', 'Valor'],
    ['Total de Leads', f'{len(nba_df)}'],
    ['Prob. Média (Log)', f'{log_df["predicted_prob_won"].mean():.1%}'],
    ['Prob. Média (XGB)', f'{xgb_df["predicted_prob_won"].mean():.1%}'],
    ['Score Final Médio', f'{nba_df["final_score"].mean():.3f}'],
    ['Sentimento +', f'{(sent_emails["label"] == "positive").sum() + (sent_meetings["label"] == "positive").sum()}'],
    ['Sentimento -', f'{(sent_emails["label"] == "negative").sum() + (sent_meetings["label"] == "negative").sum()}'],
]

table = ax9.table(cellText=summary_data, cellLoc='center', loc='center',
                 colWidths=[0.6, 0.4])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.5)

# Formatar cabeçalho
for i in range(2):
    table[(0, i)].set_facecolor('#2E86AB')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alternativas de cor nas linhas
for i in range(1, len(summary_data)):
    for j in range(2):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#f0f0f0')

ax9.set_title('Resumo dos Resultados', fontweight='bold', pad=20)

# Salvar figura
plt.savefig(base_path / 'resultados_graficos.png', dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ Gráficos salvos em: {base_path / 'resultados_graficos.png'}")
print("\n📊 Resumo dos Resultados:")
print(f"\n📈 XGBoost:")
print(f"  - Total de leads: {len(xgb_df)}")
print(f"  - Prob. média de ganho: {xgb_df['predicted_prob_won'].mean():.2%}")
print(f"\n📈 Regressão Logística:")
print(f"  - Total de leads: {len(log_df)}")
print(f"  - Prob. média de ganho: {log_df['predicted_prob_won'].mean():.2%}")
print(f"\n📈 Próxima Melhor Ação:")
print(f"  - Total de leads: {len(nba_df)}")
print(f"  - Score final médio: {nba_df['final_score'].mean():.3f}")
print(f"\nDistribuição de ações:")
for action, count in action_counts.items():
    print(f"  - {action}: {count}")
print(f"\n📊 Sentimento Emails: {sentiment_counts_email.to_dict()}")
print(f"📊 Sentimento Meetings: {sentiment_counts_meet.to_dict()}")

plt.show()
