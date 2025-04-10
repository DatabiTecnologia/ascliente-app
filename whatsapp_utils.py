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
