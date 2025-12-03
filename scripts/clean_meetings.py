import pandas as pd
from pathlib import Path

RAW_MEETINGS = Path("data/raw/meetings.csv")
CLEAN_MEETINGS = Path("data/clean/meetings.csv")
LEADS = Path("data/clean/leads.csv")

CLEAN_MEETINGS.parent.mkdir(parents=True, exist_ok=True)

def clean_meetings():
    # 1. Carregar leads e remover duplicatas
    leads_df = pd.read_csv(LEADS).drop_duplicates(subset=["contact"])
    
    # 2. Carregar reuniões brutas
    meetings_df = pd.read_csv(RAW_MEETINGS)

    # 3. Padronizar textos
    meetings_df["titulo"] = meetings_df["titulo"].str.strip().str.capitalize()
    meetings_df["pontos_discutidos"] = meetings_df["pontos_discutidos"].str.strip()
    meetings_df["acoes"] = meetings_df["acoes"].str.strip()

    # 4. Converter data
    meetings_df["data"] = pd.to_datetime(meetings_df["data"], errors="coerce")

    # 5. Traduzir sentimento
    sentiment_map = {
        "positivo": "positive",
        "neutro": "neutral",
        "negativo": "negative"
    }
    meetings_df["sentimento"] = meetings_df["sentimento"].map(sentiment_map)

    # 6. Extrair contato principal (primeiro participante antes do ;)
    meetings_df["contato_principal"] = meetings_df["participantes"].str.split(";").str[0].str.strip()

    # 7. Vincular lead_id pelo contato
    meetings_df = meetings_df.merge(
        leads_df[["id", "contact"]],
        left_on="contato_principal",
        right_on="contact",
        how="left"
    )

    # 8. Renomear colunas de id
    meetings_df.rename(columns={"id_x": "id", "id_y": "lead_id"}, inplace=True)

    # 9. Remover coluna auxiliar 'contato'
    meetings_df.drop(columns=["contact"], inplace=True)

    # 10. Remover duplicatas
    meetings_df.drop_duplicates(inplace=True)

    # 11. Traduzir nomes das colunas para inglês
    col_map = {
        "titulo": "title",
        "participantes": "participants",
        "data": "date",
        "pontos_discutidos": "discussion_points",
        "acoes": "actions",
        "sentimento": "sentiment",
        "contato_principal": "main_contact"
    }
    meetings_df = meetings_df.rename(columns=col_map)

    # 12. Salvar CSV limpo
    meetings_df.to_csv(CLEAN_MEETINGS, index=False)
    print(f"Arquivo limpo salvo em: {CLEAN_MEETINGS}")

if __name__ == "__main__":
    clean_meetings()
