from fastapi import FastAPI, APIRouter
import joblib
import pandas as pd
from pydantic import BaseModel
from core.features import build_dataset
from core.sentiment import classify_text

app = FastAPI()
router = APIRouter()

# Carregar modelos
logistic_model, logistic_features = joblib.load("models/logistic_lead_model.pkl")
xgb_model, xgb_features = joblib.load("models/xgboost_lead_model.pkl")

# Função auxiliar para garantir colunas
def ensure_features(df, features):
    for col in features:
        if col not in df.columns:
            df[col] = 0
    return df

# Endpoint de regressão logística
@app.get("/lead-score/logistic")
def get_logistic_score():
    X, train_df, feature_cols = build_dataset(
        "data/clean/leads.csv",
        "data/clean/emails.csv",
        "data/clean/meetings.csv",
        "data/clean/sales_history.csv",
        "data/clean/companies.csv"
    )
    leads_new = X[~X["lead_id"].isin(train_df["lead_id"])].copy()
    if leads_new.empty:
        return []
    leads_new = ensure_features(leads_new, logistic_features)
    leads_new = leads_new.fillna(0)
    probs = logistic_model.predict_proba(leads_new[logistic_features])[:, 1]
    leads_new["predicted_prob_won"] = probs
    return leads_new[["lead_id", "predicted_prob_won"]].sort_values(
        "predicted_prob_won", ascending=False
    ).to_dict(orient="records")

# Endpoint de XGBoost
@app.get("/lead-score/xgboost")
def get_xgboost_score():
    X, train_df, feature_cols = build_dataset(
        "data/clean/leads.csv",
        "data/clean/emails.csv",
        "data/clean/meetings.csv",
        "data/clean/sales_history.csv",
        "data/clean/companies.csv"
    )
    leads_new = X[~X["lead_id"].isin(train_df["lead_id"])].copy()
    if leads_new.empty:
        return []
    leads_new = ensure_features(leads_new, xgb_features)
    leads_new = leads_new.fillna(0)
    probs = xgb_model.predict_proba(leads_new[xgb_features])[:, 1]
    leads_new["predicted_prob_won"] = probs
    return leads_new[["lead_id", "predicted_prob_won"]].sort_values(
        "predicted_prob_won", ascending=False
    ).to_dict(orient="records")

# Sentiment (VADER)
class TextInput(BaseModel):
    text: str

@app.post("/sentiment")
def analyze_sentiment(input: TextInput):
    label = classify_text(input.text if input.text else "")
    return {"text": input.text, "label": label}

# Next Best Action (Logistic)
@app.get("/next-best-action")
def next_best_action():
    X, train_df, feature_cols = build_dataset(
        "data/clean/leads.csv",
        "data/clean/emails.csv",
        "data/clean/meetings.csv",
        "data/clean/sales_history.csv",
        "data/clean/companies.csv"
    )
    leads_new = X[~X["lead_id"].isin(train_df["lead_id"])].copy()
    if leads_new.empty:
        return []
    leads_new = ensure_features(leads_new, logistic_features)
    leads_new = leads_new.fillna(0)
    probs = logistic_model.predict_proba(leads_new[logistic_features])[:, 1]
    leads_new["predicted_prob_won"] = probs

    return build_actions(leads_new)

# Next Best Action (XGBoost)
@app.get("/next-best-action/xgboost")
def next_best_action_xgb():
    X, train_df, feature_cols = build_dataset(
        "data/clean/leads.csv",
        "data/clean/emails.csv",
        "data/clean/meetings.csv",
        "data/clean/sales_history.csv",
        "data/clean/companies.csv"
    )
    leads_new = X[~X["lead_id"].isin(train_df["lead_id"])].copy()
    if leads_new.empty:
        return []
    leads_new = ensure_features(leads_new, xgb_features)
    leads_new = leads_new.fillna(0)
    probs = xgb_model.predict_proba(leads_new[xgb_features])[:, 1]
    leads_new["predicted_prob_won"] = probs

    return build_actions(leads_new)

# Função auxiliar para construir ações
def build_actions(leads_new):
    actions = []
    emails = pd.read_csv("data/clean/emails.csv").fillna("")
    meetings = pd.read_csv("data/clean/meetings.csv").fillna("")

    for _, row in leads_new.iterrows():
        score = row["predicted_prob_won"]

        # corrigido: usar colunas certas
        lead_emails = emails[emails["lead_id"] == row["lead_id"]]["content"].tail(3)
        lead_meetings = meetings[meetings["lead_id"] == row["lead_id"]]["discussion_points"].tail(3)
        texts = list(lead_emails) + list(lead_meetings)

        sentiments = [classify_text(t) for t in texts if isinstance(t, str) and t.strip()]
        sentiment = max(set(sentiments), key=sentiments.count) if sentiments else "neutral"
        sentiment_value = {"positive": 1.0, "neutral": 0.5, "negative": 0.0}[sentiment]

        final_score = (0.7 * score) + (0.3 * sentiment_value)

        if final_score >= 0.75:
            action = "Avançar para proposta/comercial"
        elif 0.5 <= final_score < 0.75:
            action = "Agendar reunião de follow-up"
        else:
            action = "Nutrir com conteúdo ou descartar lead"

        actions.append({
            "lead_id": row["lead_id"],
            "lead_score": round(score, 3),
            "sentiment": sentiment,
            "final_score": round(final_score, 3),
            "next_best_action": action
        })

    return actions

# Testes nos emails e reuniões
@router.get("/sentiment/test-emails")
def test_emails():
    emails = pd.read_csv("data/clean/emails.csv").fillna("")
    return [{"text": text, "label": classify_text(text)} for text in emails["content"].head(5) if text]

@router.get("/sentiment/test-meetings")
def test_meetings():
    meetings = pd.read_csv("data/clean/meetings.csv").fillna("")
    return [{"text": text, "label": classify_text(text)} for text in meetings["discussion_points"].head(5) if text]

app.include_router(router)
