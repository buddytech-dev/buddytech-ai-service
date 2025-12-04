import os
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
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

    # Features e target
    X_all = train_df[feature_cols]
    y_all = train_df["won"]

    # Garantir que não haja NaN
    X_all = X_all.fillna(0)
    
    # ------------------------------
    #  Escolha o modo de treino
    MODE = "full"   # opções: "split", "full", "scaled"
    # ------------------------------

    if MODE == "split":
        # Modo 1: treino/teste com split (ex.: 50/50)
        X_tr, X_te, y_tr, y_te = train_test_split(
            X_all, y_all, test_size=0.5, random_state=42, stratify=y_all
        )
        X_tr = X_tr.fillna(0)
        X_te = X_te.fillna(0)
        
        model = LogisticRegression(max_iter=1000)
        model.fit(X_tr, y_tr)

        y_pred = model.predict(X_te)
        print("Confusion Matrix:\n", confusion_matrix(y_te, y_pred))
        print("\nClassification Report:\n", classification_report(y_te, y_pred))

    elif MODE == "full":
        # Modo 2: treino com todos os dados rotulados
        model = LogisticRegression(max_iter=1000)
        model.fit(X_all, y_all)

        y_pred = model.predict(X_all)
        print("Confusion Matrix (treino completo):\n", confusion_matrix(y_all, y_pred))
        print("\nClassification Report (treino completo):\n", classification_report(y_all, y_pred))

    elif MODE == "scaled":
        # Modo 3: treino/teste com normalização (StandardScaler)
        X_tr, X_te, y_tr, y_te = train_test_split(
            X_all, y_all, test_size=0.3, random_state=42, stratify=y_all
        )
        scaler = StandardScaler()
        X_tr_scaled = scaler.fit_transform(X_tr.fillna(0))
        X_te_scaled = scaler.transform(X_te.fillna(0))

        model = LogisticRegression(max_iter=1000)
        model.fit(X_tr_scaled, y_tr)

        y_pred = model.predict(X_te_scaled)
        print("Confusion Matrix (scaled):\n", confusion_matrix(y_te, y_pred))
        print("\nClassification Report (scaled):\n", classification_report(y_te, y_pred))

        # Previsão em todo dataset com scaler
        train_df["predicted_won"] = model.predict(scaler.transform(X_all))
    else:
        raise ValueError("Modo inválido. Use 'split', 'full' ou 'scaled'.")

    # Salvar modelo treinado
    joblib.dump((model, feature_cols),"models/logistic_lead_model.pkl")
    print("\nModelo salvo em models/logistic_lead_model.pkl")

if __name__ == "__main__":
    main()
