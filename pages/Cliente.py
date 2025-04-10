# pages/Cliente.py
import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Área do Cliente", layout="centered", initial_sidebar_state="collapsed")
st.markdown("<style>.css-18e3th9 {visibility: hidden;}</style>", unsafe_allow_html=True)

if 'usuario_logado' not in st.session_state or st.session_state['usuario_logado']['tipo'] != 'cliente':
    st.error("Acesso não autorizado.")
    st.stop()

st.title("Seus Boletos")

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "mysql"),
    user=os.getenv("DB_USER", "appuser"),
    password=os.getenv("DB_PASSWORD", "app123"),
    database=os.getenv("DB_NAME", "boletos_db")
)
cursor = conn.cursor(dictionary=True)

usuario_id = st.session_state['usuario_logado']['id']

st.subheader("Boletos Vencidos")
cursor.execute("""
    SELECT descricao, valor, vencimento, link_boleto FROM ascliente_boletos
    WHERE usuario_id = %s AND status = 'vencido'
    ORDER BY vencimento DESC LIMIT 5
""", (usuario_id,))
boletos_vencidos = cursor.fetchall()
for b in boletos_vencidos:
    with st.expander(f"{b['descricao']} - R${b['valor']} (Vencido)"):
        st.write(f"Vencimento: {b['vencimento']}")
        if b['link_boleto']:
            st.markdown(f"[Baixar Boleto]({b['link_boleto']})")

st.subheader("Boletos a Vencer")
cursor.execute("""
    SELECT descricao, valor, vencimento, link_boleto FROM ascliente_boletos
    WHERE usuario_id = %s AND status = 'pendente'
    ORDER BY vencimento ASC LIMIT 5
""", (usuario_id,))
boletos_pendentes = cursor.fetchall()
for b in boletos_pendentes:
    with st.expander(f"{b['descricao']} - R${b['valor']} (A Vencer)"):
        st.write(f"Vencimento: {b['vencimento']}")
        if b['link_boleto']:
            st.markdown(f"[Baixar Boleto]({b['link_boleto']})")

st.subheader("Boletos Pagos")
cursor.execute("""
    SELECT descricao, valor, vencimento, link_boleto FROM ascliente_boletos
    WHERE usuario_id = %s AND status = 'pago'
    ORDER BY vencimento DESC LIMIT 5
""", (usuario_id,))
boletos_pagos = cursor.fetchall()
for b in boletos_pagos:
    with st.expander(f"{b['descricao']} - R${b['valor']} (Pago)"):
        st.write(f"Vencimento: {b['vencimento']}")
        if b['link_boleto']:
            st.markdown(f"[Baixar Boleto]({b['link_boleto']})")

cursor.close()
conn.close()