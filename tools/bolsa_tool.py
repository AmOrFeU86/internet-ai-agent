import requests
import json

def get_stock_price(symbol):
    """
    Obtiene información de cotización usando la API de Yahoo Finance directamente.

    Args:
        symbol (str): Símbolo del ticker (ej: AAPL, MSFT, BTC-USD, TSLA)

    Returns:
        str: Información formateada del activo
    """
    try:
        symbol = symbol.upper()

        # URL de la API de Yahoo Finance
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Verificar si hay error
        if data.get('chart', {}).get('error'):
            return f"No se encontró información para '{symbol}'. Verifica que el símbolo sea correcto."

        # Extraer datos
        result = data['chart']['result'][0]
        meta = result['meta']
        quote = result['indicators']['quote'][0]

        nombre = meta.get('longName') or meta.get('shortName') or symbol
        precio_actual = meta['regularMarketPrice']
        precio_anterior = meta['chartPreviousClose']
        precio_apertura = quote['open'][0] if quote['open'] else precio_anterior
        precio_max = quote['high'][0] if quote['high'] else precio_actual
        precio_min = quote['low'][0] if quote['low'] else precio_actual
        volumen = quote['volume'][0] if quote['volume'] else 0

        # Calcular cambio
        cambio = precio_actual - precio_anterior
        cambio_porcentaje = (cambio / precio_anterior) * 100

        # Determinar tendencia
        tendencia = "📈" if cambio >= 0 else "📉"

        # Formatear respuesta
        resultado = f"""**{nombre} ({symbol})**

Precio actual: ${precio_actual:.2f}
Cambio: {tendencia} ${cambio:.2f} ({cambio_porcentaje:+.2f}%)

Apertura: ${precio_apertura:.2f}
Máximo del día: ${precio_max:.2f}
Mínimo del día: ${precio_min:.2f}
Volumen: {volumen:,.0f}

Datos con ~15 min de delay (Yahoo Finance)"""

        return resultado

    except requests.exceptions.RequestException as e:
        return f"Error al conectar con Yahoo Finance: {str(e)}"
    except (KeyError, IndexError, TypeError) as e:
        return f"Error al procesar datos de '{symbol}': {str(e)}\n\nVerifica que el símbolo sea correcto. Ejemplos:\n- Acciones: AAPL, MSFT, GOOGL, TSLA\n- Crypto: BTC-USD, ETH-USD\n- Índices: ^GSPC (S&P 500), ^DJI (Dow Jones)"
    except Exception as e:
        return f"Error inesperado: {str(e)}"


# Definición de la tool para el modelo
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "get_stock_price",
        "description": "Obtiene cotizaciones y precios actuales de acciones, ETFs, criptomonedas e índices bursátiles. Usa esta tool cuando el usuario pregunte por precios de bolsa, valores de acciones, cotizaciones, o 'cuánto vale/está' algún activo financiero. Ejemplos de símbolos: AAPL (Apple), MSFT (Microsoft), TSLA (Tesla), BTC-USD (Bitcoin), ETH-USD (Ethereum), ^GSPC (S&P 500).",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "El símbolo ticker del activo. Para acciones usa el ticker (ej: AAPL, MSFT, GOOGL). Para crypto añade -USD (ej: BTC-USD, ETH-USD). Para índices usa ^ (ej: ^GSPC para S&P 500)"
                }
            },
            "required": ["symbol"]
        }
    }
}
