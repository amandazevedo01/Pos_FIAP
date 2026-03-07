# 1. Imagem base
FROM python:3.10-slim

# 2. Definir diretório de trabalho
WORKDIR /app

# 3. Copiar arquivos necessários
COPY requirements.txt .
COPY src/ ./src
COPY model.pkl ./model.pkl

# 4. Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expor porta da API
EXPOSE 8000

# 6. Comando para rodar a API
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]