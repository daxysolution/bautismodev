"""
Servicio de envío de emails para Certificador de Bautismos
"""

import os
import yagmail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr
from dotenv import load_dotenv


def get_email_config():
    """Obtener configuración de email desde .env"""
    load_dotenv()

    return {
        "sender": os.getenv("EMAIL_SENDER"),
        "password": os.getenv("EMAIL_PASSWORD"),
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "587")),
    }


def test_email_configuration():
    """Probar si la configuración de email está disponible"""
    config = get_email_config()
    return bool(config["sender"] and config["password"])


def test_email_connection():
    """Probar conexión de email enviando un email de prueba"""
    try:
        config = get_email_config()
        if not config["sender"] or not config["password"]:
            return False, "Configuración de email no válida"

        yag = yagmail.SMTP(
            user=config["sender"],
            password=config["password"],
            host=config["smtp_server"],
            port=config["smtp_port"],
            smtp_starttls=True,
            smtp_ssl=False,
        )

        # Enviar email de prueba
        yag.send(
            to=config["sender"],  # Enviar a sí mismo
            subject="Prueba de Certificador de Bautismos",
            contents="Este es un email de prueba para verificar la configuración del Certificador de Bautismos.",
        )

        yag.close()
        return True, "Conexión exitosa"

    except Exception as e:
        return False, f"Error de conexión: {str(e)}"


def send_baptism_congratulations_email(
    recipient_email, recipient_name, certificate_path
):
    """
    Enviar email de felicitaciones con certificado adjunto
    Versión mejorada para mejor entrega a Hotmail/Outlook

    :param recipient_email: Email del destinatario
    :param recipient_name: Nombre del destinatario
    :param certificate_path: Ruta al certificado PDF
    :return: True si se envió correctamente, False en caso contrario
    """
    try:
        config = get_email_config()
        if not config["sender"] or not config["password"]:
            print(
                "❌ Error: EMAIL_SENDER y EMAIL_PASSWORD deben estar configurados en .env"
            )
            return False

        # Verificar que el archivo existe
        if not os.path.exists(certificate_path):
            print(f"❌ Error: No se encontró el archivo {certificate_path}")
            return False

        # Intentar primero con yagmail (método original)
        try:
            return _send_with_yagmail(
                config, recipient_email, recipient_name, certificate_path
            )
        except Exception as yag_error:
            print(f"⚠️ Yagmail falló, intentando con SMTP directo: {yag_error}")
            return _send_with_smtp_direct(
                config, recipient_email, recipient_name, certificate_path
            )

    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False


def _send_with_yagmail(config, recipient_email, recipient_name, certificate_path):
    """Enviar usando yagmail (método original)"""
    yag = yagmail.SMTP(
        user=config["sender"],
        password=config["password"],
        host=config["smtp_server"],
        port=config["smtp_port"],
        smtp_starttls=True,
        smtp_ssl=False,
    )

    # Asunto y contenido del email
    subject = "¡Felicitaciones por tu bautismo!"
    body = f"""
    ¡Hola {recipient_name}!
    
    ¡Felicitaciones por tu bautismo! Es un momento muy especial en tu vida espiritual.
    
    Adjunto encontrarás tu certificado de bautismo como recordatorio de este día tan importante.
    
    Que Dios te bendiga en tu nueva vida en Cristo.
    
    Con amor,
    Tu iglesia
    """

    # Enviar email
    yag.send(
        to=recipient_email,
        subject=subject,
        contents=body,
        attachments=certificate_path,
    )

    yag.close()
    print(f"✅ Email enviado exitosamente a {recipient_email} (yagmail)")
    return True


def _send_with_smtp_direct(config, recipient_email, recipient_name, certificate_path):
    """Enviar usando SMTP directo con configuraciones mejoradas para Hotmail/Outlook"""

    # Crear mensaje
    msg = MIMEMultipart()
    msg["From"] = formataddr(("Certificador de Bautismos", config["sender"]))
    msg["To"] = recipient_email
    msg["Subject"] = "¡Felicitaciones por tu bautismo!"

    # Headers adicionales para mejorar la entrega
    msg["X-Mailer"] = "Certificador de Bautismos v1.0"
    msg["X-Priority"] = "3"
    msg["X-MSMail-Priority"] = "Normal"
    msg["Importance"] = "normal"

    # Cuerpo del mensaje
    body = f"""
    ¡Hola {recipient_name}!
    
    ¡Felicitaciones por tu bautismo! Es un momento muy especial en tu vida espiritual.
    
    Adjunto encontrarás tu certificado de bautismo como recordatorio de este día tan importante.
    
    Que Dios te bendiga en tu nueva vida en Cristo.
    
    Con amor,
    Tu iglesia
    """

    msg.attach(MIMEText(body, "plain", "utf-8"))

    # Adjuntar archivo PDF
    with open(certificate_path, "rb") as f:
        pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
        pdf_attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=os.path.basename(certificate_path),
        )
        msg.attach(pdf_attachment)

    # Conectar y enviar
    try:
        server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
        server.starttls()
        server.login(config["sender"], config["password"])

        # Configuraciones adicionales para mejorar la entrega
        server.ehlo()

        text = msg.as_string()
        server.sendmail(config["sender"], recipient_email, text)
        server.quit()

        print(f"✅ Email enviado exitosamente a {recipient_email} (SMTP directo)")
        return True

    except Exception as e:
        print(f"❌ Error con SMTP directo: {e}")
        raise e


