-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS boletos_db;
USE boletos_db;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS ascliente_usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    telefone VARCHAR(20),
    tipo ENUM('admin', 'financeiro', 'cliente') NOT NULL,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

-- Usuários de exemplo
INSERT INTO ascliente_usuarios (nome, email, telefone, tipo, usuario, senha) VALUES
('Admin Teste', 'admin@teste.com', '5521999999999', 'admin', 'admin1', '123456'),
('Financeiro User', 'financeiro@teste.com', '5521988888888', 'financeiro', 'fin1', '123456'),
('Cliente Demo', 'cliente@teste.com', '5521977777777', 'cliente', 'cli1', '123456');

-- Tabela de boletos
CREATE TABLE IF NOT EXISTS ascliente_boletos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    descricao VARCHAR(255),
    valor DECIMAL(10, 2),
    vencimento DATE,
    status ENUM('pendente', 'pago', 'vencido') DEFAULT 'pendente',
    link_boleto TEXT,
    enviado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES ascliente_usuarios(id) ON DELETE CASCADE
);
