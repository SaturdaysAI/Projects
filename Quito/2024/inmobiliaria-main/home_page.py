import streamlit as st
import components.authenticate as authenticate
import warnings
warnings.filterwarnings("ignore")
from PIL import Image
from pathlib import Path


st.set_page_config(
    page_title = 'INMILIARIA',
    layout = 'wide',
    page_icon = ':derelict_house_building:'
)




## PARA LA IMAGEN DE FONDO        
st.markdown(
"""
<style>
.stApp {
    background-image: url("http://gseii.org/site/wp-content/uploads/2014/05/dark_blue_gradient_by_msketchley-d3gs0d8.jpg");
    background-size: cover;
}
</style>
""",
unsafe_allow_html=True
)


st.markdown("<h1 style='text-align: center;'>Bienvenido a Epsilon Data</h1>", unsafe_allow_html=True)




st.markdown("""
            **La solución inteligente para identificar oportunidades de inversión óptimas.**
            """)

st.write("""Desarrollar un modelo de predicción automatizado que estime el valor y la rentabilidad de inmuebles en remate 
        (casas, terrenos, departamentos) con base en descripciones nuevas, proporcionando una clasificación precisa de la 
        rentabilidad en categorías de alta, media o baja para optimizar la toma de decisiones en inversiones inmobiliarias. """)



st.markdown(
    """
    **👈 Inicie sesión y seleccione una página del sidebar** 

"""
)


col1, col2, col3 = st.columns(3)

img_path_2 = Path("static/inteligencia-artificial.png")
image_path_2 = Path(img_path_2)
with col2:
    if image_path_2.is_file():
        st.image(image_path_2.as_posix(),  use_container_width=True)
    else:
        st.write("El archivo de imagen no se encontró.")
        



# HTML y CSS para la marca "Powered by" 
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

st.markdown(powered_by, unsafe_allow_html=True)

authenticate.set_st_state_vars()

if st.session_state["authenticated"]:
    authenticate.button_logout()    
else:
    authenticate.button_login()

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
