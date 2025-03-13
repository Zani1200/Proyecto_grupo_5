import streamlit as st
import requests

from streamlit_ui.handler import cambiar_pagina
from streamlit_ui.uiAdmin import BASE_URL


def mostrar_login():
    st.title("🌍 Bienvenido a Experiencias Viajeras")
    st.write("""
    ¡Planifica tus viajes de manera inteligente y personalizada!
    Utiliza las opciones del menú para comenzar.
    """)

    st.title("Inicio de Sesión")
    with st.form(key="login_form"):
        usuario = st.text_input("Usuario")
        correo = st.text_input("Correo")
        contraseña = st.text_input("Contraseña", type="password")

        if st.form_submit_button("Iniciar sesión"):
            if usuario and correo and contraseña:
                st.session_state.usuario = {"usuario": usuario, "correo": correo}
                st.success("Inicio de sesión exitoso")
                if usuario.lower() == "admin":
                    cambiar_pagina("uiAdmin")
                else:
                    cambiar_pagina("uiUser")

                st.rerun()
            else:
                st.error("Por favor, completa todos los campos")
        if st.form_submit_button("Crear cuenta"):
            cambiar_pagina("uiAdmin")
            st.rerun()

"""
response = requests.get(f"{BASE_URL}/usuarios/listar/")
                data = response.json()
                for users in data:
                    if usuario == users["apodo"]:
                        st.error("Ya existe un usuario con ese apodo")
"""