def test_email_delivery_to_hotmail():
    """Probar específicamente el envío a Hotmail/Outlook"""
    try:
        config = get_email_config()
        if not config["sender"] or not config["password"]:
            return False, "Configuración de email no válida"

        # Crear un archivo de prueba
        test_file = "output/test_email.txt"
        os.makedirs("output", exist_ok=True)
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Este es un archivo de prueba para verificar la entrega de emails.")

        # Probar envío a la misma cuenta (para verificar que funciona)
        result = send_baptism_congratulations_email(
            config["sender"], "Usuario de Prueba", test_file
        )

        if os.path.exists(test_file):
            os.remove(test_file)

        return result, "Prueba completada"

    except Exception as e:
        return False, f"Error en prueba: {str(e)}"


def send_email_with_alternative_service(
    recipient_email, recipient_name, certificate_path
):
    """
    Método alternativo usando configuraciones más robustas para Hotmail/Outlook
    """
    try:
        config = get_email_config()
        if not config["sender"] or not config["password"]:
            print("❌ Error: Configuración de email no válida")
            return False

        # Verificar que el archivo existe
        if not os.path.exists(certificate_path):
            print(f"❌ Error: No se encontró el archivo {certificate_path}")
            return False

        # Crear mensaje con configuraciones específicas para Hotmail
        msg = MIMEMultipart()
        msg["From"] = formataddr(("Certificador de Bautismos", config["sender"]))
        msg["To"] = recipient_email
        msg["Subject"] = "¡Felicitaciones por tu bautismo!"

        # Headers específicos para mejorar la entrega a Hotmail
        msg["X-Mailer"] = "Certificador de Bautismos v1.0"
        msg["X-Priority"] = "3"
        msg["X-MSMail-Priority"] = "Normal"
        msg["Importance"] = "normal"
        msg["Message-ID"] = (
            f"<{os.urandom(16).hex()}@{config['smtp_server'].replace('smtp.', '')}>"
        )
        msg["Date"] = smtplib.formatdate(localtime=True)

        # Cuerpo del mensaje más simple
        body = f"""¡Hola {recipient_name}!

¡Felicitaciones por tu bautismo! Es un momento muy especial en tu vida espiritual.

Adjunto encontrarás tu certificado de bautismo como recordatorio de este día tan importante.

Que Dios te bendiga en tu nueva vida en Cristo.

Con amor,
Tu iglesia"""

        msg.attach(MIMEText(body, "plain", "utf-8"))

        # Adjuntar archivo PDF con configuración específica
        with open(certificate_path, "rb") as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
            filename = os.path.basename(certificate_path)
            pdf_attachment.add_header(
                "Content-Disposition", "attachment", filename=filename
            )
            pdf_attachment.add_header("Content-Type", "application/pdf")
            msg.attach(pdf_attachment)

        # Conectar con configuraciones mejoradas
        server = smtplib.SMTP(config["smtp_server"], config["smtp_port"], timeout=30)
        server.set_debuglevel(0)  # Cambiar a 1 para debug
        server.starttls()
        server.ehlo()
        server.login(config["sender"], config["password"])

        # Enviar con configuración específica
        text = msg.as_string()
        server.sendmail(config["sender"], [recipient_email], text)
        server.quit()

        print(f"✅ Email enviado exitosamente a {recipient_email} (método alternativo)")
        return True

    except Exception as e:
        print(f"❌ Error con método alternativo: {e}")
        return False


def get_delivery_tips():
    """Obtener consejos para mejorar la entrega de emails"""
    return """
🔧 CONSEJOS PARA MEJORAR LA ENTREGA DE EMAILS A HOTMAIL/OUTLOOK:

1. 📧 VERIFICAR CARPETA DE SPAM:
   - Revisa la carpeta "Correo no deseado" en Hotmail
   - Busca emails de marcosdanielvianello@gmail.com

2. 📋 AGREGAR A CONTACTOS:
   - Agrega marcosdanielvianello@gmail.com a tus contactos
   - Marca como remitente seguro

3. ⚙️ CONFIGURACIÓN DE FILTROS:
   - Ve a Configuración > Ver todas las configuraciones de Outlook
   - Reglas > Agregar nueva regla para permitir emails de Gmail

4. 🔄 ALTERNATIVAS:
   - Usar una cuenta de Gmail para recibir los certificados
   - Solicitar envío por WhatsApp u otro medio
   - Descargar el certificado directamente desde la aplicación

5. 📱 VERIFICAR EN MÓVIL:
   - Revisa también en la app de Outlook móvil
   - A veces los filtros son diferentes

6. ⏰ TIEMPO DE ESPERA:
   - Los emails pueden tardar hasta 24 horas en llegar
   - Revisa periódicamente durante el día
"""
