# streamlit_app.py
import streamlit as st

st.set_page_config(page_title="AsCliente", layout="wide")
st.title("📄 Sistema de Boletos")

st.markdown("Use o menu lateral para acessar o sistema.")

import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Login", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("Login")

# Simula a verificação com banco de dados
import mysql.connector

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "mysql"),
    user=os.getenv("DB_USER", "appuser"),
    password=os.getenv("DB_PASSWORD", "app123"),
    database=os.getenv("DB_NAME", "boletos_db")
)
cursor = conn.cursor(dictionary=True)

usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if st.button("Entrar"):
    cursor.execute("SELECT * FROM ascliente_usuarios WHERE usuario = %s AND senha = %s", (usuario, senha))
    user = cursor.fetchone()

    if user:
        st.session_state['usuario_logado'] = user
        st.success("Login realizado com sucesso!")

        # Redirecionamento baseado no tipo
        tipo = user['tipo']
        if tipo == 'admin':
            st.switch_page("pages/Admin.py")
        elif tipo == 'financeiro':
            st.switch_page("pages/Financeiro.py")
        elif tipo == 'cliente':
            st.switch_page("pages/Cliente.py")
        else:
            st.error("Tipo de usuário inválido.")
    else:
        st.error("Usuário ou senha inválidos.")

cursor.close()
conn.close()