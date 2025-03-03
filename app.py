import streamlit as st
from streamlit_ui.home import mostrar_home
from streamlit_ui.plan_adaptado import mostrar_plan_adaptado
from streamlit_ui.experiencia_viajera import mostrar_experiencia_viajera
from streamlit_ui.ver_base_datos import mostrar_base_datos
from streamlit_ui.configuracion import mostrar_configuracion  # Importación de la página de configuración

# Configuración de la página
st.set_page_config(page_title="Experiencias Viajeras", page_icon="🌍", layout="wide")

# Verificar si la API Key está configurada
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ No se encontró la API Key de OpenAI en secrets.toml. Por favor, configúrala.")
    st.stop()

# Menú de navegación
opciones = {
    "Inicio": mostrar_home,
    "Plan Adaptado": mostrar_plan_adaptado,
    "Experiencia Viajera": mostrar_experiencia_viajera,
    "Ver Base de Datos": mostrar_base_datos,
    "Ubicación": mostrar_configuracion,  # Cambiado de "Configuración" a "Ubicación"
}

# Sidebar para navegación
st.sidebar.title("Navegación")
seleccion = st.sidebar.radio("Ir a", list(opciones.keys()))

# Mostrar la página seleccionada
opciones[seleccion]()