import streamlit as st
from database.base_datos_Supabase import BaseDatos

def mostrar_base_datos():
    st.title("📂 Consulta de interacciones con la IA")

    # Instanciar la base de datos
    try:
        base_datos = BaseDatos()
        interacciones = base_datos.extraer_interacciones_AI()

        if interacciones:
            st.write("Listado de interacciones almacenadas:")
            # st.json(interacciones)

            # Se utiliza expander para mostrar textos largos de forma amigable
            # Invertir la lista para mostrar los más recientes primero
            for i, interaccion in enumerate(interacciones[::-1]):
                with st.expander(f"🆕 Interacción {len(interacciones) - i}"):  # Ajusta el número de la interacción
                    for clave, valor in interaccion.items():
                        st.markdown(f"**{clave}:** {valor}")
                    st.markdown("---")  # Separador visual

        else:
            st.info("ℹ️ No hay interacciones almacenadas en la base de datos.")
    except Exception as e:
        st.error(f"❌ Error al acceder a la base de datos: {e}")