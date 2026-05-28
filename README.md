# Encurtador de URL

Aplicação web e API REST para encurtar URLs, redirecionar usuários e consultar estatísticas de acesso.

Este projeto foi criado para portfólio de vaga júnior/estágio, com foco em organização, legibilidade, testes e separação de responsabilidades.

## Links

- Site online: adicione aqui depois do deploy
- Documentação da API: adicione aqui depois do deploy com `/docs`

## Tecnologias

- Python 3.11+
- FastAPI
- HTML, CSS e JavaScript
- SQLite para desenvolvimento local
- PostgreSQL para produção
- SQLAlchemy
- Pydantic
- Pytest
- Ruff

## Funcionalidades

- Criar URL curta a partir de uma URL original.
- Usar uma interface web responsiva para encurtar links.
- Redirecionar pelo código curto.
- Consultar dados e quantidade de acessos.
- Validar URLs inválidas.
- Persistir dados em banco local ou online.
- Testes automatizados da API.

## Estrutura

```text
src/url_shortener/
  api.py          Rotas HTTP e contratos da API
  config.py       Configurações por variáveis de ambiente
  database.py     Conexão e sessão do banco de dados
  frontend.py     Configuração da interface web
  main.py         Criação da aplicação FastAPI
  models.py       Modelo SQLAlchemy
  repository.py   Acesso aos dados
  schemas.py      Schemas Pydantic
  service.py      Regras de negócio
  static/         HTML, CSS e JavaScript do site
tests/
  test_api.py     Testes de integração da API
```

## Como Rodar

Crie e ative o ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -e ".[dev]"
```

Inicie a aplicação:

```bash
uvicorn url_shortener.main:app --reload
```

Acesse o site:

```text
http://localhost:8000
```

Acesse a documentação interativa:

```text
http://localhost:8000/docs
```

## Exemplos de Uso

Criar uma URL curta:

```bash
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://www.python.org\"}"
```

Resposta esperada:

```json
{
  "code": "Ab12Cd3",
  "original_url": "https://www.python.org/",
  "short_url": "http://localhost:8000/Ab12Cd3",
  "access_count": 0,
  "created_at": "2026-05-28T12:00:00"
}
```

Redirecionar:

```bash
curl -i http://localhost:8000/Ab12Cd3
```

Consultar estatísticas:

```bash
curl http://localhost:8000/api/urls/Ab12Cd3
```

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto para rodar localmente:

```env
APP_BASE_URL=http://localhost:8000
APP_DATABASE_URL=sqlite:///./url_shortener.db
APP_SHORT_CODE_SIZE=7
```

Para produção, use PostgreSQL. Exemplo de formato:

```env
APP_BASE_URL=https://seu-projeto.onrender.com
APP_DATABASE_URL=postgresql+psycopg://usuario:senha@host/database
APP_SHORT_CODE_SIZE=7
```

Não envie o arquivo `.env` para o GitHub. Use `.env.example` apenas como referência.

## Deploy Online

Este projeto está preparado para deploy no Render usando PostgreSQL no Neon.

### 1. Criar Banco no Neon

1. Acesse `https://neon.tech`.
2. Crie uma conta gratuita.
3. Crie um novo projeto PostgreSQL.
4. Copie a connection string do banco.
5. Use o formato compatível com SQLAlchemy:

```text
postgresql+psycopg://usuario:senha@host/database
```

Se o Neon mostrar uma URL começando com `postgresql://`, troque o início para `postgresql+psycopg://`.

### 2. Subir o Código no GitHub

Antes de subir, confirme que estes arquivos não serão enviados:

```text
.env
url_shortener.db
```

Eles já estão protegidos no `.gitignore`.

### 3. Criar Web Service no Render

1. Acesse `https://render.com`.
2. Crie um novo `Web Service`.
3. Conecte o repositório do GitHub.
4. Use as configurações do arquivo `render.yaml`.
5. Configure as variáveis de ambiente:

```env
APP_BASE_URL=https://seu-projeto.onrender.com
APP_DATABASE_URL=postgresql+psycopg://usuario:senha@host/database
APP_SHORT_CODE_SIZE=7
```

O `APP_DATABASE_URL` deve ser marcado como valor secreto.

### 4. Conferir o Deploy

Depois que o Render finalizar o deploy, acesse:

```text
https://seu-projeto.onrender.com
```

Documentação da API:

```text
https://seu-projeto.onrender.com/docs
```

Endpoint de saúde:

```text
https://seu-projeto.onrender.com/health
```

## Testes e Qualidade

Execute os testes:

```bash
pytest
```

Execute o linter:

```bash
ruff check .
```

## Pontos Para Defender em Entrevista

- A API separa rotas, regras de negócio e persistência.
- O frontend consome a própria API usando `fetch`, sem framework desnecessário.
- O código curto é gerado de forma aleatória e validado contra colisões.
- A validação de URL fica no schema de entrada com Pydantic.
- O projeto usa SQLite localmente e PostgreSQL em produção por variável de ambiente.
- A camada de repositório separa as regras de negócio do acesso ao banco.
- Os testes cobrem criação, redirecionamento, contagem de acessos, URL inválida e código inexistente.
