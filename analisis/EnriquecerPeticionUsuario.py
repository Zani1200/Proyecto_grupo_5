import json
import requests
import streamlit as st
from datetime import datetime

def obtener_ubicacion():
    """Obtiene la ubicación configurada por el usuario."""
    if "ubicacion" in st.session_state:
        return st.session_state["ubicacion"]
    else:
        return {"ciudad": "Oranjestad", "pais": "Aruba"}  # Valores por defecto

def obtener_hora_local():
    """Obtiene la hora configurada por el usuario."""
    if "hora_actual" in st.session_state:
        return st.session_state["hora_actual"].strftime("%H:%M")
    else:
        return datetime.now().strftime("%H:%M")  # Hora actual del sistema

def obtener_clima(ciudad, pais):
    """Obtiene el clima y la temperatura actual desde OpenWeatherMap."""
    try:
        api_key = st.secrets["OPENWEATHERMAP_API_KEY"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad},{pais}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temperatura = data["main"]["temp"]
            condicion = data["weather"][0]["description"]
            return {"temperatura": f"{temperatura}°C", "condición": condicion}
        else:
            print(f"Error al obtener el clima: {data.get('message', 'Error desconocido')}")
            return {"temperatura": "desconocida", "condición": "desconocida"}

    except Exception as e:
        print(f"Error al obtener el clima: {e}")
        return {"temperatura": "desconocida", "condición": "desconocida"}


def obtener_estado_emocional(texto):
    """Simula la obtención del estado emocional."""
    return "Feliz"

def procesar_peticion(peticion_json):
    """Procesa la petición del usuario y la enriquece con información adicional."""
    try:
        peticion = json.loads(peticion_json)
        peticion_usuario = peticion.get("actividad")
        nivel_energia = peticion.get("nivel_energia")
        ubicacion = obtener_ubicacion()

        # Obtener el clima y la temperatura actual
        clima = obtener_clima(ubicacion["ciudad"], ubicacion["pais"])

        respuesta = {
            "peticion_usuario": peticion_usuario,
            "nivel_energia": nivel_energia,
            "estado_emocional": obtener_estado_emocional(peticion_usuario),
            "ubicacion": ubicacion,
            "tiempo": clima,
            "hora_local": obtener_hora_local()
        }

        return json.dumps(respuesta, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"❌ Error al procesar la petición: {e}")
        return json.dumps({"error": "No se pudo procesar la petición"})
