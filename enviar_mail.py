import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuración del remitente
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
USUARIO = 'faustigzmd@gmail.com'
CONTRASEÑA = 'fkwa ghxq lnyi cvso'

# Lista de destinatarios
DESTINATARIOS = ['adm.pampa.rental@hotmail.com','santi.mx@hotmail.com','ventas.pampa.rental@hotmail.com']

def enviar_correo(asunto, cuerpo, destinatarios=DESTINATARIOS):
    mensaje = MIMEMultipart()
    mensaje['From'] = USUARIO
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto

    mensaje.attach(MIMEText(cuerpo, 'plain'))

    try:
        servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        servidor.starttls()
        servidor.login(USUARIO, CONTRASEÑA)
        servidor.sendmail(USUARIO, destinatarios, mensaje.as_string())
        servidor.quit()
        print(f"✅ Correo enviado: {asunto}")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {asunto}")
        print(str(e))
