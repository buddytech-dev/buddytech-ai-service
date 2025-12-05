import os
import json
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

# 1. Carrega a API Key do arquivo .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("ERRO: API Key não encontrada no arquivo .env")

# 2. Configura o Gemini
genai.configure(api_key=api_key)

# Usamos o 'gemini-1.5-flash' que é rápido e otimizado para tarefas de alto volume
model = genai.GenerativeModel(
    'gemini-2.5-flash', # Use este nome mais recente
    generation_config={"response_mime_type": "application/json"}
)

app = FastAPI(title="Sales Buddy AI Microservice")

# --- Mapeamento dos Dados que vêm do C# ---
class InteractionInput(BaseModel):
    date: str
    type: str     # Ex: "Email", "WhatsApp"
    content: str  # O texto da conversa

class LeadContextInput(BaseModel):
    industry: str
    revenue_range: int
    current_stage: str # Ex: "Novo", "Negociação"
    interactions: List[InteractionInput]

# --- Mapeamento da Resposta (Para documentação) ---
class AnalysisResponse(BaseModel):
    score: int
    notes: str
    next_step_type: int # 0=Email, 1=Call, 2=Meeting, etc.

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_lead(data: LeadContextInput):
    try:
        # 3. Formata o histórico de conversa para a IA ler
        history_text = ""
        for i in data.interactions:
            history_text += f"- [{i.date}] ({i.type}): {i.content}\n"

        if not history_text:
            history_text = "Nenhuma interação anterior registrada."

        # 4. O Prompt (A "alma" da IA)
        prompt = f"""
        Você é um estrategista de vendas B2B experiente (Sales Buddy).
        
        DADOS DA EMPRESA (LEAD):
        - Indústria: {data.industry}
        - Receita Estimada: {data.revenue_range}
        - Estágio Atual no CRM: {data.current_stage}

        HISTÓRICO DE INTERAÇÕES:
        {history_text}

        TAREFA:
        Analise o sentimento e a probabilidade de fechamento.
        Gere um JSON com os seguintes campos:
        1. "score": Um número inteiro de 0 a 100 indicando a temperatura do lead.
        2. "notes": Uma frase curta e tática sugerindo o que fazer (máx 150 chars).
        3. "next_step_type": Um ID numérico para a próxima interação sugerida.
           Use esta tabela: 0=Email, 1=Ligação, 2=Reunião, 3=WhatsApp.

        Seja crítico. Se o cliente não responde, baixe o score.
        """

        # 5. Chama o Gemini
        response = model.generate_content(prompt)
        
        # 6. Processa o retorno
        # O Gemini já devolve JSON puro graças à config lá em cima
        result = json.loads(response.text)

        return AnalysisResponse(
            score=result.get("score", 50),
            notes=result.get("notes", "Analisar manualmente."),
            next_step_type=result.get("next_step_type", 0)
        )

    except Exception as e:
        print(f"Erro no processamento: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Roda o servidor na porta 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)