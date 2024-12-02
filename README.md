# SnapCloud
Um projeto de sistema de gerenciamento multimídia utilizando AWS para a disciplina de Tópicos em Engenharia de Software.

# Instruções de instalação

## Para o Linux
1. No servidor da aplicação, crie um ambiente virtual
`python3 -m venv venv`
2. Ative o ambiente virtual
`source venv/bin/activate`
3. Instale as dependências com o PIP:
`pip3 install -r requirements.txt`
4. Execute o arquivo "run.py" para criar o banco de dados e arquivos auxiliares:
`python3 -m run.py`
5. Inicialize o servidor:
`flask --app app run --host=0.0.0.0 --port=5000`

## Para o Windows
1. No servidor da aplicação, crie um ambiente virtual
`python -m venv venv`
2. Ative o ambiente virtual
`venv/Scripts/activate`
3. Instale as dependências com o PIP:
`pip install -r requirements.txt`
4. Execute o arquivo "run.py" para criar o banco de dados e arquivos auxiliares:
`python run.py`
5. Inicialize o servidor:
`flask --app app run --host=0.0.0.0 --port=5000`