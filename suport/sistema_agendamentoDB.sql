SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS horarios_bloqueados;
DROP TABLE IF EXISTS horarios_trabalho;
DROP TABLE IF EXISTS agendamentos;
DROP TABLE IF EXISTS servicos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS profissionais;

SET FOREIGN_KEY_CHECKS=1;

-- =========================
-- PROFISSIONAIS
-- =========================
CREATE TABLE profissionais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    profissao VARCHAR(100) NOT NULL
);

INSERT INTO profissionais (nome, profissao)
VALUES ('João Chef', 'Cozinheiro');

-- =========================
-- CLIENTES
-- =========================
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20)
);

-- 15 clientes exemplo
INSERT INTO clientes (nome,email,telefone) VALUES
('Cliente 1','c1@email.com','111'),
('Cliente 2','c2@email.com','222'),
('Cliente 3','c3@email.com','333'),
('Cliente 4','c4@email.com','444'),
('Cliente 5','c5@email.com','555'),
('Cliente 6','c6@email.com','666'),
('Cliente 7','c7@email.com','777'),
('Cliente 8','c8@email.com','888'),
('Cliente 9','c9@email.com','999'),
('Cliente 10','c10@email.com','1010'),
('Cliente 11','c11@email.com','1111'),
('Cliente 12','c12@email.com','1212'),
('Cliente 13','c13@email.com','1313'),
('Cliente 14','c14@email.com','1414'),
('Cliente 15','c15@email.com','1515');

-- =========================
-- SERVIÇOS
-- =========================
CREATE TABLE servicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    duracao_minutos INT NOT NULL,
    preco DECIMAL(10,2) NOT NULL
);

INSERT INTO servicos (nome,duracao_minutos,preco)
VALUES ('Jantar Particular',240,1700.00);

-- =========================
-- AGENDAMENTOS
-- =========================
CREATE TABLE agendamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profissional_id INT NOT NULL,
    cliente_id INT NOT NULL,
    servico_id INT NOT NULL,
    data_hora DATETIME NOT NULL,
    duracao_minutos INT NOT NULL,

    FOREIGN KEY (profissional_id) REFERENCES profissionais(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (servico_id) REFERENCES servicos(id)
);

-- Alguns agendamentos exemplo
INSERT INTO agendamentos 
(profissional_id, cliente_id, servico_id, data_hora, duracao_minutos)
VALUES
(1,1,1,'2026-02-01 18:00:00',240),
(1,2,1,'2026-02-02 19:00:00',240),
(1,3,1,'2026-02-03 20:00:00',240),
(1,4,1,'2026-02-04 18:00:00',240),
(1,5,1,'2026-02-05 18:00:00',240);

-- =========================
-- HORÁRIOS DE TRABALHO
-- =========================
CREATE TABLE horarios_trabalho (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profissional_id INT NOT NULL,
    dia_semana TINYINT NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,

    FOREIGN KEY (profissional_id) REFERENCES profissionais(id)
);

-- Cozinheiro trabalha todos os dias 18h às 00h
INSERT INTO horarios_trabalho 
(profissional_id,dia_semana,hora_inicio,hora_fim)
VALUES
(1,0,'18:00','00:00'),
(1,1,'18:00','00:00'),
(1,2,'18:00','00:00'),
(1,3,'18:00','00:00'),
(1,4,'18:00','00:00'),
(1,5,'18:00','00:00'),
(1,6,'18:00','00:00');

-- =========================
-- BLOQUEIOS POR HORÁRIO
-- =========================
CREATE TABLE horarios_bloqueados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profissional_id INT NOT NULL,
    data DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    motivo VARCHAR(255),

    FOREIGN KEY (profissional_id) REFERENCES profissionais(id)
);

-- Exemplo de bloqueio
INSERT INTO horarios_bloqueados
(profissional_id,data,hora_inicio,hora_fim,motivo)
VALUES
(1,'2026-02-06','22:00','23:30','Descanso');


