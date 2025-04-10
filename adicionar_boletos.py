# adicionar_boletos.py
import mysql.connector
from datetime import date, timedelta

# Conexão com banco (ajustado para rodar dentro do Docker)
conn = mysql.connector.connect(
    host="mysql",
    user="appuser",
    password="app123",
    database="boletos_db"
)
cursor = conn.cursor()

# Buscar ID do usuário de teste
cursor.execute("SELECT id FROM ascliente_usuarios WHERE usuario = 'cliente1'")
user = cursor.fetchone()

if user:
    usuario_id = user[0]

    boletos_teste = [
        ("Mensalidade Abril", 120.50, date.today() - timedelta(days=10), False),
        ("Mensalidade Maio", 130.00, date.today() + timedelta(days=10), False),
        ("Serviço Extra", 89.90, date.today() + timedelta(days=20), True),
    ]

    for desc, valor, venc, pago in boletos_teste:
        cursor.execute("""
            INSERT INTO ascliente_boletos (usuario_id, descricao, valor, vencimento, pago)
            VALUES (%s, %s, %s, %s, %s)
        """, (usuario_id, desc, valor, venc, pago))

    conn.commit()
    print("Boletos de teste adicionados com sucesso!")
else:
    print("Usuário 'cliente1' não encontrado. Cadastre-o no painel de admin.")

cursor.close()
conn.close()
