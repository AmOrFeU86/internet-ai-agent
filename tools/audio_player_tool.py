import os
import pygame
import time

# Inicializa pygame mixer (solo una vez)
pygame.mixer.init()

# Variable global para controlar el estado de reproducción
_current_audio_file = None
_is_playing = False

def control_audio(action, file_path=None, wait=False):
    """
    Controla la reproducción de audio (MP3, WAV, OGG)

    Args:
        action (str): Acción a realizar:
            - "play": Reproduce un archivo de audio
            - "stop": Detiene la reproducción
            - "pause": Pausa la reproducción
            - "resume": Reanuda la reproducción pausada
            - "status": Obtiene el estado actual
        file_path (str): Ruta del archivo de audio (solo para action="play")
        wait (bool): Si es True, espera a que termine el audio (solo para action="play")

    Returns:
        str: Confirmación o mensaje de error
    """
    global _current_audio_file, _is_playing

    try:
        # PLAY - Reproduce un archivo de audio
        if action == "play":
            if not file_path:
                return "Error: Debes especificar 'file_path' para reproducir audio"

            # Verifica que el archivo existe
            if not os.path.exists(file_path):
                return f"Error: El archivo '{file_path}' no existe"

            # Verifica que es un archivo
            if not os.path.isfile(file_path):
                return f"Error: '{file_path}' no es un archivo"

            # Detiene cualquier audio que esté reproduciéndose
            if _is_playing:
                pygame.mixer.music.stop()

            # Carga y reproduce el audio
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            _current_audio_file = file_path
            _is_playing = True

            file_size = os.path.getsize(file_path)

            if wait:
                # Espera a que termine el audio (bloqueante)
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                _is_playing = False
                return f"✓ Audio reproducido completamente: {file_path}\nTamaño: {file_size} bytes"
            else:
                # Reproduce en background (no bloqueante)
                return f"🔊 Reproduciendo: {file_path}\nTamaño: {file_size} bytes"

        # STOP - Detiene la reproducción
        elif action == "stop":
            if not _is_playing:
                return "No hay ningún audio reproduciéndose actualmente"

            pygame.mixer.music.stop()
            previous_file = _current_audio_file
            _is_playing = False
            _current_audio_file = None

            return f"⏹️ Audio detenido: {previous_file}"

        # PAUSE - Pausa la reproducción
        elif action == "pause":
            if not _is_playing:
                return "No hay ningún audio reproduciéndose actualmente"

            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                return f"⏸️ Audio pausado: {_current_audio_file}"
            else:
                return "El audio ya está pausado"

        # RESUME - Reanuda la reproducción
        elif action == "resume":
            if not _current_audio_file:
                return "No hay ningún audio para reanudar"

            # Verifica si el audio está realmente pausado
            if not _is_playing:
                return "No hay ningún audio reproduciéndose actualmente (usa 'play' para iniciar)"

            # Si el mixer no está ocupado, el audio terminó - hay que volver a cargarlo
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(_current_audio_file)
                pygame.mixer.music.play()
                return f"▶️ Audio reiniciado desde el principio: {_current_audio_file}"

            # Si está ocupado, simplemente reanuda
            pygame.mixer.music.unpause()
            return f"▶️ Audio reanudado: {_current_audio_file}"

        # STATUS - Obtiene el estado
        elif action == "status":
            if not _current_audio_file:
                return "ℹ️ Estado: No hay audio cargado"

            # Actualiza el estado real del mixer
            is_busy = pygame.mixer.music.get_busy()

            if is_busy:
                status = "🔊 Reproduciendo"
            elif _is_playing and not is_busy:
                # El audio terminó de reproducirse
                status = "✓ Terminado"
                _is_playing = False
            else:
                status = "⏸️ Pausado" if _is_playing else "⏹️ Detenido"

            return f"{status}\nArchivo: {_current_audio_file}"

        else:
            return f"Error: Acción '{action}' no válida. Acciones disponibles: play, stop, pause, resume, status"

    except pygame.error as e:
        return f"Error de pygame: {str(e)}\n\nFormatos soportados: MP3, WAV, OGG"

    except Exception as e:
        return f"Error inesperado: {str(e)}"


# Definición de la tool para el modelo
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "control_audio",
        "description": "Controla la reproducción de audio (MP3, WAV, OGG). Puede reproducir, pausar, detener, reanudar o consultar el estado de archivos de audio. Usa esta herramienta para todas las operaciones relacionadas con audio. Ejemplos: 'reproduce audio.mp3', 'pausa el audio', 'detén la música', 'reanuda', '¿qué está sonando?'.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["play", "stop", "pause", "resume", "status"],
                    "description": "Acción a realizar: 'play' (reproducir), 'stop' (detener), 'pause' (pausar), 'resume' (reanudar), 'status' (consultar estado)"
                },
                "file_path": {
                    "type": "string",
                    "description": "Ruta del archivo de audio a reproducir (requerido solo para action='play'). Ejemplo: 'generated_audio/audio.mp3', './music.wav'"
                },
                "wait": {
                    "type": "boolean",
                    "description": "Si es True, espera a que termine el audio antes de continuar (solo para action='play'). Default: False",
                    "default": False
                }
            },
            "required": ["action"]
        }
    }
}
