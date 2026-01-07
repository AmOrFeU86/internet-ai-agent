import os
import json

def read_file(file_path):
    """
    Lee el contenido de un archivo local

    Args:
        file_path (str): Ruta del archivo a leer

    Returns:
        str: Contenido del archivo o mensaje de error
    """
    try:
        # Verifica que el archivo existe
        if not os.path.exists(file_path):
            return f"Error: El archivo '{file_path}' no existe"

        # Verifica que es un archivo (no un directorio)
        if not os.path.isfile(file_path):
            return f"Error: '{file_path}' no es un archivo"

        # Lee el archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        size = os.path.getsize(file_path)
        return f"✓ Archivo leído exitosamente: {file_path}\nTamaño: {size} bytes\n\n--- CONTENIDO ---\n{content}"

    except UnicodeDecodeError:
        try:
            # Intenta leer como binario si falla UTF-8
            with open(file_path, 'rb') as f:
                content = f.read()
            return f"✓ Archivo binario leído: {file_path}\nTamaño: {len(content)} bytes\nNota: Este es un archivo binario, no se puede mostrar como texto"
        except Exception as e:
            return f"Error al leer archivo binario: {str(e)}"

    except PermissionError:
        return f"Error: No tienes permisos para leer el archivo '{file_path}'"

    except Exception as e:
        return f"Error inesperado al leer archivo: {str(e)}"


def write_file(file_path, content):
    """
    Escribe contenido en un archivo local (lo crea o sobrescribe)

    Args:
        file_path (str): Ruta del archivo a escribir
        content (str): Contenido a escribir en el archivo

    Returns:
        str: Confirmación o mensaje de error
    """
    try:
        # Crea el directorio si no existe
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        # Escribe el archivo
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        size = os.path.getsize(file_path)
        return f"✓ Archivo escrito exitosamente: {file_path}\nTamaño: {size} bytes\nContenido guardado correctamente"

    except PermissionError:
        return f"Error: No tienes permisos para escribir en '{file_path}'"

    except Exception as e:
        return f"Error inesperado al escribir archivo: {str(e)}"


def list_files(directory="."):
    """
    Lista archivos y carpetas en un directorio

    Args:
        directory (str): Ruta del directorio a listar (por defecto: directorio actual)

    Returns:
        str: Lista de archivos y carpetas o mensaje de error
    """
    try:
        # Verifica que el directorio existe
        if not os.path.exists(directory):
            return f"Error: El directorio '{directory}' no existe"

        # Verifica que es un directorio
        if not os.path.isdir(directory):
            return f"Error: '{directory}' no es un directorio"

        # Lista el contenido
        items = os.listdir(directory)

        if not items:
            return f"El directorio '{directory}' está vacío"

        # Separa archivos y carpetas
        files = []
        folders = []

        for item in sorted(items):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                files.append(f"  📄 {item} ({size} bytes)")
            elif os.path.isdir(item_path):
                folders.append(f"  📁 {item}/")

        result = f"✓ Contenido de '{directory}':\n\n"

        if folders:
            result += "CARPETAS:\n" + "\n".join(folders) + "\n\n"

        if files:
            result += "ARCHIVOS:\n" + "\n".join(files)

        result += f"\n\nTotal: {len(folders)} carpetas, {len(files)} archivos"

        return result

    except PermissionError:
        return f"Error: No tienes permisos para acceder al directorio '{directory}'"

    except Exception as e:
        return f"Error inesperado al listar directorio: {str(e)}"


# Definición de las tools para el modelo
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Lee el contenido de un archivo local. Usa esta herramienta cuando el usuario pida leer, ver, mostrar o abrir un archivo. Ejemplos: 'lee el archivo config.json', 'muéstrame el contenido de datos.txt', 'abre el README'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Ruta completa o relativa del archivo a leer (ejemplo: 'datos.txt', './config/settings.json')"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Escribe contenido en un archivo local (crea el archivo si no existe, lo sobrescribe si existe). Usa esta herramienta cuando el usuario pida crear, escribir, guardar o modificar un archivo. Ejemplos: 'guarda esto en un archivo', 'crea un archivo con este contenido', 'escribe esto en output.txt'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Ruta del archivo a escribir (ejemplo: 'output.txt', './resultados/data.json')"
                    },
                    "content": {
                        "type": "string",
                        "description": "Contenido a escribir en el archivo"
                    }
                },
                "required": ["file_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lista archivos y carpetas en un directorio. Usa esta herramienta cuando el usuario pida ver, listar o mostrar el contenido de una carpeta. Ejemplos: 'lista los archivos en esta carpeta', 'qué hay en el directorio documentos', 'muéstrame el contenido de /tmp'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Ruta del directorio a listar (ejemplo: '.', './documentos', '/tmp'). Por defecto es el directorio actual."
                    }
                },
                "required": []
            }
        }
    }
]
