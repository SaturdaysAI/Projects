import streamlit as st
from pathlib import Path
import components.authenticate as authenticate
import warnings
warnings.filterwarnings("ignore")


st.set_page_config(
    page_title = 'INMILIARIA',
    layout = 'wide',
    page_icon = ':derelict_house_building:'
)

# Check authentication
authenticate.set_st_state_vars()

# Add login/logout buttons
if st.session_state["authenticated"]:
    authenticate.button_logout()
else:
    authenticate.button_login()
    
if (st.session_state["authenticated"]):

    image_path = "data/page2_3.jpg"
    
    # st.title("Inversión") 
    image_path = Path(image_path)
    col1, col2, col3 = st.columns(3)
    with col2:
        st.title("Inversión")
        st.header("Página en Construcción") 

        if image_path.is_file():
            st.image(image_path.as_posix(), use_container_width=True)
        else:
            st.write("El archivo de imagen no se encontró.")
            
        st.write("¡Estamos trabajando en algo increíble!") 
        st.write("Por favor, vuelve pronto para más actualizaciones.")

    # st.button("Re-run")
else:
    if st.session_state["authenticated"]:
        st.write("Usted no tene Acceso. Por favor, contáctece con el Administrador.")
    else:
        st.write("Por favor, realizar el login!")

powered_by = """ <div style="position: fixed; 
                bottom: 0; 
                right: 0; 
                width: 100%; 
                background-color: #f8f9fa; 
                text-align: right; 
                padding: 10px 20px; 
                font-size: 12px; 
                color: #6c757d;"> 
                Powered by <a href="https://sites.google.com/view/epsilon-data/" 
                target="_blank">[Epsilon Data]</a> 
                </div> """ 

# Agregar el HTML a la aplicación 
st.markdown(powered_by, unsafe_allow_html=True)

for _ in range(18):
    st.sidebar.write("")


logo_html = f"""
<div style="display: flex; align-items: center;">
    <a href="https://sites.google.com/view/epsilon-data/">
    <img src="app/static/icono_nombre.png" alt="logo" width=300 height=215>
    </a>
    <span style="font-size: 8px; font-weight: bold; color:black;"></span>
</div>
"""
st.sidebar.markdown(logo_html,unsafe_allow_html=True)
