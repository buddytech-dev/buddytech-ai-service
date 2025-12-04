import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

def save_response_to_csv(endpoint, filename):
    print(f"\n🔎 Testando {endpoint}...")
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        print("Status:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            print(f"✅ Resultado salvo em {filename}")
        else:
            print("❌ Erro na requisição:", response.text)
    except Exception as e:
        print(f"⚠️ Falha ao testar {endpoint}: {e}")

def test_all():
    save_response_to_csv("/lead-score/logistic", "results_logistic.csv")
    save_response_to_csv("/lead-score/xgboost", "results_xgboost.csv")
    save_response_to_csv("/sentiment/test-emails", "results_sentiment_emails.csv")
    save_response_to_csv("/sentiment/test-meetings", "results_sentiment_meetings.csv")
    save_response_to_csv("/next-best-action", "results_next_best_action.csv")
    save_response_to_csv("/next-best-action/xgboost", "results_next_best_action_xgb.csv")

if __name__ == "__main__":
    test_all()
    