import pandas as pd
import re
import uuid
import unicodedata
from pathlib import Path

# Caminhos
RAW_PATH = Path("data/raw/leads.csv")
CLEAN_DIR = Path("data/clean")
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

LEADS_OUT = CLEAN_DIR / "leads.csv"
COMPANIES_OUT = CLEAN_DIR / "companies.csv"

# --------------------
# Helpers
# --------------------

def remove_accents(text: str) -> str:
    if pd.isna(text):
        return text
    return ''.join(ch for ch in unicodedata.normalize('NFD', str(text))
                   if unicodedata.category(ch) != 'Mn')

def normalize_company_name(name: str) -> str:
    if pd.isna(name):
        return ""
    n = remove_accents(name).lower().strip()
    suffixes = [
        " ltda", " ltd.", " s.a.", " sa", " me", " eireli", " ei", " llc", " inc", " empresa jr",
        " soluções", " solutions"
    ]
    for s in suffixes:
        if n.endswith(s):
            n = n[: -len(s)]
    n = re.sub(r"[^\w\s]", " ", n)
    n = re.sub(r"\s+", " ", n).strip()
    return n

def company_id_from_name(name: str) -> str:
    norm = normalize_company_name(name)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, norm))

def normalize_phone_br(phone: str) -> str:
    digits = re.sub(r"\D", "", str(phone or ""))
    if not digits:
        return ""
    if digits.startswith("55"):
        rest = digits[2:]
        if 10 <= len(rest) <= 11:
            return "+55" + rest
        if len(rest) > 11:
            return "+55" + rest[-11:]
        return "+55" + rest
    if len(digits) in (10, 11):
        return "+55" + digits
    if len(digits) > 11:
        return "+55" + digits[-11:]
    return "+55" + digits.zfill(11)

# --------------------
# Limpeza principal
# --------------------

def clean_leads():
    # 1. Leitura
    df = pd.read_csv(RAW_PATH)

    # 2. Status para inglês
    status_map = {
        "Em negociação": "negotiating",
        "Fechado": "won",
        "Prospect": "prospect",
        "Perdido": "lost"
    }
    df["status"] = df["status"].map(status_map)

    # 3. Telefone
    df["telefone"] = df["telefone"].apply(normalize_phone_br)

    # 4. Datas
    df["ultima_interacao"] = pd.to_datetime(df["ultima_interacao"], errors="coerce")

    # 5. Cliente e contato
    df["cliente"] = df["cliente"].astype(str).str.strip()
    df["contato"] = df["contato"].astype(str).str.strip()
    df["cliente"] = df["cliente"].str.title()
    df["contato"] = df["contato"].str.title()

    # 6. E-mails
    df["email"] = df["email"].astype(str).str.strip().str.replace(" ", "")
    regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    df = df[df["email"].str.match(regex)]

    # 7. Notas
    df["notas"] = df["notas"].astype(str).str.strip()
    df["notas"] = df["notas"].str[:1].str.upper() + df["notas"].str[1:]

    # 8. company_id estável por empresa
    df["company_id"] = df["cliente"].apply(company_id_from_name)

    # 9. Remover duplicados exatos
    df.drop_duplicates(inplace=True)

    # 10. Traduzir nomes das colunas para inglês
    col_map = {
    "cliente": "client",
    "contato": "contact",
    "email": "email",
    "telefone": "phone",
    "status": "status",
    "ultima_interacao": "last_interaction",
    "notas": "notes"
    }
    
    df = df.rename(columns=col_map)  #type: ignore

    # 11. Salvar CRM limpo
    df.to_csv(LEADS_OUT, index=False)

    # 12. Salvar dicionário de empresas (companies.csv)
    companies = (
        df[["company_id", "client"]]
        .drop_duplicates()
        .rename(columns={"client": "client_display"})
    )
    companies["client_normalized"] = companies["client_display"].apply(normalize_company_name)
    companies.to_csv(COMPANIES_OUT, index=False)

    print(f"Leads limpo: {LEADS_OUT}")
    print(f"Dicionário de empresas: {COMPANIES_OUT}")

if __name__ == "__main__":
    clean_leads()
