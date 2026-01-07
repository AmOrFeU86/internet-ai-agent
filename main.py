import requests
import os
import json
from datetime import datetime
from tools.buscador_tool import search_internet, TOOL_DEFINITION as BUSCADOR_TOOL
from tools.scraper_tool import scrape_website, TOOL_DEFINITION as SCRAPER_TOOL
from tools.telegram_tool import (
    send_telegram_message,
    send_telegram_document,
    send_telegram_photo,
    send_telegram_audio,
    TOOL_DEFINITION as TELEGRAM_TOOL,
    TOOL_DEFINITION_DOCUMENT as TELEGRAM_DOCUMENT_TOOL,
    TOOL_DEFINITION_PHOTO as TELEGRAM_PHOTO_TOOL,
    TOOL_DEFINITION_AUDIO as TELEGRAM_AUDIO_TOOL
)
from tools.bolsa_tool import get_stock_price, TOOL_DEFINITION as BOLSA_TOOL
from tools.gmail_tool import send_email, TOOL_DEFINITION as GMAIL_TOOL
from tools.image_generator_tool import generate_image, TOOL_DEFINITION as IMAGE_TOOL
from tools.file_tool import read_file, write_file, list_files, TOOL_DEFINITIONS as FILE_TOOLS
from tools.code_executor_tool import execute_python, TOOL_DEFINITION as CODE_EXECUTOR_TOOL
from tools.tts_tool import text_to_speech, TOOL_DEFINITION as TTS_TOOL
from tools.audio_player_tool import control_audio, TOOL_DEFINITION as AUDIO_PLAYER_TOOL

# Coloca tu API key aquí o mejor como variable de entorno
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "TU_API_KEY_AQUI"

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    # Opcionales pero recomendados por OpenRouter
    "HTTP-Referer": "http://localhost",
    "X-Title": "hello-example"
}

# Obtener la fecha actual para el system prompt
now = datetime.now()
fecha_actual = now.strftime("%Y-%m-%d")  # Formato: 2025-01-07
fecha_legible = now.strftime("%d de %B de %Y")  # Formato: 07 de enero de 2025

# Memoria de sesión: historial de mensajes con mensaje de sistema
conversation_history = [
    {
        "role": "system",
        "content": f"""Eres un asistente de IA útil y conversacional.

INFORMACIÓN IMPORTANTE:
- Fecha actual: {fecha_actual} ({fecha_legible})
- Cuando el usuario pida información del "último mes", "última semana", o "reciente", usa esta fecha como referencia.
- Siempre usa la fecha actual para cálculos de tiempo y búsquedas.

Tienes acceso a múltiples herramientas para ayudar al usuario. Úsalas cuando sea necesario."""
    }
]

