# cadastrar_usuario.py
import mysql.connector
import bcrypt

# Conexão com o banco
conn = mysql.connector.connect(
    host="localhost",  # ou "mysql" se for rodar dentro do Docker
    user="appuser",
    password="app123",
    database="boletos_db"
)
cursor = conn.cursor()

# Dados do novo usuário
nome = "Admin Principal"
email = "admin@email.com"
telefone = "21999999999"
usuario = "admin"
senha = "admin123"
tipo = "admin"

# Gerar hash da senha
senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

# Inserir no banco
try:
    cursor.execute("""
        INSERT INTO ascliente_usuarios (nome, email, telefone, tipo, usuario, senha_hash)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nome, email, telefone, tipo, usuario, senha_hash))
    conn.commit()
    print("Usuário cadastrado com sucesso!")
except mysql.connector.Error as err:
    print(f"Erro: {err}")
finally:
    cursor.close()
    conn.close()
