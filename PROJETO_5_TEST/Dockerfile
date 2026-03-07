# Usa uma imagem oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . /app

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta da API
EXPOSE 8000

# Comando para rodar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]