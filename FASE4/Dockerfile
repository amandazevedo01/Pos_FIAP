# Imagem base oficial do Python
FROM python:3.12-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta que o Uvicorn vai usar
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "api_tsla:app", "--host", "0.0.0.0", "--port", "8000"]
