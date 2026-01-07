import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    """
    Envía un mensaje a Telegram usando el bot.

    Args:
        message (str): El mensaje a enviar

    Returns:
        str: Confirmación del envío o mensaje de error
    """
    if not TELEGRAM_BOT_TOKEN:
        return "Error: TELEGRAM_BOT_TOKEN no está configurada"

    if not TELEGRAM_CHAT_ID:
        return "Error: TELEGRAM_CHAT_ID no está configurada"

    # Procesa el mensaje para convertir \n literales en saltos de línea reales
    # Esto maneja casos donde el JSON contiene "\\n" escapado
    processed_message = message.replace('\\n', '\n')

    # Limpia el formato Markdown básico ya que no usamos parse_mode
    processed_message = processed_message.replace('**', '')  # Quita negritas
    processed_message = processed_message.replace('__', '')  # Quita subrayado
    processed_message = processed_message.replace('`', '')   # Quita código

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": processed_message
        # No usamos parse_mode por defecto para que los \n funcionen correctamente
        # Si necesitas formato, usa HTML: <b>negrita</b>, <i>cursiva</i>, <code>código</code>
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()

        if data.get("ok"):
            return f"✓ Mensaje enviado exitosamente a Telegram"
        else:
            # Mostrar más detalles del error
            error_desc = data.get('description', 'Desconocido')
            error_code = data.get('error_code', 'N/A')
            return f"Error al enviar mensaje a Telegram:\nCódigo: {error_code}\nDescripción: {error_desc}\n\nVerifica que:\n1. Hayas iniciado conversación con el bot enviando /start\n2. El CHAT_ID sea correcto: {TELEGRAM_CHAT_ID}\n3. El bot token sea válido"

    except requests.exceptions.Timeout:
        return "Error: Timeout al conectar con Telegram"
    except requests.exceptions.RequestException as e:
        return f"Error al enviar mensaje a Telegram: {str(e)}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"


def send_telegram_document(file_path, caption=None):
    """
    Envía un documento/archivo a Telegram.

    Args:
        file_path (str): Ruta del archivo a enviar
        caption (str, optional): Descripción del archivo

    Returns:
        str: Confirmación del envío o mensaje de error
    """
    if not TELEGRAM_BOT_TOKEN:
        return "Error: TELEGRAM_BOT_TOKEN no está configurada"

    if not TELEGRAM_CHAT_ID:
        return "Error: TELEGRAM_CHAT_ID no está configurada"

    if not os.path.exists(file_path):
        return f"Error: El archivo '{file_path}' no existe"

    if not os.path.isfile(file_path):
        return f"Error: '{file_path}' no es un archivo"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"

    try:
        with open(file_path, 'rb') as file:
            files = {'document': file}
            data = {'chat_id': TELEGRAM_CHAT_ID}

            if caption:
                data['caption'] = caption

            response = requests.post(url, data=data, files=files, timeout=30)
            result = response.json()

            if result.get("ok"):
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                return f"✓ Documento enviado exitosamente a Telegram\nArchivo: {file_name}\nTamaño: {file_size} bytes"
            else:
                error_desc = result.get('description', 'Desconocido')
                error_code = result.get('error_code', 'N/A')
                return f"Error al enviar documento:\nCódigo: {error_code}\nDescripción: {error_desc}"

    except requests.exceptions.Timeout:
        return "Error: Timeout al enviar documento a Telegram"
    except requests.exceptions.RequestException as e:
        return f"Error al enviar documento: {str(e)}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"


def send_telegram_photo(file_path, caption=None):
    """
    Envía una imagen a Telegram.

    Args:
        file_path (str): Ruta de la imagen a enviar (JPG, PNG, etc.)
        caption (str, optional): Descripción de la imagen

    Returns:
        str: Confirmación del envío o mensaje de error
    """
    if not TELEGRAM_BOT_TOKEN:
        return "Error: TELEGRAM_BOT_TOKEN no está configurada"

    if not TELEGRAM_CHAT_ID:
        return "Error: TELEGRAM_CHAT_ID no está configurada"

    if not os.path.exists(file_path):
        return f"Error: El archivo '{file_path}' no existe"

    if not os.path.isfile(file_path):
        return f"Error: '{file_path}' no es un archivo"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"

    try:
        with open(file_path, 'rb') as file:
            files = {'photo': file}
            data = {'chat_id': TELEGRAM_CHAT_ID}

            if caption:
                data['caption'] = caption

            response = requests.post(url, data=data, files=files, timeout=30)
            result = response.json()

            if result.get("ok"):
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                return f"✓ Imagen enviada exitosamente a Telegram\nArchivo: {file_name}\nTamaño: {file_size} bytes"
            else:
                error_desc = result.get('description', 'Desconocido')
                error_code = result.get('error_code', 'N/A')
                return f"Error al enviar imagen:\nCódigo: {error_code}\nDescripción: {error_desc}"

    except requests.exceptions.Timeout:
        return "Error: Timeout al enviar imagen a Telegram"
    except requests.exceptions.RequestException as e:
        return f"Error al enviar imagen: {str(e)}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"


