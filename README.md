🤖 Sales Buddy AI — Microservice

Microsserviço de Inteligência Artificial desenvolvido em Python com FastAPI.
Ele funciona como o motor cognitivo do CRM, analisando interações com clientes e gerando insights táticos usando o Google Gemini.

🚀 Funcionalidades

Lead Scoring: calcula a temperatura (0–100) com base no histórico do lead.

Análise de Sentimento: interpreta e-mails, mensagens e anotações.

Sugestão de Próximos Passos: define a ação ideal (Email, Ligação, Reunião ou WhatsApp).

Resposta Estruturada: sempre retorna JSON limpo e padronizado (response_mime_type: application/json).

🛠️ Tech Stack

Linguagem: Python 3.9+

Framework Web: FastAPI

Servidor: Uvicorn

Modelo de IA: Google Gemini (google-generativeai)

Validação: Pydantic

Ambiente: dotenv (.env)

⚙️ Configuração e Instalação
1. Clonar o repositório
git clone https://github.com/seu-usuario/sales-buddy-ai.git
cd sales-buddy-ai

2. Criar ambiente virtual (opcional, recomendado)
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

3. Instalar dependências

Crie um arquivo requirements.txt com:

fastapi
uvicorn
google-generativeai
python-dotenv
pydantic


Instale tudo:

pip install -r requirements.txt

4. Criar o arquivo .env

Crie um arquivo .env na raíz:

GEMINI_API_KEY=sua_chave_aqui


⚠️ Nunca commite este arquivo no Git!

▶️ Como Rodar

Iniciar o servidor:

python main.py


Ou usando Uvicorn (com hot reload):

uvicorn main:app --reload


O serviço ficará disponível em:

http://localhost:8000

📚 Documentação da API

FastAPI gera documentação automaticamente:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

🔎 Endpoint Principal
POST /analyze

É o endpoint consumido pelo backend em C#.

📥 Exemplo de Request
{
  "industry": "Tecnologia",
  "revenue_range": 500000,
  "current_stage": "Negociação",
  "interactions": [
    {
      "date": "2024-10-05",
      "type": "Email",
      "content": "O cliente pediu desconto de 10% e disse que o concorrente está mais barato."
    },
    {
      "date": "2024-10-06",
      "type": "Call",
      "content": "Liguei mas caiu na caixa postal."
    }
  ]
}

📤 Exemplo de Response
{
  "score": 45,
  "notes": "Cliente sensível a preço e difícil de contatar. Risco de churn alto se não demonstrar valor agregado rápido.",
  "next_step_type": 2
}

🧭 Legenda next_step_type
ID	Tipo
0	Email
1	Ligação
2	Reunião
3	WhatsApp
🔗 Integração com C# (.NET)

Basta criar DTOs equivalentes ao request/response e consumir o endpoint via:

HttpClient

ou Refit (recomendado)

📌 Status

Em desenvolvimento 🚧
