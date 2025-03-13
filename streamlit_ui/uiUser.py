import streamlit as st
from streamlit_ui.login import mostrar_login
from streamlit_ui.plan_adaptado import mostrar_plan_adaptado
from streamlit_ui.experiencia_viajera import mostrar_experiencia_viajera
from streamlit_ui.ver_base_datos import mostrar_base_datos
from streamlit_ui.configuracion import mostrar_configuracion

def uiUser():
    # Menú de navegación
    opciones = {
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