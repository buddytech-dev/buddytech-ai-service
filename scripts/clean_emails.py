import pandas as pd
import re
from pathlib import Path

RAW_EMAILS = Path("data/raw/emails.csv")
CLEAN_EMAILS = Path("data/clean/emails.csv")
LEADS = Path("data/clean/leads.csv")

CLEAN_EMAILS.parent.mkdir(parents=True, exist_ok=True)

def clean_emails():
    # 1. Carregar leads limpos e remover duplicatas de email
    leads_df = pd.read_csv(LEADS)
    leads_df = leads_df.drop_duplicates(subset=["email"])

    # 2. Carregar emails brutos
    emails_df = pd.read_csv(RAW_EMAILS)

    # 3. Padronizar remetente/destinatário
    emails_df["remetente"] = emails_df["remetente"].str.strip()
    emails_df["destinatario"] = emails_df["destinatario"].str.strip()

    # 4. Validar formato de email
    regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    emails_df = emails_df[emails_df["remetente"].str.match(regex)]
    emails_df = emails_df[emails_df["destinatario"].str.match(regex)]

    # 5. Padronizar assunto/corpo
    emails_df["assunto"] = emails_df["assunto"].str.strip().str.capitalize()
    emails_df["corpo"] = emails_df["corpo"].str.strip()

    # 6. Converter data_envio
    emails_df["data_envio"] = pd.to_datetime(emails_df["data_envio"], errors="coerce")

    # 7. Traduzir sentimento
    sentiment_map = {
        "positivo": "positive",
        "neutro": "neutral",
        "negativo": "negative"
    }
    emails_df["sentimento"] = emails_df["sentimento"].map(sentiment_map)

    # 8. Cruzar com leads pelo email do remetente
    emails_df = emails_df.merge(
        leads_df[["id", "email"]],
        left_on="remetente",
        right_on="email",
        how="left"
    )

    # 9. Renomear colunas de id
    emails_df.rename(columns={"id_x": "id", "id_y": "lead_id"}, inplace=True)

    # 10. Remover coluna auxiliar 'email' (veio do leads)
    emails_df.drop(columns=["email"], inplace=True)

    # 11. Remover duplicados
    emails_df = emails_df.drop_duplicates(subset=["remetente","destinatario","assunto","data_envio"])

    # 12. Traduzir nomes das colunas para inglês
    emails_df.rename(columns={
        "remetente": "sender",
        "destinatario": "recipient",
        "assunto": "subject",
        "corpo": "content",
        "data_envio": "date",
        "sentimento": "sentiment"
    }, inplace=True)

    # 13. Salvar CSV limpo
    emails_df.to_csv(CLEAN_EMAILS, index=False)
    print(f"Arquivo limpo salvo em: {CLEAN_EMAILS}")

if __name__ == "__main__":
    clean_emails()
