# pages/Admin.py
import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import urllib.parse

load_dotenv()

st.set_page_config(page_title="Admin", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    #MainMenu, footer {visibility: hidden;}
    .block-container {padding-top: 2rem;}
    .stButton>button {border-radius: 12px; padding: 0.5rem 1.5rem; background-color: #4CAF50; color: white; border: none;}
    .stButton>button:hover {background-color: #45a049;}
    </style>
""", unsafe_allow_html=True)

if 'usuario_logado' not in st.session_state or st.session_state['usuario_logado']['tipo'] != 'admin':
    st.error("Acesso não autorizado.")
    st.stop()

st.title("📊 Painel do Administrador")

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "mysql"),
    user=os.getenv("DB_USER", "appuser"),
    password=os.getenv("DB_PASSWORD", "app123"),
    database=os.getenv("DB_NAME", "boletos_db")
)
cursor = conn.cursor(dictionary=True)

def gerar_pdf_boleto(descricao, valor, vencimento, nome_cliente, arquivo_saida="boleto.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Boleto de Pagamento", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Cliente: {nome_cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Descrição: {descricao}", ln=True)
    pdf.cell(200, 10, txt=f"Valor: R$ {valor}", ln=True)
    pdf.cell(200, 10, txt=f"Vencimento: {vencimento}", ln=True)
    pdf.output(arquivo_saida)
    return arquivo_saida

def enviar_email_com_pdf(destinatario, assunto, corpo, caminho_pdf):
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = os.getenv("EMAIL_ORIGEM")
    msg['To'] = destinatario
    msg.set_content(corpo)

    with open(caminho_pdf, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(caminho_pdf)

    msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    with smtplib.SMTP_SSL(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as smtp:
        smtp.login(os.getenv("EMAIL_ORIGEM"), os.getenv("EMAIL_SENHA"))
        smtp.send_message(msg)

def enviar_whatsapp(numero, mensagem):
    numero = numero.replace("+", "").replace(" ", "").replace("-", "")
    mensagem_codificada = urllib.parse.quote(mensagem)
    url = f"https://wa.me/{numero}?text={mensagem_codificada}"
    return url

st.subheader("👥 Cadastro de Usuários")
nome = st.text_input("Nome")
email = st.text_input("Email")
telefone = st.text_input("Telefone")
tipo = st.selectbox("Tipo de usuário", ["admin", "financeiro", "cliente"])
usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if st.button("Cadastrar Usuário"):
    try:
        cursor.execute("""
            INSERT INTO ascliente_usuarios (nome, email, telefone, tipo, usuario, senha)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, email, telefone, tipo, usuario, senha))
        conn.commit()
        st.success("Usuário cadastrado com sucesso!")
    except mysql.connector.Error as err:
        st.error(f"Erro: {err}")

st.markdown("---")

st.subheader("🔎 Buscar Boletos por Cliente")
cursor.execute("SELECT id, nome FROM ascliente_usuarios WHERE tipo = 'cliente'")
clientes = cursor.fetchall()
nome_id_map = {c['nome']: c['id'] for c in clientes}
selected_nome = st.selectbox("Selecione o cliente", list(nome_id_map.keys()))

if st.button("Buscar Boletos"):
    cursor.execute("""
        SELECT descricao, valor, vencimento, status, link_boleto FROM ascliente_boletos
        WHERE usuario_id = %s
        ORDER BY vencimento DESC
    """, (nome_id_map[selected_nome],))
    boletos = cursor.fetchall()
    for b in boletos:
        with st.expander(f"{b['descricao']} - R${b['valor']} ({b['status']})"):
            st.write(f"Vencimento: {b['vencimento']}")
            if b['link_boleto']:
                st.markdown(f"[📎 Baixar Boleto]({b['link_boleto']})")

st.markdown("---")

st.subheader("📤 Envio de Boletos a Vencer")
if st.button("Enviar via WhatsApp"):
    cursor.execute("SELECT id, nome, telefone FROM ascliente_usuarios WHERE tipo = 'cliente'")
    clientes = cursor.fetchall()
    for cliente in clientes:
        cursor.execute("""
            SELECT descricao, valor, vencimento FROM ascliente_boletos
            WHERE usuario_id = %s AND status = 'pendente'
        """, (cliente['id'],))
        boletos = cursor.fetchall()
        for boleto in boletos:
            mensagem = f"Olá {cliente['nome']}, seu boleto de {boleto['descricao']} no valor de R$ {boleto['valor']} vence em {boleto['vencimento']}."
            url = enviar_whatsapp(cliente['telefone'], mensagem)
            st.markdown(f"[{cliente['nome']}]({url})", unsafe_allow_html=True)

if st.button("Enviar via Email com PDF"):
    cursor.execute("SELECT id, nome, email FROM ascliente_usuarios WHERE tipo = 'cliente'")
    clientes = cursor.fetchall()

    for cliente in clientes:
        cursor.execute("""
            SELECT descricao, valor, vencimento FROM ascliente_boletos
            WHERE usuario_id = %s AND status = 'pendente'
        """, (cliente['id'],))
        boletos = cursor.fetchall()

        for boleto in boletos:
            caminho_pdf = gerar_pdf_boleto(
                descricao=boleto['descricao'],
                valor=boleto['valor'],
                vencimento=boleto['vencimento'],
                nome_cliente=cliente['nome']
            )
            try:
                enviar_email_com_pdf(
                    destinatario=cliente['email'],
                    assunto="Seu boleto está disponível",
                    corpo="Segue anexo o seu boleto para pagamento.",
                    caminho_pdf=caminho_pdf
                )
            except Exception as e:
                st.warning(f"Erro ao enviar para {cliente['email']}: {e}")

    st.success("Boletos enviados com sucesso!")

cursor.close()
conn.close()
