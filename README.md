Appointment System API

Sistema de agendamentos completo desenvolvido com Flask e MySQL, oferecendo autenticação JWT, gerenciamento de clientes, profissionais, serviços, agendamentos e bloqueios. Ideal para portfólio demonstrando boas práticas de desenvolvimento backend.
Funcionalidades

    Autenticação: Registro e login de clientes, profissionais e administradores com JWT.

    Clientes: CRUD completo, com permissões baseadas em tipo de usuário.

    Profissionais: CRUD completo, com campo de intervalo entre atendimentos (buffer).

    Serviços: CRUD completo, com duração e preço.

    Agendamentos: Criação, listagem, remarcação e cancelamento, com verificação de conflitos (incluindo buffer e bloqueios).

    Bloqueios: Dias inteiros, horários específicos, períodos e bloqueios recorrentes (semanais).

    Horários livres: Cálculo inteligente baseado em jornada de trabalho, agendamentos e bloqueios.

    Permissões: Rotas protegidas por tipo de usuário (cliente, profissional, admin).

Tecnologias

    Backend: Flask, Flask-JWT-Extended, bcrypt

    Banco de dados: MySQL (MariaDB)

    Outras: python-dotenv, mysql-connector-python

Estrutura de Diretórios
text

.
├── app.py # Ponto de entrada da aplicação<br>
├── utils/ # Configurações (banco de dados, JWT) Decoradores de permissão (admin_required, etc.)
│ ├── config.py
│ └── decorators.py #
├── dao/ # Data Access Objects
│ ├── blocked_dao.py
│ ├── client_dao.py
│ ├── professional_dao.py
│ ├── scheduling_dao.py
│ ├── service_dao.py
│ ├── user_dao.py
│ └── worktime_dao.py
├── database/
│ └── connection.py # Conexão com o banco
├── routes/ # Blueprints
│ ├── admin_routes.py
│ ├── auth_routes.py
│ ├── blocked_routes.py
│ ├── clients_routes.py
│ ├── professionals_routes.py
│ ├── scheduling_routes.py
│ └── services_routes.py
├── services/ # Lógica de negócio
│ └── horarios_livres_services.py
├── static/ # Frontend (CSS/JS)
│ ├── css/
│ └── js/
├── templates/ # Páginas HTML
│ ├── auth/
│ ├── client/
│ ├── index.html
│ └── ...
└── .env # Variáveis de ambiente

Configuração do Ambiente
Pré-requisitos

    Python 3.9+

    MySQL/MariaDB

    pip e virtualenv (recomendado)

Passo a passo

    Clone o repositório
    bash

git clone https://github.com/seu-usuario/appointment-system.git
cd appointment-system

Crie e ative um ambiente virtual
bash

python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows

Instale as dependências
bash

pip install -r requirements.txt

Configure o banco de dados

    Crie um banco de dados MySQL (ex.: sistema_agendamento).

    Execute o script database/schema.sql (se disponível) ou importe o dump fornecido.

    Copie o arquivo .env.example para .env e ajuste as credenciais:
    text

DB_HOST=localhost
DB_NAME=sistema_agendamento
DB_USER=root
DB_PASSWORD=sua_senha
DB_PORT=3306
JWT_SECRET_KEY=uma_chave_secreta_forte_com_pelo_menos_32_caracteres

Execute a aplicação
bash

python app.py

    O servidor estará disponível em http://localhost:5000.

Endpoints Principais
Método Rota Descrição Permissão
POST /auth/login Login Pública
POST /auth/registro/cliente Registro de cliente Pública
GET /auth/me Dados do usuário logado Qualquer token
POST /clientes Criar cliente Admin
GET /clientes Listar clientes Admin
GET /clientes/<id> Buscar cliente Admin ou próprio
PUT /clientes/<id> Atualizar cliente Admin ou próprio
DELETE /clientes/<id> Deletar cliente Admin
POST /profissionais Criar profissional Admin
GET /profissionais Listar profissionais Pública
GET /profissionais/<id> Buscar profissional Pública
PUT /profissionais/<id> Atualizar profissional Admin ou próprio
DELETE /profissionais/<id> Deletar profissional Admin
POST /servicos Criar serviço Admin
GET /servicos Listar serviços Pública
GET /servicos/<id> Buscar serviço Pública
PUT /servicos/<id> Atualizar serviço Admin
DELETE /servicos/<id> Deletar serviço Admin
POST /agendamentos Criar agendamento Cliente (próprio) ou admin
GET /agendamentos Listar agendamentos (filtro) Profissional (seus) ou admin
GET /agendamentos/horarios-livres Horários livres Pública
DELETE /agendamentos/<id> Deletar agendamento Admin, profissional (dono) ou cliente (dono)
POST /bloqueios/bloquear-dia Bloquear dia Profissional (próprio) ou admin
POST /bloqueios/bloquear-horario Bloquear horário Profissional (próprio) ou admin
POST /bloqueios/recorrente Criar bloqueio recorrente Profissional (próprio) ou admin
GET /bloqueios/todos Listar todos os bloqueios Profissional (seus) ou admin

Exemplos de Uso (curl)

Login como cliente
bash

curl -X POST http://localhost:5000/auth/login \
 -H "Content-Type: application/json" \
 -d '{"email": "joao@email.com", "senha": "123456"}'

Criar agendamento (com token)
bash

curl -X POST http://localhost:5000/agendamentos \
 -H "Authorization: Bearer SEU_TOKEN" \
 -H "Content-Type: application/json" \
 -d '{
"cliente_id": 1,
"profissional_id": 1,
"servico_id": 1,
"data_hora": "2026-03-20 09:00:00"
}'

Frontend (opcional)

O projeto inclui um frontend simples servido pelo próprio Flask, localizado nas pastas templates/ e static/. Para acessar:

    Página inicial: http://localhost:5000/

    Login: http://localhost:5000/auth/login

    Dashboard do cliente: http://localhost:5000/client/dashboard

O frontend utiliza Tailwind CSS para estilização e JavaScript puro para consumo da API.
Próximos Passos / Melhorias Futuras

    Implementar refresh tokens

    Adicionar testes automatizados (pytest)

    Documentação com Swagger/OpenAPI

    Deploy em produção com Docker e nginx

Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para usar e modificar.

Desenvolvido como projeto de portfólio para demonstrar habilidades em desenvolvimento backend com Flask e boas práticas de arquitetura.
