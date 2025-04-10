# email_utils.py
import smtplib
from email.message import EmailMessage
import os


def enviar_email(destinatario, assunto, corpo):
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA")

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario
    msg.set_content(corpo)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Erro ao enviar email:", e)
        return False


# whatsapp_utils.py
from twilio.rest import Client
import os


def enviar_whatsapp(destinatario_telefone, mensagem):
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_TOKEN")
    twilio_numero = os.getenv("TWILIO_NUMERO")

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=mensagem,
            from_=twilio_numero,
            to=f'whatsapp:{destinatario_telefone}'
        )
        return True
    except Exception as e:
        print("Erro ao enviar WhatsApp:", e)
        return False
