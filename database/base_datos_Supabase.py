
import os
import sys

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import supabase
from _datetime import datetime

from postgrest import APIError


from .usuarios import set_id_usuario


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
            "prompt": prompt_usuario,
            "respuesta_AI": respuesta_AI,
            "model": model,
            "tokens_consumidos": tokens,
            "error": error
        }

        self.client.table("openai_interactions").insert(data).execute()

    def extraer_interacciones_AI(self):
        interacciones = response = self.client.table("openai_interactions").select("*").execute()

        return interacciones.data

    def crear_usuario(self, apodo, correo, contraseña):
        try:
            timestamp = datetime.now().isoformat()
            rol = "admin" if apodo.lower() == "admin" else "user"
            usuario = {
                "apodo": apodo,
                "correo": correo,
                "contraseña": contraseña,
                "created_at": timestamp,
                "rol": rol
            }

            response = self.client.table("usuarios").insert(usuario).execute()
            set_id_usuario(response.data[0]["id"])
            return response
        except APIError:
            print("Ya existe un usuario con el mismo apodo")

    def borrar_usuario(self, id):
        response = self.client.table("usuarios").delete().eq("id", id).execute()

        return response

    def modificar_usuario(self, id, correo, contraseña):

        usuario_modificado = {
            "correo": correo,
            "contraseña": contraseña
        }

        response = self.client.table("usuarios").update(usuario_modificado).eq("id", id).execute()
        return response

    def consultar_usuario(self, id):
        response = self.client.table("usuarios").select().eq("id", id).execute()
        return response.data

    def listar_usuarios(self):
        response = self.client.table("usuarios").select("*").execute()
        if not response.data:
            print("No hay usuarios")
            return []
        else:
            return response.data

    def verificar_usuario(self, apodo, correo, contaseña):
        response = self.client.table("usuarios").select().eq("apodo", apodo).eq("correo", correo).eq("contraseña",contaseña).execute()
        if not response.data:
            return False
        return response.data[0]

    def insertar_pregunta_respuesta(self, variables: dict, respuesta: str, pregunta: str, id_usuario: int):
        response = self.client.table("variables_comunes").insert(variables).execute()

        id_variables_comunes = response.data[0]["id"]

        data_respuesta = {
            "respuesta": respuesta,
            "id_variables_comunes": id_variables_comunes
        }
        response_respuesta = self.client.table("respuesta").insert(data_respuesta).execute()

        id_respuesta = response_respuesta.data[0]["id"]

        data_pregunta = {
            "id_usuario": id_usuario,
            "pregunta": pregunta,
            "id_respuesta": id_respuesta,
            "id_variables_comunes": id_variables_comunes
        }
        response_pregunta = self.client.table("pregunta").insert(data_pregunta).execute()

        return {"message": "Pregunta y respuesta guardadas correctamente"}

    def listar_paises(self):
        response = self.client.table("variables_comunes").select("pais").execute()
        return response.data

    def preguntas_diarias(self):
        response = self.client.table("pregunta").select("created_at").execute()
        tiempo_preguntas = []
        for tiempo in response.data:
            tiempo_preguntas.append(tiempo.get("created_at"))
        return tiempo_preguntas

"""
if __name__ == "__main__":
    # Ejemplo de uso

    basedatos = BaseDatos()

    usuario = Usuario("example", "example@gmail.com", "example")

    basedatos.crear_usuario(usuario.apodo, usuario.correo, usuario.contraseña)
    basedatos.consultar_usuario(get_id_usuario())
    basedatos.modificar_usuario(get_id_usuario(), "exampleCambiado@gmail.com", "exampleCambiado")
    basedatos.listar_usuarios()
    basedatos.borrar_usuario(get_id_usuario())
    basedatos.listar_usuarios()

# Para probar la inserción
# Parámetros de prueba (test)

prompt = ("System: Eres un especialista en ocio y actividades culturales. Das respuestas breves y cortas, de unas 50 palabras como máximo"
          "\nUser: ¿Qué te apetece hacer hoy? Descríbemelo como te parezca.\n")

respuesta = ("Visita el Museo del Greco para disfrutar de su arte. Luego, relájate con un café en una acogedora cafetería del casco antiguo."
             " Perfecto para un día lluvioso.")
model = "gpt-3.5-turbo"
tokens = 125

basedatos.guarda_peticion_AI(prompt, respuesta, model, tokens, None)


# Para probar la extracción de datos imprimimos toda la información

interacciones = basedatos.extraer_interacciones_AI()
if not interacciones:
    print("\nNo hay datos")
else:
    for interaccion in interacciones:
        for interaccion in interacciones:
            print(f"ID: {interaccion.get('id')}")
            print(f"Fecha: {interaccion.get('created_at')}")
            print(f">> Prompt: {interaccion.get('prompt_usuario')}")
            print(f">> Respuesta: {interaccion.get('respuesta_AI')}")
            print(f"Modelo: {interaccion.get('model')}")
            print(f"Tokens: {interaccion.get('tokens_consumidos')}")
            print(f"Error: {interaccion.get('error')}")
            print("-" * 40)  # Separador entre registros

"""