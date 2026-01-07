import requests

def scrape_website(url):
    """
    Extrae el contenido actual de una URL usando Jina AI Reader.
    Obtiene contenido en tiempo real directamente del sitio web.

    Args:
        url (str): La URL completa del sitio a scrapear

    Returns:
        str: Contenido de la página en formato markdown
    """
    # Jina AI Reader convierte cualquier URL a markdown limpio
    jina_url = f"https://r.jina.ai/{url}"

    try:
        response = requests.get(jina_url, timeout=30)
        response.raise_for_status()

        content = response.text

        # Limitar el tamaño si es muy grande (para no saturar el contexto)
        max_length = 15000
        if len(content) > max_length:
            content = content[:max_length] + "\n\n[Contenido truncado por tamaño...]"

        return content

    except requests.exceptions.Timeout:
        return f"Error: Timeout al acceder a {url}"
    except requests.exceptions.RequestException as e:
        return f"Error al hacer scraping de {url}: {str(e)}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"


# Definición de la tool para el modelo
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "scrape_website",
        "description": "Lee el contenido ACTUAL EN TIEMPO REAL de una URL específica. PRIORIZA esta tool cuando el usuario pida datos 'ahora', 'actual', 'en este momento' o información que cambia constantemente como: clima/temperatura actual, precios de bolsa/cripto AHORA, portadas de noticias del día, resultados deportivos en directo, o cualquier dato que se actualice frecuentemente. También para leer artículos completos cuando ya conoces la URL exacta.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "La URL completa del sitio web a scrapear (debe incluir https://). Ejemplos: 'https://www.elmundo.es', 'https://www.elpais.com/economia'"
                }
            },
            "required": ["url"]
        }
    }
}
