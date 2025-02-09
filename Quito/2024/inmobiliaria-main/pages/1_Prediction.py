import pandas as pd
import numpy as np
import os
import json
import requests
import streamlit as st
import components.authenticate as authenticate
from config.conexionDb import conn
from pathlib import Path
from PIL import Image

import warnings
warnings.filterwarnings("ignore")

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


# Check authentication
authenticate.set_st_state_vars()

# Add login/logout buttons
if st.session_state["authenticated"]:
    authenticate.button_logout()
else:
    authenticate.button_login()

    
if (st.session_state["authenticated"]  

    ):
    # Ruta a tu imagen de fondo
    img_path = Path("data/data.jpg")

    st.markdown("<h1 style='text-align: center;'>INMOBILIARIA</h1>", unsafe_allow_html=True)


    col1, col2, col3 = st.columns(3)
    
    img_path_1 = Path("data/people.png")
    image_path_1 = Path(img_path_1)
    with col1:
        if image_path_1.is_file():
            st.image(image_path_1.as_posix(),  use_container_width=True)
        else:
            st.write("El archivo de imagen no se encontró.")
            
    img_path_2 = Path("data/house.png")
    image_path_2 = Path(img_path_2)
    with col2:
        if image_path_2.is_file():
            st.image(image_path_2.as_posix(),  use_container_width=True)
        else:
            st.write("El archivo de imagen no se encontró.")
            
    img_path_3 = Path("data/predictive.png")
    image_path_3 = Path(img_path_3)
    with col3:
        if image_path_3.is_file():
            st.image(image_path_3.as_posix(), use_container_width=True)
        else:
            st.write("El archivo de imagen no se encontró.")


    st.write("Introduce los valores de tus variables:")
    
    query = """
            select distinct "LOCALIZACIONDELBIEN" 
                from "REMATES_INTERNO" ri
                order by "LOCALIZACIONDELBIEN" asc
        """
    data = pd.read_sql(query,conn)
    data[['PROVINCIAS', 'CANTONES']] = data['LOCALIZACIONDELBIEN'].str.split(',', expand=True)

    # Crear diccionario para almacenar las provincias y sus cantones
    provincias_dic = {}

    # Agrupar cantones por provincia y almacenar en el diccionario
    for provincia, cantones in data.groupby('PROVINCIAS')['CANTONES']:
        provincias_dic[provincia] = list(cantones)

    col1, col2 = st.columns(2)


    with col1:
        options_p = data['PROVINCIAS'].unique().tolist()
        provincia = st.selectbox("Selecciona una Provincia",options_p)
        options_c = provincias_dic[provincia]
        canton = st.selectbox("Selecciona un Cantón",options_c)
        area_p = st.number_input('AREA PROPIEDAD',min_value=0.0)
        caracteristicas = st.text_input('CARACTERÍSTICAS')

    with col2:
        options = [
                "Terreno",
                "Departamento",
                # "Edificio",
                # "Finca",
                # "Suite",
                "Casa",
                # "Oficina",
                # "Derechos y Acciones"
                ]
        tipo = st.selectbox("Selecciona una opción", options)
        options_ = [
                "Primer Señalamiento",
                # "Segundo Señalamiento",
                "Tercer Señalamiento",
                # "Otro Señalamiento",
                # "Retasa de Bienes"
                ]
        signage = st.selectbox("Selecciona una opción", options_)
        area_c = st.number_input('AREA CONSTRUCCION',min_value=0.0)
        



    
    provincia_canton = f'{provincia.upper()}' + ' ' + f'{canton.upper()}'
    provincia_canton_ = f'{provincia.lower()}' + ' ' + f'{canton.lower()}'
    
    texture = f'{provincia_canton_}'+' '+f'{caracteristicas}'
    texture = texture.replace(',','')

    url = "https://uniajfk7o3.execute-api.us-east-1.amazonaws.com/Dev/prediccion"

    payload = json.dumps({
    "data": f"{provincia_canton},{tipo},{signage},{texture},{area_p},{area_c}"
    })

    headers = {
    'Content-Type': 'application/json'
    }


    if st.button('Procesar'):
        try:
            data = json.loads(payload)
            df = pd.DataFrame([data])
            # st.write(df)
            
            response = requests.request("POST", url, headers=headers, data=payload)
            result = np.float64(response.text)
            result = abs(result)
            

            print(result)
            st.success(f'El avalúo estimado con las características ingresadas es: {"{:,.2f}".format(result)} USD')
            # st.write(result)
        except json.JSONDecodeError:
            st.error('Error al procesar el JSON. Asegúrate de que el formato es correcto.')
        except Exception as e:
            st.error(f'Error al predecir: {e}')

    # Directorio donde se almacenarán las imágenes
    upload_dir = "data/"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)


    # Cargar una imagen desde el disco local 
    uploaded_file = st.file_uploader("Elige una imagen", type=["png", "jpg", "jpeg"]) 


    # Almacenar la imagen si se ha cargado un archivo válido
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_path = os.path.join(upload_dir, uploaded_file.name)
        image.save(image_path)
        st.success(f"Imagen almacenada en: {image_path}")
    # HTML y CSS para la marca "Powered by" 


#     st.button("Re-run")
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
