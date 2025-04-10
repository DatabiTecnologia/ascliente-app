import streamlit as st
import mysql.connector
import hashlib
import webbrowser

# Função para conectar no banco
def get_connection():
    return mysql.connector.connect(
        host="mysql",
        user="appuser",
        password="app123",
        database="boletos_db"
    )

# Criptografar senha
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

st.title("Área do Cliente")

usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if st.button("Entrar"):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    senha_hash = hash_password(senha)

    cursor.execute("SELECT * FROM ascliente_usuarios WHERE usuario = %s AND senha_hash = %s", (usuario, senha_hash))
    user = cursor.fetchone()

    if user:
        st.success(f"Bem-vindo, {user['nome']}! Tipo: {user['tipo']}")

        # Redireciona com base no tipo
        if user['tipo'] == "admin":
            webbrowser.open("http://localhost:8501/admin")
        elif user['tipo'] == "financeiro":
            webbrowser.open("http://localhost:8501/financeiro")
        elif user['tipo'] == "cliente":
            webbrowser.open("http://localhost:8501/cliente")
    else:
        st.error("Usuário ou senha incorretos.")

