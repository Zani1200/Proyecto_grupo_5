import os

import streamlit as st
from modelos.modelo_gpt import ModeloGPT
from analisis.EnriquecerPeticionUsuario import obtener_ubicacion, obtener_hora_local

def mostrar_experiencia_viajera():
    st.title("✈️ Solicitar una Experiencia Viajera")

    # Obtener la API Key de OpenAI desde secrets.toml
    openai_api_key = os.getenv("OPENAI_API_KEY")
    # Se comenta para usar en Google Cloud, donde no se pueden usar secrets con nuestro usuario
    # openai_api_key = st.secrets["OPENAI_API_KEY"]

    # Instanciar el modelo GPT
    modelo_gpt = ModeloGPT("GPT-4", "v1.0", openai_api_key)

    # Obtener la ubicación y la hora configuradas por el usuario
    ubicacion = obtener_ubicacion()
    hora_local = obtener_hora_local()

    # Mostrar la ubicación y la hora actual
    st.write(f"📍 Ubicación actual: {ubicacion['ciudad']}, {ubicacion['pais']}")
    st.write(f"🕒 Hora actual: {hora_local}")

    # Entrada del usuario
    peticion = st.text_input("✍️ ¿A dónde vas? (Ejemplo: 'Voy a Filipinas una semana')")

    if st.button("Generar Experiencia"):
        if not peticion:
            st.error("❌ Por favor, ingresa una petición.")
        else:
            # Generar la experiencia usando la ubicación y la hora configuradas
            prompt = f"""
            Genera una experiencia viajera en {peticion}.
            Ten en cuenta que el usuario está actualmente en {ubicacion['ciudad']}, {ubicacion['pais']},
            y la hora actual es {hora_local}.
            """
            respuesta = modelo_gpt.generar_texto(prompt)
            st.success("✅ Experiencia generada con éxito:")
            st.write(respuesta)