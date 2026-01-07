# Agente de IA con Tools (Function Calling)

Agente de inteligencia artificial con memoria de sesión que puede usar múltiples herramientas (tools) para interactuar con servicios externos.

## Características

El agente puede:
- 🔍 **Buscar en Internet** - Búsquedas en tiempo real
- 🌐 **Hacer Scraping** - Extraer contenido de sitios web
- 💬 **Enviar mensajes a Telegram** - Notificaciones y recordatorios
- 📈 **Consultar precios de acciones** - Información del mercado bursátil
- 📧 **Enviar emails con Gmail** - Correos automatizados
- 🎨 **Generar imágenes con IA** - Creación de imágenes desde texto
- 📁 **Manipular archivos locales** - Leer, escribir y listar archivos
- 🐍 **Ejecutar código Python** - Cálculos y procesamiento dinámico
- 🔊 **Text-to-Speech** - Convierte texto a voz en múltiples idiomas
- 🎵 **Audio Player** - Reproduce, pausa, reanuda y controla archivos de audio

## Instalación

1. Clona el repositorio:
```bash
git clone [tu-repo]
cd internet-ai-agent
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita .env con tus API keys
```

4. (Opcional) Configura Gmail API:
   - Ve a [Google Cloud Console](https://console.cloud.google.com)
   - Habilita Gmail API
   - Descarga las credenciales OAuth 2.0
   - Guárdalas como `client_secret_gmail.json`

## Configuración

### Variables de entorno necesarias:

```env
OPENROUTER_API_KEY=tu_api_key        # Obligatorio
TELEGRAM_BOT_TOKEN=tu_token          # Opcional
TELEGRAM_CHAT_ID=tu_chat_id          # Opcional
REPLICATE_API_KEY=tu_api_key         # Opcional
```

## Uso

Ejecuta el agente:
```bash
python main.py
```

### Ejemplos de comandos:

```
Tú: Busca información sobre inteligencia artificial
Tú: Dame el precio de las acciones de Apple
Tú: Envíame un resumen a Telegram
Tú: Manda un email a juan@example.com con un recordatorio
Tú: Genera una imagen de un gato astronauta en el espacio
Tú: Lee el archivo config.json
Tú: Guarda esto en un archivo llamado resultados.txt
Tú: Calcula la factorial de 50
Tú: Convierte este texto a voz: Hola, soy tu asistente de IA
Tú: Reproduce el audio que acabas de generar
Tú: Pausa el audio
```

## Estructura del proyecto

```
internet-ai-agent/
├── main.py                      # Archivo principal
├── requirements.txt             # Dependencias
├── .env.example                # Plantilla de variables de entorno
├── client_secret.example.json  # Plantilla de credenciales Google
└── tools/                       # Herramientas del agente
    ├── buscador_tool.py        # Búsqueda en internet
    ├── scraper_tool.py         # Web scraping
    ├── telegram_tool.py        # Mensajes a Telegram
    ├── bolsa_tool.py           # Precios de acciones
    ├── gmail_tool.py           # Envío de emails
    ├── image_generator_tool.py # Generación de imágenes
    ├── file_tool.py            # Manipulación de archivos
    ├── code_executor_tool.py   # Ejecución de Python
    ├── tts_tool.py             # Text-to-Speech
    └── audio_player_tool.py    # Reproductor de audio
```

## Cómo funciona

El agente utiliza **Function Calling** para determinar cuándo usar cada herramienta:

1. Recibes un mensaje del usuario
2. El modelo de IA decide si necesita usar alguna tool
3. Si es necesario, ejecuta la tool correspondiente
4. Procesa el resultado y responde al usuario

## APIs y Servicios utilizados

- **OpenRouter** - Acceso a modelos de IA (Grok, GPT, Claude, etc.)
- **Gmail API** - Envío de correos electrónicos
- **Telegram Bot API** - Mensajería
- **Replicate** - Generación de imágenes con IA
- **Yahoo Finance** - Datos bursátiles (a través de web scraping)

## Costos

- **Gmail API**: Gratis (100 emails/día)
- **Telegram**: Gratis
- **Replicate**: Pay-per-use (~$0.003 por imagen)
- **OpenRouter**: Varía según el modelo usado

## Licencia

MIT

