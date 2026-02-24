<h1>Agendamento API</h1>

Uma API RESTful para gerenciamento de agendamentos de serviços, construída com Flask e MySQL. Permite o cadastro de clientes, profissionais, serviços, bloqueios de horários e a criação/consulta de agendamentos, com autenticação via JWT.
Funcionalidades

    Cadastro e autenticação de usuários (clientes, profissionais e administradores)

    Gerenciamento de clientes, profissionais e serviços

    Criação e consulta de agendamentos

    Bloqueios de horários (dia inteiro, períodos, horários específicos e recorrentes)

    Cálculo de horários livres considerando jornada de trabalho, agendamentos e bloqueios

    Diferentes níveis de acesso (admin, profissional, cliente)

<h3>Tecnologias utilizadas</h3>

    Python 3.8+

    Flask

    Flask-JWT-Extended

    MySQL (conector oficial)

    bcrypt (para hash de senhas)

    python-dotenv

<h3>Pré-requisitos</h3>

    Python 3.8 ou superior

    MySQL Server (ou MariaDB)

    pip (gerenciador de pacotes Python)

    Git (opcional, para clonar o repositório)

<h3>Instalação</h3>

    Clone o repositório

    git clone https://github.com/mrld-rodrigues/sistema_agendamento.git

<h3>Crie e ative um ambiente virtual</h3>

    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows

<h3>Instale as dependências</h3>

    pip install -r requirements.txt

<h3>Configure as variáveis de ambiente</h3>

    Crie um arquivo .env na raiz do projeto com o seguinte conteúdo (ajuste os valores conforme seu ambiente):

    DB_HOST=localhost
    DB_NAME=agendamento_db
    DB_USER=root
    DB_PASSWORD=sua_senha
    DB_PORT=3306
    JWT_SECRET_KEY=uma-chave-secreta-forte

<h3>Crie o banco de dados</h3>

    Usando o MySQL ou o MariaDB
    Use o dump(sistema_back_up.sql) que está no diretório sistema_agendamento/suport
    para testar.
