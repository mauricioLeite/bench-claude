# DevConnect

Rede interna de habilidades de desenvolvedores. Mapeie competências, encontre especialistas e facilite conexões de mentoria dentro da equipe.

## Overview

DevConnect permite que times de desenvolvimento:
- Cadastrem perfis com hard skills e soft skills niveladas (1-5)
- Encontrem colegas que dominam uma tecnologia específica
- Solicitem contato ou mentoria diretamente pelo sistema
- Visualizem o mapa de competências da equipe em dashboards e clusters

## Setup

### Com Docker (recomendado)

```bash
# Build e subir a aplicação
docker compose up --build

# Em outro terminal: aplicar migrations
docker compose exec web python manage.py migrate

# Criar superusuário (opcional)
docker compose exec web python manage.py createsuperuser
```

Acesse: http://localhost:8000

### Sem Docker (desenvolvimento local)

```bash
# Criar e ativar virtualenv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Migrations e servidor
python manage.py migrate
python manage.py runserver
```

## Commands

| Comando | Descrição |
|---------|-----------|
| `docker compose up --build` | Fazer build e subir a aplicação |
| `docker compose up` | Subir a aplicação (sem rebuild) |
| `docker compose exec web python manage.py migrate` | Aplicar migrations |
| `docker compose exec web python manage.py test` | Rodar testes |
| `docker compose exec web python manage.py createsuperuser` | Criar admin |
| `docker compose exec web python manage.py shell` | Shell interativo |

## Features

- **Perfis de Desenvolvedores**: Cadastro completo com bio, time, cargo e avatar
- **Skills Globais**: Catálogo de hard skills e soft skills com categorias
- **Níveis de Proficiência**: Escala de 1 a 5 (aprendendo → pode mentorar)
- **Busca Avançada**: Filtros por skill, categoria, tipo, nível mínimo, time e disponibilidade
- **Clusters**: Visualização de skills agrupadas por área (Front-end, Back-end, Cloud, etc.)
- **Conexões**: Solicitações de contato/mentoria com controle de status
- **Endorsements**: Validações de skills de colegas
- **Dashboard**: Métricas, top skills, distribuição de níveis e lacunas de conhecimento
- **Admin Django**: Interface administrativa completa em `/admin/`

## Tech Stack

- **Backend**: Python 3.13 + Django 5.2
- **Frontend**: Bootstrap 5.3 + Bootstrap Icons
- **Banco de dados**: SQLite (dev) — facilmente substituível por PostgreSQL
- **Containerização**: Docker + Docker Compose
