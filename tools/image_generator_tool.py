import os
import requests
import replicate
from datetime import datetime

def generate_image(prompt, output_dir="generated_images"):
    """
    Genera una imagen usando Replicate API (FLUX.1 Schnell)

    Args:
        prompt (str): Descripción de la imagen a generar
        output_dir (str): Directorio donde guardar las imágenes generadas

    Returns:
        str: Confirmación con la ruta de la imagen o mensaje de error
    """
    # Replicate usa REPLICATE_API_TOKEN, pero mantenemos compatibilidad con REPLICATE_API_KEY
    api_key = os.getenv("REPLICATE_API_TOKEN") or os.getenv("REPLICATE_API_KEY")

    if not api_key:
        return "Error: REPLICATE_API_TOKEN (o REPLICATE_API_KEY) no está configurada en las variables de entorno"

    try:
        # Crea el directorio si no existe
        os.makedirs(output_dir, exist_ok=True)

        # Configura el cliente de Replicate con el API token
        os.environ["REPLICATE_API_TOKEN"] = api_key

        print(f"Generando imagen: '{prompt}'...")

        # Usa FLUX.1 Schnell (rápido y de alta calidad)
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": prompt,
                "aspect_ratio": "1:1",
                "output_format": "png",
                "output_quality": 90
            }
        )

        # El output es una lista de URLs
        if not output:
            return "Error: No se generó ninguna imagen"

        image_url = output[0]

        # Descarga la imagen
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()

        # Genera un nombre de archivo único con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Limpia el prompt para usarlo en el nombre del archivo (primeras 30 chars)
        safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_prompt = safe_prompt.replace(' ', '_')
        filename = f"{timestamp}_{safe_prompt}.png"
        filepath = os.path.join(output_dir, filename)

        # Guarda la imagen
        with open(filepath, 'wb') as f:
            f.write(response.content)

        return f"✓ Imagen generada exitosamente!\n\nPrompt: {prompt}\nArchivo: {filepath}\nURL temporal: {image_url}\n\nLa imagen se ha guardado en el directorio '{output_dir}'"

    except replicate.exceptions.ReplicateError as e:
        return f"Error de Replicate API: {str(e)}\n\nVerifica que:\n1. REPLICATE_API_KEY sea válida\n2. Tengas créditos en tu cuenta de Replicate\n3. El modelo esté disponible"

    except requests.exceptions.RequestException as e:
        return f"Error al descargar la imagen: {str(e)}"

    except Exception as e:
        return f"Error inesperado al generar imagen: {str(e)}"


# Definición de la tool para el modelo
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "generate_image",
        "description": "Genera una imagen usando IA a partir de una descripción en texto (text-to-image). Usa esta herramienta cuando el usuario pida crear, generar, o hacer una imagen. Ejemplos: 'genera una imagen de...', 'crea una foto de...', 'hazme un dibujo de...', 'quiero ver una imagen de...'.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Descripción detallada en inglés de la imagen a generar. Incluye detalles como estilo, colores, composición, ambiente, etc. Ejemplo: 'A futuristic city at sunset with flying cars, cyberpunk style, neon lights, highly detailed'"
                }
            },
            "required": ["prompt"]
        }
    }
}
