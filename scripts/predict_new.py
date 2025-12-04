# scripts/predict_new.py
import joblib
import pandas as pd
from core.features import build_dataset
from core.suggestions import suggest_next_step   # módulo de próximos passos


def main():
    # Carregar dataset completo (inclui companies.csv para features de setor)
    X, train_df, feature_cols = build_dataset(
        "data/clean/leads.csv",
        "data/clean/emails.csv",
        "data/clean/meetings.csv",
        "data/clean/sales_history.csv",
        "data/clean/companies.csv"
    )

    # Carregar modelos treinados
    log_model = joblib.load("models/logistic_lead_model.pkl")
    xgb_model = joblib.load("models/xgboost_lead_model.pkl")

    # Selecionar leads que ainda não têm rótulo (prospect, negotiating)
    leads_new = X[~X["lead_id"].isin(train_df["lead_id"])].copy()

    # Garantir que não haja NaN nas features
    leads_new[feature_cols] = leads_new[feature_cols].fillna(0)

    # Prever probabilidade de vitória com os dois modelos
    probs_log = log_model.predict_proba(leads_new[feature_cols])[:, 1]
    probs_xgb = xgb_model.predict_proba(leads_new[feature_cols])[:, 1]

    leads_new["Win Probability Logistic (%)"] = (probs_log * 100).round(2)
    leads_new["Win Probability XGBoost (%)"] = (probs_xgb * 100).round(2)

    # Usar last_sentiment se disponível, senão cair para sentiment_mean
    if "last_sentiment" in leads_new.columns:
        sent_col = "last_sentiment"
    else:
        sent_col = "sentiment_mean"

    # Gerar sugestão de próximo passo (usando Logistic como referência principal)
    leads_new["Next Step"] = leads_new.apply(
        lambda r: suggest_next_step(r["Win Probability Logistic (%)"], r.get(sent_col, 0.0)),
        axis=1
    )

    # Ordenar e mostrar ranking
    leads_ranked = leads_new.sort_values(by="Win Probability Logistic (%)", ascending=False)  # type: ignore
    out = leads_ranked[
        ["lead_id", "Win Probability Logistic (%)", "Win Probability XGBoost (%)", sent_col, "Next Step"]
    ].reset_index(drop=True).head(10)

    print("\nRanking de leads novos (com próximos passos):")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
