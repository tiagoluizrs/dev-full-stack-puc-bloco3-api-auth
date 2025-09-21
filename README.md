# Auth

Este projeto é um microsserviço de autenticação com Flask, JWT e PostgreSQL.

## O que o projeto faz

- Permite registrar usuários, autenticar e validar tokens JWT.
- Senhas são armazenadas com hash SHA256.
- O endpoint de validação retorna o ID do usuário autenticado.
- 
## Pré-requisitos
- Docker e Docker Compose (opcional, para rodar com Docker)

## Como rodar com Docker

1. Configure as variáveis de ambiente em um arquivo `.env` (exemplo: `JWT_SECRET_KEY`, `DATABASE_URL`).
2. Execute:

```cmd
docker-compose up --build
```

>> Se ao rodar o build der erro na api, aguarde o banco subir e reinicie que irá funcionar.

O serviço Flask e o banco PostgreSQL serão iniciados. As migrações são aplicadas automaticamente antes do servidor iniciar.

## Como testar os endpoints

Use Postman, Insomnia ou `curl`.

### Registrar usuário
```bash
curl -X POST http://localhost:5000/auth/register -H "Content-Type: application/json" -d "{\"email\":\"user@email.com\",\"username\":\"user1\",\"password\":\"senha123\"}"
```

### Login
```bash
curl -X POST http://localhost:5000/auth/login -H "Content-Type: application/json" -d "{\"email\":\"user@email.com\",\"password\":\"senha123\"}"
```

### Validar token
```bash
curl -X POST http://localhost:5000/auth/validate-token -H "Content-Type: application/json" -d "{\"token\":\"<seu_token_jwt>\"}"
```