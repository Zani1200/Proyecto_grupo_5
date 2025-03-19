import streamlit as st
from streamlit_ui.login import mostrar_login
from streamlit_ui.uiAdmin import uiAdmin
from streamlit_ui.uiUser import uiUser


# Configuración de la página
st.set_page_config(page_title="Experiencias Viajeras", page_icon="🌍", layout="wide")

if "pagina" not in st.session_state:
    st.session_state.pagina = "Login"

if "usuario" not in st.session_state:
    usuario = st.session_state.usuario = None

# Verificar si la API Key está configurada - Quitamos esta condición porque nuestro usuario de Google Cloud no permite usar secretos
# if "OPENAI_API_KEY" not in st.secrets:
#     st.error("❌ No se encontró la API Key de OpenAI en secrets.toml. Por favor, configúrala.")
#     st.stop()


if st.session_state.pagina == 'Login':
    mostrar_login()
elif st.session_state.pagina == 'uiUser':
    uiUser()
else:
    uiAdmin()

