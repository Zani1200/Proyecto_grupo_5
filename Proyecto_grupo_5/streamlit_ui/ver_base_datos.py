import streamlit as st
from database.base_datos_Supabase import BaseDatos

def mostrar_base_datos():
    st.title("📂 Ver Base de Datos")

    # Instanciar la base de datos
    try:
        base_datos = BaseDatos()
        interacciones = base_datos.extraer_interacciones_AI()

        if interacciones:
            st.write("Interacciones almacenadas:")
            st.json(interacciones)
        else:
            st.info("ℹ️ No hay interacciones almacenadas en la base de datos.")
    except Exception as e:
        st.error(f"❌ Error al acceder a la base de datos: {e}")