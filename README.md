(The file `/home/mrldrodor/Documentos/mrld_projetos/sistema_agendamento/README.md` exists, but is empty)

# Sistema de Agendamento (API)

API simples para gerenciamento de clientes, profissionais, serviços e agendamentos.

## Visão geral

Aplicação Flask que expõe endpoints para autenticação (JWT), gerenciamento de clientes, profissionais, serviços, agendamentos, bloqueios e rotas administrativas. Também serve um frontend básico nas rotas HTML em `templates/`.

## Requisitos

- Python 3.8+
- Dependências em `requeriments.txt` (instale com `pip install -r requeriments.txt`).

## Instalação rápida

1. Criar e ativar um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instalar dependências:

```bash
pip install -r requeriments.txt
```

## Configuração (variáveis de ambiente)

Defina as variáveis antes de rodar a aplicação:

- `DB_HOST` — host do banco de dados (MySQL/MariaDB)
- `DB_NAME` — nome do banco de dados
- `DB_USER` — usuário do banco
- `DB_PASSWORD` — senha do banco
- `DB_PORT` — porta (opcional, padrão 3306)
- `JWT_SECRET_KEY` — chave secreta para JWT (opcional; há um valor padrão de desenvolvimento)

Exemplo (Linux/macOS):

```bash
export DB_HOST=localhost
export DB_NAME=sistema_agendamento
export DB_USER=root
export DB_PASSWORD=senha
export JWT_SECRET_KEY=minha_chave_secreta
```

## Rodando a aplicação

Com o ambiente ativado e variáveis definidas, execute:

```bash
python app.py
```

Por padrão a aplicação roda em modo de desenvolvimento (`debug=True`).

## Endpoints principais

- `POST /auth/login` — autenticação (recebe `email` e `senha`, retorna `access_token`).
- `GET /auth/me` — retorna dados do usuário autenticado (JWT requerido).
- `POST /auth/registro/cliente` — registra cliente + usuário.
- `POST /auth/registro/profissional` — registra profissional + usuário.

Blueprints (prefixos de API):

- `/clientes` — endpoints de clientes
- `/profissionais` — endpoints de profissionais
- `/servicos` — endpoints de serviços
- `/agendamentos` — endpoints de agendamentos
- `/admin` — endpoints administrativos
- `/bloqueios` — gerenciamento de dias/horários bloqueados

Observação: muitas rotas exigem JWT (token) para operações protegidas.

## Banco de dados

O projeto usa MySQL/MariaDB via `mysql-connector-python`. A conexão é configurada em `utils/config.py` e usada em `database/connection.py`.

## Estrutura resumida

- `app.py` — ponto de entrada e registro de blueprints
- `routes/` — blueprints das rotas (auth, clientes, profissionais, etc.)
- `dao/` — acesso a dados (CRUD para entidades)
- `templates/` e `static/` — frontend servido pela app
- `utils/` — configurações e decoradores

## Observações finais

- Este README é um guia rápido. Para detalhes sobre cada endpoint consulte os arquivos em `routes/` e os DAOs em `dao/`.
- Para produção, ajuste `JWT_SECRET_KEY`, desative `debug` e use um servidor WSGI (gunicorn/uwsgi) e TLS/SSL.

---
