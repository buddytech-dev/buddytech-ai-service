import os
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from core.features import build_dataset

def main():
    # Carregar dataset
    X, train_df, feature_cols = build_dataset(
        "data/clean/leads.csv",
        "data/clean/emails.csv",
        "data/clean/meetings.csv",
        "data/clean/sales_history.csv", 
        "data/clean/companies.csv"
    )

    X_train = train_df[feature_cols]
    y_train = train_df["won"]

    # Split treino/teste
    X_tr, X_te, y_tr, y_te = train_test_split(
        X_train, y_train, test_size=0.3, random_state=42, stratify=y_train
    )

    # Modelo XGBoost
    model = XGBClassifier(
        use_label_encoder=False,
        eval_metric="logloss",
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1
    )
    model.fit(X_tr, y_tr)

    # Avaliação
    y_pred = model.predict(X_te)
    print("=== Confusion Matrix ===")
    print(confusion_matrix(y_te, y_pred))
    print("\n=== Classification Report ===")
    print(classification_report(y_te, y_pred))

    # Salvar modelo + features
    os.makedirs("models", exist_ok=True)
    joblib.dump((model, feature_cols), "models/xgboost_lead_model.pkl")
    print("\n✅ Modelo XGBoost salvo em models/xgboost_lead_model.pkl")

    # Validação rápida do salvamento
    loaded_model, loaded_features = joblib.load("models/xgboost_lead_model.pkl")
    print(f"\nModelo carregado: {type(loaded_model)}")
    print(f"Total de features salvas: {len(loaded_features)}")

if __name__ == "__main__":
    main()
