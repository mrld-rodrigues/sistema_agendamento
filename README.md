<h2>Appointment System API</h2>

Sistema de agendamentos completo desenvolvido com Flask e MySQL, oferecendo autenticação JWT, gerenciamento de clientes, profissionais, serviços, agendamentos e bloqueios. Ideal para portfólio demonstrando boas práticas de desenvolvimento backend.

<h4>Funcionalidades</h4>

    Autenticação: Registro e login de clientes, profissionais e administradores com JWT.

    Clientes: CRUD completo, com permissões baseadas em tipo de usuário.

    Profissionais: CRUD completo, com campo de intervalo entre atendimentos (buffer).

    Serviços: CRUD completo, com duração e preço.

    Agendamentos: Criação, listagem, remarcação e cancelamento, com verificação de conflitos (incluindo buffer e bloqueios).

    Bloqueios: Dias inteiros, horários específicos, períodos e bloqueios recorrentes (semanais).

    Horários livres: Cálculo inteligente baseado em jornada de trabalho, agendamentos e bloqueios.

    Permissões: Rotas protegidas por tipo de usuário (cliente, profissional, admin).

<h4>Tecnologias</h4>

    Backend: Flask, Flask-JWT-Extended, bcrypt

    Banco de dados: MySQL (MariaDB)

    Outras: python-dotenv, mysql-connector-python

<h4>Estrutura de Diretórios</h4>

.<br>
├── app.py # Ponto de entrada da aplicação<br>
├── utils/ # Configurações (banco de dados, JWT) Decoradores de permissão (admin_required, etc.)<br>
│ ├── config.py<br>
│ └── decorators.py<br>
├── dao/ # Data Access Objects<br>
│ ├── blocked_dao.py<br>
│ ├── client_dao.py<br>
│ ├── professional_dao.py<br>
│ ├── scheduling_dao.py<br>
│ ├── service_dao.py<br>
│ ├── user_dao.py<br>
│ └── worktime_dao.py<br>
├── database/<br>
│ └── connection.py # Conexão com o banco<br>
├── routes/ # Blueprints<br>
│ ├── admin_routes.py<br>
│ ├── auth_routes.py<br>
│ ├── blocked_routes.py<br>
│ ├── clients_routes.py<br>
│ ├── professionals_routes.py<br>
│ ├── scheduling_routes.py<br>
│ └── services_routes.py<br>
├── services/ # Lógica de negócio<br>
│ └── horarios_livres_services.py<br>
├── static/ # Frontend (CSS/JS)<br>
│ ├── css/<br>
│ └── js/<br>
├── templates/ # Páginas HTML<br>
│ ├── auth/<br>
│ ├── client/<br>
│ ├── index.html<br>
│ └── ...<br>
└── .env # Variáveis de ambiente<br>

<h4>Configuração do Ambiente</h4><br>
Pré-requisitos

    Python 3.9+

    MySQL/MariaDB

    pip e virtualenv (recomendado)

<h4>Passo a passo</h4>

Clone o repositório

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

<h4>Configure o banco de dados</h4>

    Crie um banco de dados MySQL (ex.: sistema_agendamento).

    Execute o script database/schema.sql (se disponível) ou importe o dump fornecido.

    Copie o arquivo .env.example para .env e ajuste as credenciais:
    text

DB_HOST=localhost<br>
DB_NAME=sistema_agendamento<br>
DB_USER=root<br>
DB_PASSWORD=sua_senha<br>
DB_PORT=3306<br>
JWT_SECRET_KEY=uma_chave_secreta_forte_com_pelo_menos_32_caracteres<br>

<h4>Execute a aplicação</h4>

python app.py

    O servidor estará disponível em http://localhost:5000.

Endpoints Principais<br>
Método Rota Descrição Permissão<br>
POST /auth/login Login Pública<br>
POST /auth/registro/cliente Registro de cliente Pública<br>
GET /auth/me Dados do usuário logado Qualquer token<br>
POST /clientes Criar cliente Admin<br>
GET /clientes Listar clientes Admin<br>
GET /clientes/<id> Buscar cliente Admin ou próprio<br>
PUT /clientes/<id> Atualizar cliente Admin ou próprio<br>
DELETE /clientes/<id> Deletar cliente Admin<br>
POST /profissionais Criar profissional Admin<br>
GET /profissionais Listar profissionais Pública<br>
GET /profissionais/<id> Buscar profissional Pública<br>
PUT /profissionais/<id> Atualizar profissional Admin ou próprio<br>
DELETE /profissionais/<id> Deletar profissional Admin<br>
POST /servicos Criar serviço Admin<br>
GET /servicos Listar serviços Pública<br>
GET /servicos/<id> Buscar serviço Pública<br>
PUT /servicos/<id> Atualizar serviço Admin<br>
DELETE /servicos/<id> Deletar serviço Admin<br>
POST /agendamentos Criar agendamento Cliente (próprio) ou admin<br>
GET /agendamentos Listar agendamentos (filtro) Profissional (seus) ou admin<br>
GET /agendamentos/horarios-livres Horários livres Pública<br>
DELETE /agendamentos/<id> Deletar agendamento Admin, profissional (dono) ou cliente (dono)<br>
POST /bloqueios/bloquear-dia Bloquear dia Profissional (próprio) ou admin<br>
POST /bloqueios/bloquear-horario Bloquear horário Profissional (próprio) ou admin<br>
POST /bloqueios/recorrente Criar bloqueio recorrente Profissional (próprio) ou admin<br>
GET /bloqueios/todos Listar todos os bloqueios Profissional (seus) ou admin<br>

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

<h4>Frontend (opcional)</h4>

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
