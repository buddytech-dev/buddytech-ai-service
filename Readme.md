# Buddytech ML Service

Este projeto é um microserviço em Python para processamento e análise de dados comerciais (leads, reuniões, histórico de vendas etc).

---

## Configuração do Ambiente em Outro Computador

### Requisitos

Python instalado (versão 3.8 ou superior recomendada)

#### Verificando se o Python está instalado

Abra o terminal e execute:

```bash
python --version

```

**Observação:** Se não estiver instalado, baixe em [python.org](https://www.python.org).

## Passos para Configuração

1. Clone ou copie o projeto

2. Crie o ambiente virtual No terminal, dentro da pasta do projeto:

```bash
python -m venv venv

```

3. Ative o ambiente virtual

Windows:

```bash
venv\Scripts\activate

```

Mac/Linux:

```bash

source venv/bin/activate

```

4. Instale as dependências

Com o ambiente virtual ativo:

```bash
pip install -r requirements.txt

```

### Testando a Configuração

1. Abra o terminal do VS Code ou CMD

2. Navegue até a pasta do projeto:

```bash
cd buddytech-ml-service

```

3. Ative o ambiente virtual (se ainda não estiver ativo):

```bash
venv\Scripts\activate

```

4. Instale as bibliotecas:

```bash
pip install -r requirements.txt

```

Após esses passos, o ambiente estará pronto para rodar o projeto.

5. Executando o Serviço

Para iniciar o microserviço, rode:

```bash
python app.py

```
