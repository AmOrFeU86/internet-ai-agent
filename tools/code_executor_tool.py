import sys
import io
import contextlib
import traceback
from typing import Any

def execute_python(code):
    """
    Ejecuta código Python dinámicamente y retorna el resultado

    ADVERTENCIA DE SEGURIDAD:
    Esta herramienta ejecuta código Python arbitrario. Solo úsala en entornos
    controlados y de confianza. No ejecutes código de fuentes no confiables.

    Args:
        code (str): Código Python a ejecutar

    Returns:
        str: Resultado de la ejecución (stdout, resultado de expresiones, o errores)
    """
    try:
        # Crea buffers para capturar stdout y stderr
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()

        # Variable para guardar el resultado de la última expresión
        result = None

        # Contexto para capturar la salida
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            try:
                # Intenta compilar y ejecutar el código
                # Usamos compile() para distinguir entre expresiones y statements
                try:
                    # Primero intenta como expresión (para cosas como "2 + 2")
                    compiled = compile(code, '<string>', 'eval')
                    result = eval(compiled)
                except SyntaxError:
                    # Si falla, intenta como statement(s) (para código con múltiples líneas)
                    compiled = compile(code, '<string>', 'exec')
                    # Crea un namespace local para la ejecución
                    local_vars = {}
                    exec(compiled, {"__builtins__": __builtins__}, local_vars)

                    # Si hay una variable 'result' en el namespace, úsala
                    if 'result' in local_vars:
                        result = local_vars['result']

            except Exception as e:
                # Captura errores de ejecución
                stderr_buffer.write(f"Error durante la ejecución:\n{traceback.format_exc()}")

        # Recopila toda la salida
        stdout_output = stdout_buffer.getvalue()
        stderr_output = stderr_buffer.getvalue()

        # Construye la respuesta
        response_parts = []

        # Si hubo salida en stdout
        if stdout_output:
            response_parts.append(f"--- OUTPUT ---\n{stdout_output.strip()}")

        # Si hay un resultado de expresión
        if result is not None:
            response_parts.append(f"--- RESULTADO ---\n{result}")

        # Si hubo errores
        if stderr_output:
            response_parts.append(f"--- ERROR ---\n{stderr_output.strip()}")
            return "❌ Error al ejecutar el código:\n\n" + "\n\n".join(response_parts)

        # Si no hubo salida ni resultado
        if not response_parts:
            return "✓ Código ejecutado exitosamente (sin output)"

        return "✓ Código ejecutado exitosamente:\n\n" + "\n\n".join(response_parts)

    except Exception as e:
        return f"❌ Error inesperado al ejecutar el código:\n{str(e)}\n\n{traceback.format_exc()}"


# Definición de la tool para el modelo
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "execute_python",
        "description": "Ejecuta código Python dinámicamente y retorna el resultado. Usa esta herramienta para cálculos, procesamiento de datos, operaciones matemáticas complejas, o cualquier tarea que requiera ejecutar código Python. Ejemplos: 'calcula la factorial de 50', 'genera una lista de números primos menores que 100', 'procesa estos datos con Python'. IMPORTANTE: El código debe ser Python válido.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Código Python a ejecutar. Puede ser una expresión simple (ej: '2 + 2') o código de múltiples líneas. Si quieres retornar un valor específico, asígnalo a la variable 'result'. Ejemplo: 'result = sum([1,2,3,4,5])'"
                }
            },
            "required": ["code"]
        }
    }
}
