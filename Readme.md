# Buddytech ML Service

Este projeto é um microserviço em Python para processamento e análise de dados comerciais (leads, reuniões, histórico de vendas etc).

---

## Configuração do Ambiente em Outro Computador

### Requisitos

Python instalado (versão 3.9.13 recomendada)

#### Verificando se o Python está instalado

Abra o terminal e execute:

```bash
python --version

```

**Observação:** Se não estiver instalado, baixe a versao 3.9.13 em [python.org](https://www.python.org).

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

4. Atualizar o pip (se necessario)

```bash
python -m pip install --upgrade pip

```

5. Instale as dependências

Com o ambiente virtual ativo:

```bash
pip install -r requirements.txt

```

5. Teste opcional para confirmar que as dependências foram instaladas corretamente

```bash
python -c "import transformers; print(transformers.__version__)"

```

Após esses passos, o ambiente estará pronto para rodar o projeto.

6. Executando o Serviço

Para iniciar o microserviço, rode:

```bash
python app.py

```
