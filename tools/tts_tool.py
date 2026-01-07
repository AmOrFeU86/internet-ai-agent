import os
import asyncio
import edge_tts
from datetime import datetime

async def _generate_speech_async(text, voice, output_path):
    """
    Función asíncrona interna para generar el audio
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def text_to_speech(text, voice="es-ES-AlvaroNeural", output_dir="generated_audio"):
    """
    Convierte texto a voz usando Microsoft Edge TTS (Text-to-Speech)

    Args:
        text (str): Texto a convertir en voz
        voice (str): Voz a usar. Opciones populares:
            - es-ES-AlvaroNeural (Hombre, España) - DEFAULT
            - es-ES-ElviraNeural (Mujer, España)
            - es-MX-DaliaNeural (Mujer, México)
            - es-MX-JorgeNeural (Hombre, México)
            - es-AR-ElenaNeural (Mujer, Argentina)
            - en-US-GuyNeural (Hombre, USA)
            - en-US-JennyNeural (Mujer, USA)
        output_dir (str): Directorio donde guardar los audios

    Returns:
        str: Confirmación con la ruta del audio o mensaje de error
    """
    try:
        # Valida que el texto no esté vacío
        if not text or not text.strip():
            return "Error: El texto no puede estar vacío"

        # Crea el directorio si no existe
        os.makedirs(output_dir, exist_ok=True)

        # Genera un nombre de archivo único con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Limpia el texto para usarlo en el nombre del archivo (primeras 30 chars)
        safe_text = "".join(c for c in text[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_text = safe_text.replace(' ', '_')
        filename = f"{timestamp}_{safe_text}.mp3"
        filepath = os.path.join(output_dir, filename)

        print(f"Generando audio: '{text[:50]}...' con voz {voice}")

        # Ejecuta la función asíncrona de forma síncrona
        asyncio.run(_generate_speech_async(text, voice, filepath))

        # Verifica que se creó el archivo
        if not os.path.exists(filepath):
            return "Error: El archivo de audio no se generó correctamente"

        file_size = os.path.getsize(filepath)

        return f"✓ Audio generado exitosamente!\n\nTexto: {text}\nVoz: {voice}\nArchivo: {filepath}\nTamaño: {file_size} bytes\n\nEl audio se ha guardado en el directorio '{output_dir}'"

    except Exception as e:
        return f"Error inesperado al generar audio: {str(e)}\n\nVerifica que:\n1. La librería edge-tts esté instalada (pip install edge-tts)\n2. Tengas conexión a Internet\n3. El nombre de la voz sea válido"


# Definición de la tool para el modelo
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "text_to_speech",
        "description": "Convierte texto a voz (Text-to-Speech / TTS) y genera un archivo de audio MP3. Usa esta herramienta cuando el usuario pida generar audio, crear voz, hacer un audio, o convertir texto a voz. Ejemplos: 'convierte esto a voz', 'genera un audio diciendo...', 'crea un mensaje de voz', 'haz que esto suene en español'.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Texto a convertir en voz. Puede ser cualquier texto en español, inglés u otros idiomas."
                },
                "voice": {
                    "type": "string",
                    "description": "Voz a usar (opcional). Opciones: 'es-ES-AlvaroNeural' (hombre español, default), 'es-ES-ElviraNeural' (mujer español), 'es-MX-DaliaNeural' (mujer mexicano), 'en-US-GuyNeural' (hombre inglés), 'en-US-JennyNeural' (mujer inglés). Si no se especifica, usa la voz por defecto.",
                    "default": "es-ES-AlvaroNeural"
                }
            },
            "required": ["text"]
        }
    }
}
