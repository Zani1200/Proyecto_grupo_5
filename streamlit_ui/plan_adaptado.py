import streamlit as st
from interfaces.generador_textos import GeneradorTextos
from modelos.modelo_gpt import ModeloGPT
from analisis.EnriquecerPeticionUsuario import procesar_peticion, obtener_ubicacion, obtener_hora_local
import json

def mostrar_plan_adaptado():
    st.title("📍 Plan Adaptado a Ti")

    # Obtener la API Key de OpenAI desde secrets.toml
    openai_api_key = st.secrets["OPENAI_API_KEY"]

    # Instanciar el modelo GPT
    modelo_gpt = ModeloGPT("GPT-4", "v1.0", openai_api_key)
    generador = GeneradorTextos()
    generador.agregar_modelo(modelo_gpt)

    # Obtener la ubicación y la hora configuradas por el usuario
    ubicacion = obtener_ubicacion()
    hora_local = obtener_hora_local()

    # Mostrar la ubicación y la hora actual
    st.write(f"📍 Ubicación actual: {ubicacion['ciudad']}, {ubicacion['pais']}")
    st.write(f"🕒 Hora actual: {hora_local}")

    # Entradas del usuario
    actividad = st.text_input("✍️ ¿Qué te gustaría hacer hoy? (Ejemplo: 'Quiero explorar museos')")
    estado_emocional = st.text_input("😊 ¿Cómo te sientes? (Ejemplo: 'Feliz', 'Cansado', 'Emocionado')")
    nivel_energia = st.selectbox("⚡ Nivel de energía", ["Bajo", "Medio", "Alto"])

    if st.button("Generar Plan"):
        if not actividad or not estado_emocional:
            st.error("❌ Por favor, ingresa una actividad y tu estado emocional.")
        else:
            try:
                datos_usuario = json.dumps({
                    "actividad": actividad,
                    "estado_emocional": estado_emocional,
                    "nivel_energia": nivel_energia.lower(),
                    "ubicacion": ubicacion,
                    "hora_local": hora_local
                })

                peticion_enriquecida = procesar_peticion(datos_usuario)
                resultado = generador.generar(peticion_enriquecida)

                if resultado and not resultado.startswith("❌"):
                    st.success("✅ Plan generado con éxito:")
                    st.write(resultado)
                else:
                    st.error("❌ Error al generar el plan. Detalles: " + resultado)

            except Exception as e:
                st.error(f"❌ Error inesperado: {str(e)}")

