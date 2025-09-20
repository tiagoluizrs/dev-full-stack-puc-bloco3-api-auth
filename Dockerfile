# Imagem base
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instalar dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor a porta da API-auth (ex: 5002)
EXPOSE 5002

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]