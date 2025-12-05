Markdown# 🤖 Sales Buddy AI - Microservice

Microsserviço de Inteligência Artificial desenvolvido em **Python** com **FastAPI**.
Este serviço atua como o "cérebro" de análise de vendas, utilizando o **Google Gemini** para processar históricos de interação com clientes e fornecer insights táticos para o sistema de CRM (backend em C#).

## 🚀 Funcionalidades

- **Lead Scoring:** Calcula a "temperatura" (0-100) de um lead baseando-se no histórico e estágio do funil.
- **Análise de Sentimento:** Lê e interpreta o contexto de e-mails, mensagens e anotações.
- **Sugestão de Próximos Passos:** Define qual a melhor ação tática (Email, Ligação, Reunião, WhatsApp).
- **Resposta Estruturada:** Retorna JSON puro garantido (`response_mime_type: application/json`), facilitando a desserialização no C#.

## 🛠️ Tech Stack

- **Linguagem:** Python 3.9+
- **Framework Web:** FastAPI
- **Servidor:** Uvicorn
- **AI Model:** Google Gemini (via `google-generativeai`)
- **Validação de Dados:** Pydantic

## ⚙️ Configuração e Instalação

### 1. Clonar o repositório
```bash
git clone [https://github.com/seu-usuario/sales-buddy-ai.git](https://github.com/seu-usuario/sales-buddy-ai.git)
cd sales-buddy-ai
```
### 2. Criar ambiente virtual (Recomendado)Bashpython -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

### 3. Instalar dependênciasCrie um arquivo requirements.txt com o conteúdo abaixo ou instale manualmente:Plaintextfastapi
uvicorn
google-generativeai
python-dotenv
pydantic
Instale rodando:Bashpip install -r requirements.txt

### 4. Configurar Variáveis de AmbienteCrie um arquivo .env na raiz do projeto e adicione sua chave da API do Gemini (não compartilhe este arquivo!):Snippet de códigoGEMINI_API_KEY=sua_chave_nova_aqui
▶️ Como RodarPara iniciar o servidor de desenvolvimento na porta 8000:Bashpython main.py
# OU via uvicorn diretamente (com hot-reload)
uvicorn main:app --reload
O serviço estará rodando em: http://localhost:8000📚 Documentação da APIO FastAPI gera documentação automática. Com o serviço rodando, acesse:Swagger UI: http://localhost:8000/docsReDoc: http://localhost:8000/redocEndpoint: /analyze [POST]
Este é o endpoint principal consumido pelo backend C#.Request Body (Exemplo):JSON{
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
Response Body (Exemplo):JSON{
  "score": 45,
  "notes": "Cliente sensível a preço e difícil de contatar. Risco de churn alto se não demonstrar valor agregado rápido.",
  "next_step_type": 2
}
Legenda next_step_type:IDTipo0Email1Ligação2Reunião3WhatsApp🔗 Integração com C# (.NET)Para consumir este serviço no .NET, certifique-se de criar as classes DTO correspondentes (AnalysisResponse) e usar HttpClient ou Refit apontando para http://localhost:8000/analyze.Status: Em desenvolvimento 🚧
---

### Próximo passo sugerido

Considerando que você está fazendo a **integração do C# para o Python**, você quer que eu gere o **Service em C#** (usando `HttpClient` e `System.Text.Json`) pronto para consumir esse endpoint `/analyze`?
