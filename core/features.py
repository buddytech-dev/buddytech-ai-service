import pandas as pd
import numpy as np

# Mapeamento de sentimentos para valores numéricos
SENTIMENT_MAP = {"positive": 1, "neutral": 0, "negative": -1}
SENTIMENT_LABELS = {-1: "negative", 0: "neutral", 1: "positive"}

def days_since_last(series: pd.Series) -> pd.Series:
    # Converte para datetime com timezone UTC (tz-aware)
    ts = pd.to_datetime(series, errors="coerce", utc=True)
    # Agora também em UTC e tz-aware
    now_utc = pd.Timestamp.now(tz="UTC")
    delta = now_utc - ts
    return delta.dt.days.astype(float)  # type: ignore

def map_sentiment(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Adiciona coluna numérica de sentimento"""
    df["sentiment_num"] = df[col].map(SENTIMENT_MAP)
    return df

def aggregate_sentiment_counts(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    """Conta ocorrências de cada tipo de sentimento por lead_id"""
    counts = df.groupby("lead_id")["sentiment_num"].value_counts().unstack().fillna(0)
    # renomear colunas para legibilidade
    new_cols = {}
    for c in counts.columns:
        label = SENTIMENT_LABELS.get(int(c), str(c))
        new_cols[c] = f"{prefix}_sent_{label}"
    counts = counts.rename(columns=new_cols)
    return counts

def build_dataset(leads_path, emails_path, meetings_path, sales_path, companies_path=None):
    # Carregar dados
    leads = pd.read_csv(leads_path)
    emails = pd.read_csv(emails_path)
    meetings = pd.read_csv(meetings_path)
    sales = pd.read_csv(sales_path)
    companies = pd.read_csv(companies_path) if companies_path else None

    # Target supervisionado (won/lost)
    y = leads[["id", "status"]].copy()
    y["won"] = (y["status"].str.lower() == "won").astype(int)
    y = y[y["status"].str.lower().isin(["won", "lost"])]
    y = y.rename(columns={"id": "lead_id"})[["lead_id", "won"]]

    # Base de features
    X = leads.loc[:, ["id", "last_interaction", "status", "company_id"]].copy()
    X = X.rename(columns={"id": "lead_id"})  # type: ignore
    X["days_since_last"] = days_since_last(X["last_interaction"])
    X["status"] = X["status"].str.lower()

    # Sentimento médio (emails + reuniões)
    emails = map_sentiment(emails, "sentiment")
    meetings = map_sentiment(meetings, "sentiment")

    e_mean = emails.groupby("lead_id")["sentiment_num"].mean()  # Series
    m_mean = meetings.groupby("lead_id")["sentiment_num"].mean()  # Series

    sentiment_mean_series = pd.concat([e_mean, m_mean], axis=1).mean(axis=1)
    sentiment = pd.DataFrame({"sentiment_mean": sentiment_mean_series})

    # Último sentimento (considerando data mais recente de email ou reunião)
    emails_last = emails.sort_values("date").groupby("lead_id").tail(1).set_index("lead_id")["sentiment_num"]
    meetings_last = meetings.sort_values("date").groupby("lead_id").tail(1).set_index("lead_id")["sentiment_num"]
    # usar combine_first para evitar médias estranhas
    last_sentiment_series = emails_last.combine_first(meetings_last)
    sentiment["last_sentiment"] = last_sentiment_series

    # Contagem de sentimentos (emails e reuniões)
    email_sentiment_counts = aggregate_sentiment_counts(emails, "email")
    meeting_sentiment_counts = aggregate_sentiment_counts(meetings, "meeting")

    # Interações totais (emails + reuniões + histórico de vendas)
    e_cnt = emails.groupby("lead_id").size()  # Series
    m_cnt = meetings.groupby("lead_id").size()  # Series
    s_cnt = sales.groupby("lead_id")["interactions"].sum()  # Series
    inter_sum_series = pd.concat([e_cnt, m_cnt, s_cnt], axis=1).fillna(0).sum(axis=1)
    interactions = pd.DataFrame({"interactions_total": inter_sum_series.astype(int)})  # type: ignore

    # Contrato e duração (máximo e média)
    s_agg = sales.groupby("lead_id")[["contract_value", "negotiation_duration_days"]].max()
    s_mean = sales.groupby("lead_id")[["contract_value", "negotiation_duration_days", "interactions"]].mean()
    s_mean.columns = [f"{c}_mean" for c in s_mean.columns]

    # Empresa normalizada (se disponível)
    if companies is not None:
        company_norm = leads[["id", "company_id"]].merge(companies, on="company_id", how="left")
        company_norm = company_norm.set_index("id")[["client_normalized"]]
        X = X.set_index("lead_id").join(company_norm).reset_index()
        # One-hot encoding do setor
        X = pd.get_dummies(X, columns=["client_normalized"], prefix="sector")

    # Merge final (todos em index lead_id)
    X = (
        X.set_index("lead_id")
        .join(sentiment)
        .join(interactions)
        .join(s_agg)
        .join(s_mean)
        .join(email_sentiment_counts)
        .join(meeting_sentiment_counts)
        .reset_index()
    )

    # Preencher faltas e garantir tipos numéricos
    fill_map = {
        "sentiment_mean": 0.0,
        "last_sentiment": 0.0,
        "interactions_total": 0,
        "contract_value": 0.0,
        "negotiation_duration_days": 0.0,
        "contract_value_mean": 0.0,
        "negotiation_duration_days_mean": 0.0,
        "interactions_mean": 0.0,
    }
    X = X.fillna(fill_map)

    # Dataset de treino
    train_df = X.merge(y, on="lead_id", how="inner")

    # Remover colunas não usadas como features
    drop_cols = {"lead_id", "last_interaction", "status", "won", "company_id"}

    # Features finais = todas menos os identificadores
    feature_cols = [c for c in X.columns if c not in drop_cols]

    # Garantir que todas as features sejam numéricas
    for col in feature_cols:
        if X[col].dtype == "object":
            X[col] = pd.to_numeric(X[col], errors="coerce").fillna(0)  # type: ignore

    return X, train_df, feature_cols
