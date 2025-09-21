# Imagem base
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instalar dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Copiar script wait-for-db.sh
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Expor a porta da API-auth (ex: 5002)
EXPOSE 5002

RUN chmod +x entrypoint.sh
# Comando para rodar a aplicação via entrypoint
ENTRYPOINT ["sh", "entrypoint.sh"]
CMD ["/wait-for-db.sh", "gunicorn", "-b", "0.0.0.0:5002", "app:app"]
