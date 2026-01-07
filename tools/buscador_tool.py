import os
import requests

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def search_internet(query):
    """
    Busca información en internet usando Tavily API.

    Args:
        query (str): La consulta de búsqueda

    Returns:
        str: Resultados de la búsqueda formateados
    """
    if not TAVILY_API_KEY:
        return "Error: TAVILY_API_KEY no está configurada"

    url = "https://api.tavily.com/search"

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "include_answer": True,
        "max_results": 10
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        # Formatear los resultados
        results = []

        if data.get("answer"):
            results.append(f"Respuesta: {data['answer']}\n")

        if data.get("results"):
            results.append("Fuentes:")
            for i, result in enumerate(data["results"], 1):
                results.append(f"{i}. {result.get('title', 'Sin título')}")
                results.append(f"   URL: {result.get('url', 'N/A')}")
                results.append(f"   {result.get('content', 'Sin contenido')[:200]}...")
                results.append("")

        return "\n".join(results) if results else "No se encontraron resultados"

    except Exception as e:
        return f"Error al buscar en internet: {str(e)}"


# Definición de la tool para el modelo
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "search_internet",
        "description": "Busca y ENCUENTRA información en internet entre múltiples fuentes. Útil para: descubrir URLs relevantes, buscar artículos/noticias sobre un tema, encontrar información general, o cuando NO conoces la URL exacta. IMPORTANTE: Los resultados pueden tener varios días de antigüedad (no son en tiempo real). Para datos que cambian constantemente (clima, precios, portadas de noticias AHORA MISMO) usa scrape_website en su lugar.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "La consulta de búsqueda en internet"
                }
            },
            "required": ["query"]
        }
    }
}
