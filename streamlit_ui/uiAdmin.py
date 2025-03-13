import datetime


import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
from streamlit_ui.handler import cambiar_pagina

BASE_URL = "http://localhost:8000"  # Cambia esto si FastAPI corre en otro host/puerto

# Manera inicial de crear el título y el menú

# st.title("👤 Gestión de Usuarios")  # Icono en el título
#pi
# menu = st.sidebar.selectbox("Selecciona una opción", [
#     "Crear Usuario", "Obtener Usuario", "Actualizar Usuario", "Eliminar Usuario", "Listar Usuarios"
# ])


def uiAdmin():
    # Creamos el título usando markdown para controlar el icono que añadimos

    # Obtenemos los iconos de https://icons.getbootstrap.com/
    st.markdown(
        """
        <h1>
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16">
                <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001m-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708z"/>
            </svg>
            Gestión de Usuarios
        </h1>
        """,
        unsafe_allow_html=True
    )
    # Menú lateral con iconos
    with st.sidebar:
        if isinstance(st.session_state.usuario, dict): #con esto manejo si el usuario es admin o un user
            menu = option_menu(
                "Menú",  # Título del menú lateral
                ["Crear Usuario", "Obtener Usuario", "Actualizar Usuario", "Eliminar Usuario", "Listar Usuarios", "Metrica"],  # Opciones
                icons=["person-add", "person-gear", "person-up", "person-dash", "person-lines-fill"],  # Iconos de Bootstrap
                menu_icon="menu-button-wide",  # Icono del menú principal
                default_index=0,  # Opción por defecto
                orientation="vertical"  # Asegura que el menú se muestre en la barra lateral
            )
        else:
            menu = option_menu(
                "Menú",  # Título del menú lateral
                ["Crear Usuario", "Metrica"],  # Opciones, la metrica hay que quitarla de aqui pero esta solo para hacer pruebas
                icons=["person-add", "person-gear", "person-up", "person-dash", "person-lines-fill"],  # Iconos de Bootstrap
                menu_icon="menu-button-wide",  # Icono del menú principal
                default_index=0,  # Opción por defecto
                orientation="vertical"  # Asegura que el menú se muestre en la barra lateral
            )

    if menu == "Crear Usuario":
        # Usamos markdown para cabecera con icono extraído de https://icons.getbootstrap.com/
        st.markdown(
            """
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7m.5-5v1h1a.5.5 0 0 1 0 1h-1v1a.5.5 0 0 1-1 0v-1h-1a.5.5 0 0 1 0-1h1v-1a.5.5 0 0 1 1 0m-2-6a3 3 0 1 1-6 0 3 3 0 0 1 6 0M8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4"/>
                    <path d="M8.256 14a4.5 4.5 0 0 1-.229-1.004H3c.001-.246.154-.986.832-1.664C4.484 10.68 5.711 10 8 10q.39 0 .74.025c.226-.341.496-.65.804-.918Q8.844 9.002 8 9c-5 0-6 3-6 4s1 1 1 1z"/>
                </svg> Crear Nuevo Usuario
            </h2>
            """,
            unsafe_allow_html=True
        )
        apodo = st.text_input("Apodo")
        correo = st.text_input("Correo electrónico")
        contraseña = st.text_input("Contraseña", type="password")

        if st.button("Crear Usuario"):
            response = requests.post(f"{BASE_URL}/usuarios/crear/", json={
                "apodo": apodo,
                "correo": correo,
                "contraseña": contraseña
            })
            st.write(response.json())

            cambiar_pagina("Login")
            st.rerun()


    elif menu == "Obtener Usuario":
        # Usamos markdown para cabecera con icono extraído de https://icons.getbootstrap.com/
        st.markdown(
            """
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-person-check" viewBox="0 0 16 16">
                    <path d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7m1.679-4.493-1.335 2.226a.75.75 0 0 1-1.174.144l-.774-.773a.5.5 0 0 1 .708-.708l.547.548 1.17-1.951a.5.5 0 1 1 .858.514M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0M8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4"/>
                    <path d="M8.256 14a4.5 4.5 0 0 1-.229-1.004H3c.001-.246.154-.986.832-1.664C4.484 10.68 5.711 10 8 10q.39 0 .74.025c.226-.341.496-.65.804-.918Q8.844 9.002 8 9c-5 0-6 3-6 4s1 1 1 1z"/>
                </svg> Consultar usuario por ID
            </h2>
            """,
            unsafe_allow_html=True
        )
        user_id = st.number_input("ID de usuario", min_value=1, step=1)
        if st.button("Buscar Usuario"):
            response = requests.get(f"{BASE_URL}/usuarios/{user_id}")
            st.write(response.json())

    elif menu == "Actualizar Usuario":
        # Cabecera con icono extraído de https://icons.getbootstrap.com/icons/person-gear/
        st.markdown(
            """
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-person-gear" viewBox="0 0 16 16">
                    <path d="M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0M8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4m.256 7a4.5 4.5 0 0 1-.229-1.004H3c.001-.246.154-.986.832-1.664C4.484 10.68 5.711 10 8 10q.39 0 .74.025c.226-.341.496-.65.804-.918Q8.844 9.002 8 9c-5 0-6 3-6 4s1 1 1 1zm3.63-4.54c.18-.613 1.048-.613 1.229 0l.043.148a.64.64 0 0 0 .921.382l.136-.074c.561-.306 1.175.308.87.869l-.075.136a.64.64 0 0 0 .382.92l.149.045c.612.18.612 1.048 0 1.229l-.15.043a.64.64 0 0 0-.38.921l.074.136c.305.561-.309 1.175-.87.87l-.136-.075a.64.64 0 0 0-.92.382l-.045.149c-.18.612-1.048.612-1.229 0l-.043-.15a.64.64 0 0 0-.921-.38l-.136.074c-.561.305-1.175-.309-.87-.87l.075-.136a.64.64 0 0 0-.382-.92l-.148-.045c-.613-.18-.613-1.048 0-1.229l.148-.043a.64.64 0 0 0 .382-.921l-.074-.136c-.306-.561.308-1.175.869-.87l.136.075a.64.64 0 0 0 .92-.382zM14 12.5a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0"/>
                </svg> Actualizar datos de usuario
            </h2>
            """,
            unsafe_allow_html=True
        )
        user_id = st.number_input("ID de usuario", min_value=1, step=1)
        nuevo_correo = st.text_input("Nuevo correo electrónico (opcional)")
        nueva_contraseña = st.text_input("Nueva contraseña (opcional)", type="password")

        if st.button("Actualizar Usuario"):
            response = requests.put(f"{BASE_URL}/usuarios/{user_id}", json={
                "correo": nuevo_correo if nuevo_correo else None,
                "contraseña": nueva_contraseña if nueva_contraseña else None
            })
            st.write(response.json())

    elif menu == "Eliminar Usuario":
        # Usamos markdown para cabecera con icono extraído de https://icons.getbootstrap.com/
        st.markdown(
            """
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-person-dash" viewBox="0 0 16 16">
                    <path d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M11 12h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1 0-1m0-7a3 3 0 1 1-6 0 3 3 0 0 1 6 0M8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4"/>
                    <path d="M8.256 14a4.5 4.5 0 0 1-.229-1.004H3c.001-.246.154-.986.832-1.664C4.484 10.68 5.711 10 8 10q.39 0 .74.025c.226-.341.496-.65.804-.918Q8.844 9.002 8 9c-5 0-6 3-6 4s1 1 1 1z"/>
                </svg> Eliminar usuario por ID
            </h2>
            """,
            unsafe_allow_html=True
        )
        user_id = st.number_input("ID de usuario", min_value=1, step=1)
        if st.button("Eliminar Usuario"):
            response = requests.delete(f"{BASE_URL}/usuarios/{user_id}")
            st.write(response.json())

    elif menu == "Listar Usuarios":
        # Cabecera con icono extraído de https://icons.getbootstrap.com/icons/person-lines-fill/
        st.markdown(
            """
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-person-lines-fill" viewBox="0 0 16 16">
                    <path d="M6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6m-5 6s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zM11 3.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5m.5 2.5a.5.5 0 0 0 0 1h4a.5.5 0 0 0 0-1zm2 3a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1z"/>
                </svg> Listado completo de usuarios
            </h2>
            """,
            unsafe_allow_html=True
        )
        if st.button("Cargar Usuarios"):
            response = requests.get(f"{BASE_URL}/usuarios/listar/")
            data = response.json()  # Convertimos la respuesta a JSON

            if isinstance(data, list):  # Verificamos que la respuesta sea una lista de usuarios
                df = pd.DataFrame(data)
                st.dataframe(df)  # Mostrar en una tabla interactiva
            else:
                st.error("Error al cargar los usuarios")
                st.json(data)  # Mostrar el error en JSON para depuración

            # st.write(response.json()) #Antigua salida del metodo en JSON crudo
    elif menu == "Metrica":
        col1,col2 = st.columns(2)
        with col1:
            paises = st.session_state.paises = {
                "España": 5,
                "Francia": 2,
                "Colombia": 4,
                "Inglaterra": 1
            }

            # Convertir el diccionario en un DataFrame
            df = pd.DataFrame(list(paises.items()), columns=["País", "Visitas"])
            # Crear el gráfico de pastel
            fig = px.pie(df, names="País", values="Visitas", title="Países más visitados")

            # Mostrar en Streamlit
            st.plotly_chart(fig)
        with col2:
            if "metricas" not in st.session_state:
                st.session_state.preguntas = []

            # Función para agregar nueva métrica diaria
            def actualizar_metricas():
                hoy = datetime.date.today()
                mañana = datetime.date.today() + datetime.timedelta(days=1)

                # Eliminar datos más antiguos de 30 días
                st.session_state.preguntas = [m for m in st.session_state.preguntas if
                                    m["fecha"] >= hoy - datetime.timedelta(days=30)]

                # Agregar nueva métrica del día (simulación)
                nueva_metrica = {
                    "fecha": hoy,
                    "preguntas": 5,  # Aquí pondrías un query real a la base de datos
                }
                st.session_state.preguntas.append(nueva_metrica)
                nueva_metrica_mañana = {
                    "fecha": mañana,
                    "preguntas": 2,
                }
                st.session_state.preguntas.append(nueva_metrica_mañana)


            actualizar_metricas() # para que se actualice al entrar

            # Mostrar datos
            df = pd.DataFrame(st.session_state.preguntas, columns=["fecha", "preguntas"])
            fig = px.line(df,x="fecha",y="preguntas",title="Preguntas diarias")
            st.plotly_chart(fig)

            # Botón para actualizar
            if st.button("Actualizar métricas"):
                actualizar_metricas()

