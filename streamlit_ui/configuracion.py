import streamlit as st

# Valor por defecto para la ubicación
def mostrar_configuracion():
    st.title("📍 Configurar Ubicación")

    # Configurar ubicación
    st.subheader("📍 Configurar Ubicación Actual")

    # Si ya tenemos ubicación guardada, la mostramos. Si no, se usan los valores por defecto
    ubicacion = {"ciudad": "Oranjestad", "pais": "Aruba"}
    if "ubicacion" in st.session_state:
        ubicacion = st.session_state["ubicacion"]

    ciudad = st.text_input("Ciudad", value=ubicacion['ciudad'])
    pais = st.text_input("País", value=ubicacion['pais'])

    # Guardar configuración en session_state
    if st.button("Guardar Ubicación"):
        st.session_state["ubicacion"] = {"ciudad": ciudad, "pais": pais}
        st.success(f"✅ Tu ubicación actual ha sido cambiada a **{ciudad}**, ubicada en **{pais}**.")

    # Mostrar ubicación guardada
    if "ubicacion" in st.session_state:
        ubicacion = st.session_state["ubicacion"]
        st.markdown(
            f"<p style='font-size:28px;'>Ubicación guardada: {ubicacion['ciudad']}, {ubicacion['pais']}.</p>",
            unsafe_allow_html=True
        )