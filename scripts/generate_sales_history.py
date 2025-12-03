import pandas as pd
import random
from pathlib import Path

LEADS = Path("data/clean/leads.csv")
RAW_SALES = Path("data/raw/sales_history.csv")

RAW_SALES.parent.mkdir(parents=True, exist_ok=True)

def generate_sales_history():
    # 1. Carregar leads
    leads_df = pd.read_csv(LEADS)

    # 2. Gerar vendas compatíveis
    sales_records = []
    for idx, row in enumerate(leads_df.itertuples(), start=1):
        sales_records.append({
            "id": idx,
            "cliente": row.client,
            "valor_contrato": random.randint(20000, 120000),
            "duracao_negociacao_dias": random.randint(20, 70),
            "interacoes": random.randint(5, 25),
            "sentimento_medio": random.choice(["positivo", "neutro", "negativo"]),
            "status": row.status
        })

    # 3. Adicionar alguns órfãos (sem lead correspondente)
    orfaos = [
        {"id": len(sales_records) + 1, "cliente": "OrphanCo", "valor_contrato": 45000,
         "duracao_negociacao_dias": 39, "interacoes": 12, "sentimento_medio": "neutro", "status": "lost"},
        {"id": len(sales_records) + 2, "cliente": "ExternalSoft", "valor_contrato": 72000,
         "duracao_negociacao_dias": 51, "interacoes": 16, "sentimento_medio": "positivo", "status": "won"},
        {"id": len(sales_records) + 3, "cliente": "LegacyData", "valor_contrato": 28000,
         "duracao_negociacao_dias": 29, "interacoes": 8, "sentimento_medio": "negativo", "status": "lost"}
    ]
    sales_records.extend(orfaos)

    # 4. Salvar CSV bruto
    sales_df = pd.DataFrame(sales_records)
    sales_df.to_csv(RAW_SALES, index=False)
    print(f"Arquivo bruto gerado em: {RAW_SALES}")

if __name__ == "__main__":
    generate_sales_history()