def send_message(user_message):
    """
    Envía un mensaje al modelo y mantiene el historial de conversación.
    Maneja function calling si el modelo necesita usar tools.
    """
    # Agregar el mensaje del usuario al historial
    conversation_history.append({"role": "user", "content": user_message})

    # Loop para manejar múltiples llamadas a tools
    while True:
        data = {
            "model": "x-ai/grok-4.1-fast",
            "messages": conversation_history,
            "tools": [
                BUSCADOR_TOOL,
                SCRAPER_TOOL,
                TELEGRAM_TOOL,
                TELEGRAM_DOCUMENT_TOOL,
                TELEGRAM_PHOTO_TOOL,
                TELEGRAM_AUDIO_TOOL,
                BOLSA_TOOL,
                GMAIL_TOOL,
                IMAGE_TOOL,
                *FILE_TOOLS,  # Expande las 3 tools de archivos
                CODE_EXECUTOR_TOOL,
                TTS_TOOL,
                AUDIO_PLAYER_TOOL
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        message = result["choices"][0]["message"]

        # Agregar la respuesta del asistente al historial
        conversation_history.append(message)

        # Si el modelo quiere usar una tool
        if message.get("tool_calls"):
            for tool_call in message["tool_calls"]:
                function_name = tool_call["function"]["name"]
                arguments = json.loads(tool_call["function"]["arguments"])

                # Mostrar qué tool se está usando
                if function_name == "search_internet":
                    print(f"[Buscador: buscando '{arguments.get('query')}']")
                    tool_result = search_internet(arguments["query"])
                elif function_name == "scrape_website":
                    print(f"[Scraper: leyendo {arguments.get('url')}]")
                    tool_result = scrape_website(arguments["url"])
                elif function_name == "send_telegram_message":
                    print(f"[Telegram: enviando mensaje...]")
                    tool_result = send_telegram_message(arguments["message"])
                elif function_name == "send_telegram_document":
                    print(f"[Telegram: enviando documento {arguments.get('file_path')}...]")
                    tool_result = send_telegram_document(
                        arguments["file_path"],
                        arguments.get("caption")
                    )
                elif function_name == "send_telegram_photo":
                    print(f"[Telegram: enviando imagen {arguments.get('file_path')}...]")
                    tool_result = send_telegram_photo(
                        arguments["file_path"],
                        arguments.get("caption")
                    )
                elif function_name == "send_telegram_audio":
                    print(f"[Telegram: enviando audio {arguments.get('file_path')}...]")
                    tool_result = send_telegram_audio(
                        arguments["file_path"],
                        arguments.get("caption"),
                        arguments.get("title")
                    )
                elif function_name == "get_stock_price":
                    print(f"[Bolsa: consultando {arguments.get('symbol')}...]")
                    tool_result = get_stock_price(arguments["symbol"])
                elif function_name == "send_email":
                    print(f"[Gmail: enviando email a {arguments.get('to')}...]")
                    tool_result = send_email(arguments["to"], arguments["subject"], arguments["body"])
                elif function_name == "generate_image":
                    print(f"[IA Image: generando '{arguments.get('prompt')[:50]}...']")
                    tool_result = generate_image(arguments["prompt"])
                elif function_name == "read_file":
                    print(f"[File: leyendo {arguments.get('file_path')}]")
                    tool_result = read_file(arguments["file_path"])
                elif function_name == "write_file":
                    print(f"[File: escribiendo {arguments.get('file_path')}]")
                    tool_result = write_file(arguments["file_path"], arguments["content"])
                elif function_name == "list_files":
                    directory = arguments.get("directory", ".")
                    print(f"[File: listando {directory}]")
                    tool_result = list_files(directory)
                elif function_name == "execute_python":
                    print(f"[Python: ejecutando código...]")
                    tool_result = execute_python(arguments["code"])
                elif function_name == "text_to_speech":
                    voice = arguments.get("voice", "es-ES-AlvaroNeural")
                    print(f"[TTS: generando audio con voz {voice}...]")
                    tool_result = text_to_speech(arguments["text"], voice)
                elif function_name == "control_audio":
                    action = arguments.get("action")
                    print(f"[Audio Player: {action}...]")
                    tool_result = control_audio(
                        action=action,
                        file_path=arguments.get("file_path"),
                        wait=arguments.get("wait", False)
                    )
                else:
                    tool_result = "Tool no encontrada"

                # Agregar el resultado de la tool al historial
                conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": tool_result
                })

            # Continuar el loop para que el modelo procese el resultado
            continue

        # Si no hay tool calls, retornar la respuesta final
        return message.get("content", "")

# Bucle principal de conversación
print("Agente de IA con memoria de sesión iniciado.")
print("Escribe 'salir' o 'exit' para terminar.\n")

while True:
    user_input = input("Tú: ")

    if user_input.lower() in ["salir", "exit", "quit"]:
        print("¡Hasta luego!")
        break

    if not user_input.strip():
        continue

    try:
        response = send_message(user_input)
        print(f"Asistente: {response}\n")
    except Exception as e:
        print(f"Error: {e}\n")
