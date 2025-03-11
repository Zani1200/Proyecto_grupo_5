import streamlit as st

def mostrar_configuracion():
    st.title("📍 Configurar Ubicación")

    # Configurar ubicación
    st.subheader("📍 Configurar Ubicación Actual")
    ciudad = st.text_input("Ciudad", value="Oranjestad")
    pais = st.text_input("País", value="Aruba")

    # Guardar configuración en session_state
    if st.button("Guardar Ubicación"):
        st.session_state["ubicacion"] = {"ciudad": ciudad, "pais": pais}
        st.success(f"✅ Tu ubicación actual ha sido cambiada a **{ciudad}**, ubicada en **{pais}**.")

    # Mostrar ubicación actual
    if "ubicacion" in st.session_state:
        st.write("**Ubicación actual:**", st.session_state["ubicacion"])