# Sistema de Chamados — Nexa Solutions

Projeto desenvolvido para a disciplina de Manutenção e Evolução de Software, no contexto do desafio técnico da empresa fictícia **Nexa Solutions**.

## Contexto

A Nexa Solutions mantém um sistema interno para abertura e acompanhamento de chamados de suporte. A aplicação é composta por:

- uma **API REST** desenvolvida em Django + Django REST Framework;
- uma **interface HTML simples** para listagem e cadastro de chamados;
- um **banco de dados PostgreSQL**, executado em container.

As demandas formais atendidas neste repositório estão descritas em [`docs/issues.md`](docs/issues.md).

## Tecnologias

- Python 3.12
- Django 5
- Django REST Framework
- PostgreSQL 16
- Docker e Docker Compose
- Git / GitHub (branches, issues e Pull Requests)

## Estrutura do projeto

```text
nexa-solutions/
├── backend/
│   ├── config/          # Configurações do projeto Django
│   ├── chamados/        # App principal (models, serializers, views, tests)
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   └── index.html       # Interface simples de consulta e cadastro
├── docs/
│   ├── README.md        # Enunciado original do desafio
│   └── issues.md        # Demandas formais da empresa
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/) (incluído no Docker Desktop)

Não é necessário ter Python ou PostgreSQL instalados localmente — todo o ambiente roda em containers.

## Configuração do ambiente

1. Copie o arquivo de exemplo de variáveis de ambiente:

   ```bash
   cp .env.example .env
   ```

2. Ajuste os valores de `.env` conforme necessário. As variáveis disponíveis são:

   | Variável | Descrição |
   |---|---|
   | `DJANGO_SECRET_KEY` | Chave secreta do Django. Deve ser trocada em produção. |
   | `DEBUG` | Ativa/desativa o modo de depuração do Django (`True`/`False`). |
   | `ALLOWED_HOSTS` | Lista de hosts permitidos, separados por vírgula. |
   | `POSTGRES_DB` | Nome do banco de dados PostgreSQL. |
   | `POSTGRES_USER` | Usuário do PostgreSQL. |
   | `POSTGRES_PASSWORD` | Senha do PostgreSQL. |
   | `POSTGRES_HOST` | Host do banco (nome do serviço no Docker Compose, ex.: `db`). |
   | `POSTGRES_PORT` | Porta do PostgreSQL (padrão `5432`). |

   O arquivo `.env` **nunca** deve ser versionado — ele já está listado no [`.gitignore`](.gitignore). Apenas `.env.example`, com valores de exemplo, faz parte do repositório.

## Como executar

Com o `.env` configurado, suba a aplicação com:

```bash
docker compose up --build
```

Esse comando:

- constrói a imagem da API;
- sobe o container do PostgreSQL com um volume persistente;
- aguarda o banco ficar disponível antes de iniciar o backend;
- aplica as migrações do Django automaticamente.

Após subir, a aplicação estará disponível em:

- API: `http://localhost:8000/api/chamados/`
- Interface HTML: abra `frontend/index.html` no navegador, ou sirva o arquivo estático conforme configurado no container.

Para encerrar:

```bash
docker compose down
```

Para remover também os dados persistidos do banco:

```bash
docker compose down -v
```

## Executando os testes

Com os containers em execução:

```bash
docker compose exec api python manage.py test
```

Também é possível rodar os testes localmente, fora do Docker, criando um ambiente virtual em `backend/`:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py test
```

## Endpoints da API

Base: `http://localhost:8000/api/`

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/chamados/` | Lista chamados. Aceita filtro opcional `?status=ABERTO\|EM_ANDAMENTO\|CONCLUIDO`. |
| `POST` | `/api/chamados/` | Cria um novo chamado. O campo `titulo` é obrigatório. |
| `GET` | `/api/chamados/<id>/` | Consulta um chamado específico. |
| `PATCH` / `PUT` | `/api/chamados/<id>/` | Atualiza um chamado existente. |
| `GET` | `/api/indicadores/` | Retorna contagem total de chamados e por status (`abertos`, `em_andamento`, `concluidos`). |

**Campos do chamado:** `id`, `titulo` (obrigatório), `descricao`, `status` (`ABERTO`, `EM_ANDAMENTO` ou `CONCLUIDO`), `criado_em`, `atualizado_em`.

**Exemplo — criação válida:**

```bash
curl -X POST http://localhost:8000/api/chamados/ \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Impressora não liga", "descricao": "Setor financeiro"}'
```

**Exemplo — filtro por status:**

```bash
curl "http://localhost:8000/api/chamados/?status=ABERTO"
```

**Exemplo — indicadores:**

```bash
curl http://localhost:8000/api/indicadores/
```

Resposta:

```json
{"total": 4, "abertos": 2, "em_andamento": 1, "concluidos": 1}
```

## Decisões técnicas

- **PostgreSQL em vez de SQLite**: o banco original em SQLite não é adequado para um ambiente reproduzível e multiusuário; o projeto passou a usar PostgreSQL containerizado, com dados persistidos em volume Docker.
- **Segredos via variáveis de ambiente**: a chave secreta do Django e as credenciais de banco deixaram de ser fixadas no código-fonte e passaram a ser lidas de variáveis de ambiente, carregadas a partir de `.env`.
- **Validação explícita no serializer**: campos obrigatórios (como `titulo`) são validados pelo Django REST Framework, retornando `400 Bad Request` com mensagens claras em vez de erro interno (`500`).
- **Filtro por status via query parameter**: escolhido por ser o padrão REST mais simples e testável, com tratamento explícito para valores inválidos.

## Fluxo de trabalho colaborativo

O desenvolvimento segue o padrão:

1. Demandas da empresa registradas como *issues* no GitHub, referenciando os códigos de [`docs/issues.md`](docs/issues.md) (INC-01 a INC-07).
2. Uma branch por issue, seguindo o padrão `tipo/inc-NN-descricao-curta` (ex.: `fix/inc-01-required-title-validation`, `feature/inc-02-status-filter`).
3. Nenhuma alteração é feita diretamente na `main` — todas passam por Pull Request revisado por outro integrante da dupla.

## Integrantes

- Lucas Fagundes — [@LucasFagundesWielewski](https://github.com/LucasFagundesWielewski)
- _(adicionar nome completo e GitHub do segundo integrante)_
