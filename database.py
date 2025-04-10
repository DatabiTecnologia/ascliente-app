import mysql.connector
import pandas as pd

def conectar():
    return mysql.connector.connect(
        host="mysql",
        user="appuser",
        password="app123",
        database="boletos_db"
    )

def validar_login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ascliente_usuarios WHERE usuario=%s AND senha=%s", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def get_boletos_do_usuario(usuario):
    conn = conectar()
    query = "SELECT * FROM ascliente_boletos WHERE usuario = %s"
    df = pd.read_sql(query, conn, params=(usuario,))
    conn.close()
    return df
