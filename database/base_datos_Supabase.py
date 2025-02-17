import json
import os
import supabase
from datetime import datetime

class BaseDatos:
    def __init__(self):
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

    def guarda_peticion_AI(self, prompt_usuario, respuesta_AI, model, tokens, error):

        timestamp = datetime.now().isoformat()

        # Verifica que 'prompt_usuario' es un stringç
        if not isinstance(prompt_usuario, str):
            prompt_usuario = str(prompt_usuario)  # Convertir a string si no lo es

        # Verifica que 'respuesta' es un string
        if not isinstance(respuesta_AI, str):
            respuesta_AI = str(respuesta_AI)  # Convertir a string si no lo es

        data = {
            "created_at": timestamp,
            "prompt_usuario": prompt_usuario,
            "respuesta_AI": respuesta_AI,
            "model": model,
            "tokens_consumidos": tokens,
            "error": error
        }

        self.client.table("openai_interactions").insert(data).execute()

# Ejemplo de uso

# Parámetros de prueba
prompt = ("System: Eres un especialista en ocio y actividades culturales. Das respuestas breves y cortas, de unas 50 palabras como máximo"
          "\nUser: ¿Qué te apetece hacer hoy? Descríbemelo como te parezca.\n")

respuesta = ("Visita el Museo del Greco para disfrutar de su arte. Luego, relájate con un café en una acogedora cafetería del casco antiguo."
             " Perfecto para un día lluvioso.")
model = "gpt-3.5-turbo"
tokens = 125

basedatos = BaseDatos()
basedatos.guarda_peticion_AI(prompt, respuesta, model, tokens, None)