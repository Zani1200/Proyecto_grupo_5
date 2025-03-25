import streamlit as st

from streamlit_ui.handler import cambiar_pagina
from streamlit_ui.login import mostrar_login
from streamlit_ui.plan_adaptado import mostrar_plan_adaptado
from streamlit_ui.experiencia_viajera import mostrar_experiencia_viajera
from streamlit_ui.uiAdmin import uiAdmin
from streamlit_ui.configuracion import mostrar_configuracion

def uiUser():
    # Menú de navegación
    if st.session_state.usuario["apodo"] == "admin":
        def mostrar_uiAdmin():
            cambiar_pagina("uiAdmin")
            st.rerun()

        opciones = {
            "Plan Adaptado": mostrar_plan_adaptado,
            "Experiencia Viajera": mostrar_experiencia_viajera,
            "Ubicación": mostrar_configuracion, # Cambiado de "Configuración" a "Ubicación"
            "Consola de Administración": mostrar_uiAdmin
        }
    else:
        opciones = {
            "Plan Adaptado": mostrar_plan_adaptado,
            "Experiencia Viajera": mostrar_experiencia_viajera,
            "Ubicación": mostrar_configuracion,  # Cambiado de "Configuración" a "Ubicación"
        }

    # Sidebar para navegación
    st.sidebar.title("Navegación")
    seleccion = st.sidebar.radio("Ir a", list(opciones.keys()))

    # Mostrar la página seleccionada
    opciones[seleccion]()