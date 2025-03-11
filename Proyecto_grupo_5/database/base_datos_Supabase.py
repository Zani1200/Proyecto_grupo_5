import os
import sys
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import supabase
from datetime import datetime
from postgrest import APIError
from .usuarios import set_id_usuario


class BaseDatos:
    def __init__(self):
        SUPABASE_URL = st.secrets.get("SUPABASE_URL")
        SUPABASE_KEY = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY")
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

