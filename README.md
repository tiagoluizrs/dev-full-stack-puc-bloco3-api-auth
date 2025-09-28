# # Sistema de Gestão de Hábitos Sustentáveis - API de Autenticação

## O que o projeto faz (Descrição)

Esta API simples gerencia autenticação de usuários permitindo que o front-end realize login e registre novos usuários. Ela utiliza JWT para autenticação e validação de tokens.

- Permite registrar usuários, autenticar e validar tokens JWT.
- Senhas são armazenadas com hash SHA256.
- O endpoint de validação retorna o usuário autenticado.
- 
### Diagrama
Cada um dos 3 projetos terá o mesmo diagrama, apenas com uma diferença que é a marcação de qual serviço ele representa.

![Diagrama](./diagrama-auth.jpg)

## Pré-requisitos
- Docker e Docker Compose (opcional, para rodar com Docker)

O arquivo .env_example tem o que você precisa para gerar o arquivo .env, caso mude alguma configuração, ajuste no .env.

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY="6GwaS2HCfXangHm96sZOdH+333shRS2vFdvtvTAwDUI="
JWT_SECRET_KEY="YzTvTBspjLJ9y5RBgZJaUsCtcvpwZlPxSyRdW3bxU1w="
SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost:5432/authdb
SQLALCHEMY_TRACK_MODIFICATIONS=False
```

## Como rodar com Docker

1. Configure as variáveis de ambiente em um arquivo `.env` (exemplo: `JWT_SECRET_KEY`, `DATABASE_URL`).
2. Execute:

```cmd
docker network create authnet
```

e depois

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

### Resetar token
```bash
curl -X POST http://localhost:5000/auth/reset-token -H "Content-Type: application/json" -d "{\"token\":\"<seu_token_jwt>\"}"
```

Github do projeto:  https://github.com/tiagoluizrs/dev-full-stack-puc-bloco3-api-auth