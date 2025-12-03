import pandas as pd
from pathlib import Path

RAW_SALES = Path("data/raw/sales_history.csv")
CLEAN_SALES = Path("data/clean/sales_history.csv")
LEADS = Path("data/clean/leads.csv")

CLEAN_SALES.parent.mkdir(parents=True, exist_ok=True)

def clean_sales_history():
    # 1. Carregar leads e remover duplicatas por cliente
    leads_df = pd.read_csv(LEADS).drop_duplicates(subset=["client"])
    
    # 2. Carregar histórico bruto
    sales_df = pd.read_csv(RAW_SALES)

    # 3. Renomear colunas para inglês
    sales_df.rename(columns={
        "cliente": "client",
        "valor_contrato": "contract_value",
        "duracao_negociacao_dias": "negotiation_duration_days",
        "interacoes": "interactions",
        "sentimento_medio": "average_sentiment",
        "status": "status"
    }, inplace=True)

    # 4. Padronizar nomes de cliente (agora a coluna já existe)
    sales_df["client"] = sales_df["client"].str.strip().str.lower()
    leads_df["client"] = leads_df["client"].str.strip().str.lower()

    # 5. Traduzir sentimentos
    sentiment_map = {"positivo": "positive", "neutro": "neutral", "negativo": "negative"}
    sales_df["average_sentiment"] = sales_df["average_sentiment"].map(sentiment_map)

    # 6. Traduzir status
    status_map = {"ganho": "won", "perdido": "lost"}
    sales_df["status"] = sales_df["status"].map(status_map)

    # 7. Vincular lead_id pelo cliente
    sales_df = sales_df.merge(
        leads_df[["id", "client"]],
        left_on="client",
        right_on="client",
        how="left"
    )

    # 8. Renomear colunas de id
    sales_df.rename(columns={"id_x": "id", "id_y": "lead_id"}, inplace=True)

    # 9. Remover coluna auxiliar
    sales_df.drop(columns=["client"], inplace=True)

    # 10. Remover duplicatas
    sales_df.drop_duplicates(inplace=True)

    # 11. Salvar CSV limpo
    sales_df.to_csv(CLEAN_SALES, index=False)
    print(f"Arquivo limpo salvo em: {CLEAN_SALES}")

if __name__ == "__main__":
    clean_sales_history()
