-- Pegue o ID do cliente 'cli1'
SELECT id FROM ascliente_usuarios WHERE usuario = 'cli1';

-- Suponha que o ID retornado seja 3 (substitua se for diferente)

-- Inserir boletos vencidos
INSERT INTO ascliente_boletos (usuario_id, nome_cliente, descricao, valor, vencimento, status, link_boleto)
VALUES
(3, 'Cliente Demo', 'Conta de Luz - Fevereiro', 180.50, '2025-02-10', 'vencido', 'https://exemplo.com/boleto_v1.pdf'),
(3, 'Cliente Demo', 'Internet - Fevereiro', 120.90, '2025-02-15', 'vencido', 'https://exemplo.com/boleto_v2.pdf');

-- Inserir boletos a vencer
INSERT INTO ascliente_boletos (usuario_id, nome_cliente, descricao, valor, vencimento, status, link_boleto)
VALUES
(3, 'Cliente Demo', 'Água - Abril', 95.40, '2025-04-15', 'pendente', 'https://exemplo.com/boleto_av1.pdf'),
(3, 'Cliente Demo', 'Internet - Abril', 130.00, '2025-04-20', 'pendente', 'https://exemplo.com/boleto_av2.pdf');

-- Inserir boletos pagos
INSERT INTO ascliente_boletos (usuario_id, nome_cliente, descricao, valor, vencimento, status, link_boleto)
VALUES
(3, 'Cliente Demo', 'Mensalidade Escola - Março', 300.00, '2025-03-05', 'pago', 'https://exemplo.com/boleto_p1.pdf'),
(3, 'Cliente Demo', 'Mensalidade Escola - Fevereiro', 300.00, '2025-02-05', 'pago', 'https://exemplo.com/boleto_p2.pdf');