def send_telegram_audio(file_path, caption=None, title=None):
    """
    Envía un archivo de audio a Telegram.

    Args:
        file_path (str): Ruta del archivo de audio (MP3, etc.)
        caption (str, optional): Descripción del audio
        title (str, optional): Título del audio

    Returns:
        str: Confirmación del envío o mensaje de error
    """
    if not TELEGRAM_BOT_TOKEN:
        return "Error: TELEGRAM_BOT_TOKEN no está configurada"

    if not TELEGRAM_CHAT_ID:
        return "Error: TELEGRAM_CHAT_ID no está configurada"

    if not os.path.exists(file_path):
        return f"Error: El archivo '{file_path}' no existe"

    if not os.path.isfile(file_path):
        return f"Error: '{file_path}' no es un archivo"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendAudio"

    try:
        with open(file_path, 'rb') as file:
            files = {'audio': file}
            data = {'chat_id': TELEGRAM_CHAT_ID}

            if caption:
                data['caption'] = caption

            if title:
                data['title'] = title

            response = requests.post(url, data=data, files=files, timeout=30)
            result = response.json()

            if result.get("ok"):
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                return f"✓ Audio enviado exitosamente a Telegram\nArchivo: {file_name}\nTamaño: {file_size} bytes"
            else:
                error_desc = result.get('description', 'Desconocido')
                error_code = result.get('error_code', 'N/A')
                return f"Error al enviar audio:\nCódigo: {error_code}\nDescripción: {error_desc}"

    except requests.exceptions.Timeout:
        return "Error: Timeout al enviar audio a Telegram"
    except requests.exceptions.RequestException as e:
        return f"Error al enviar audio: {str(e)}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"


# Definiciones de las tools para el modelo
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "send_telegram_message",
        "description": "Envía un mensaje de texto a Telegram. Usa esta tool cuando el usuario pida explícitamente enviar texto a Telegram, crear recordatorios, notificaciones, o guardar información importante que quiera recibir en su Telegram. Ejemplos: 'envíame un resumen a Telegram', 'mándame esto por Telegram', 'guarda esto en Telegram'.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "El mensaje a enviar. Los saltos de línea (\\n) se renderizarán correctamente. Para dar formato usa emojis o caracteres Unicode."
                }
            },
            "required": ["message"]
        }
    }
}

TOOL_DEFINITION_DOCUMENT = {
    "type": "function",
    "function": {
        "name": "send_telegram_document",
        "description": "Envía un documento/archivo a Telegram. Usa esta tool cuando el usuario pida enviar archivos, PDFs, documentos, o cualquier tipo de archivo que no sea específicamente imagen o audio. Ejemplos: 'envíame este archivo a Telegram', 'manda el PDF por Telegram'.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Ruta completa del archivo a enviar. Ejemplo: 'C:/Users/Gabriel/Documents/archivo.pdf' o './documento.txt'"
                },
                "caption": {
                    "type": "string",
                    "description": "Descripción o comentario sobre el archivo (opcional)"
                }
            },
            "required": ["file_path"]
        }
    }
}

TOOL_DEFINITION_PHOTO = {
    "type": "function",
    "function": {
        "name": "send_telegram_photo",
        "description": "Envía una imagen a Telegram. Usa esta tool cuando el usuario pida enviar imágenes, fotos, capturas de pantalla, o gráficos. Soporta JPG, PNG, etc. Ejemplos: 'envíame esta imagen a Telegram', 'manda la foto por Telegram'.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Ruta completa de la imagen a enviar. Ejemplo: 'C:/Users/Gabriel/Pictures/foto.jpg' o './imagen.png'"
                },
                "caption": {
                    "type": "string",
                    "description": "Descripción o comentario sobre la imagen (opcional)"
                }
            },
            "required": ["file_path"]
        }
    }
}

TOOL_DEFINITION_AUDIO = {
    "type": "function",
    "function": {
        "name": "send_telegram_audio",
        "description": "Envía un archivo de audio a Telegram. Usa esta tool cuando el usuario pida enviar audios, podcasts, música, grabaciones de voz, o archivos MP3. Ejemplos: 'envíame el audio a Telegram', 'manda el podcast por Telegram'.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Ruta completa del archivo de audio a enviar. Ejemplo: 'generated_audio/podcast.mp3' o 'C:/Users/Gabriel/Music/cancion.mp3'"
                },
                "caption": {
                    "type": "string",
                    "description": "Descripción o comentario sobre el audio (opcional)"
                },
                "title": {
                    "type": "string",
                    "description": "Título del audio que se mostrará en Telegram (opcional)"
                }
            },
            "required": ["file_path"]
        }
    }
}
