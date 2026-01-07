import os
import pickle
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes necesarios para enviar emails con Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """
    Autentica y retorna el servicio de Gmail API
    """
    credentials = None

    # El archivo gmail_token.pickle almacena los tokens de acceso
    if os.path.exists('gmail_token.pickle'):
        with open('gmail_token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # Si no hay credenciales válidas, solicita autenticación
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            # Usa el mismo client_secret.json que ya tienes configurado
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_gmail.json', SCOPES)
            credentials = flow.run_local_server(port=8080)

        # Guarda las credenciales para la próxima ejecución
        with open('gmail_token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return build('gmail', 'v1', credentials=credentials)


def send_email(to, subject, body):
    """
    Envía un email usando Gmail API

    Args:
        to (str): Email del destinatario
        subject (str): Asunto del email
        body (str): Cuerpo del mensaje (texto plano)

    Returns:
        str: Confirmación del envío o mensaje de error
    """
    try:
        # Obtiene el servicio autenticado
        service = get_gmail_service()

        # Crea el mensaje
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject

        # Codifica el mensaje en base64
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        # Envía el email
        send_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        return f"✓ Email enviado exitosamente a {to}\nID del mensaje: {send_message['id']}"

    except HttpError as e:
        error_detail = e.error_details[0] if e.error_details else {}
        error_reason = error_detail.get('reason', 'Desconocido')
        return f"Error HTTP al enviar email: {e.status_code}\nRazón: {error_reason}\n\nVerifica que:\n1. Gmail API esté habilitada en Google Cloud Console\n2. Hayas autorizado el acceso con tu cuenta de Gmail\n3. El archivo client_secret_gmail.json sea válido"

    except FileNotFoundError:
        return "Error: No se encontró el archivo client_secret_gmail.json\n\nPasos para configurarlo:\n1. Ve a Google Cloud Console\n2. Habilita Gmail API\n3. Crea credenciales OAuth 2.0\n4. Descarga el archivo JSON y renómbralo a 'client_secret_gmail.json'"

    except Exception as e:
        return f"Error inesperado al enviar email: {str(e)}"


# Definición de la tool para el modelo
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "Envía un email usando Gmail. Usa esta herramienta cuando el usuario pida enviar un correo electrónico, mandar información por email, o notificar algo vía Gmail. Ejemplos: 'envíame esto por email', 'manda un correo a juan@example.com con esto', 'envía un email de recordatorio'.",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Dirección de email del destinatario (ejemplo: usuario@gmail.com)"
                },
                "subject": {
                    "type": "string",
                    "description": "Asunto del email"
                },
                "body": {
                    "type": "string",
                    "description": "Cuerpo del mensaje (texto plano)"
                }
            },
            "required": ["to", "subject", "body"]
        }
    }
}
