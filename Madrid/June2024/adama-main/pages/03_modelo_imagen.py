import streamlit as st
import pandas as pd
import seaborn as sns
import os
import base64

st.header('Detección automática de vehículos')
st.caption('A través de este modelo, desde ADAMA somos capaces de determinar la intensidad de tráfico haciendo uso de YOLO. Con dicha variable y junto con las variables atmosféricas, seremos capaces de determinar el nivel de concentración de NO2 en la vía donde se encuentra la cámara.')

# Obtener la ruta del directorio del script actual
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# Construir las rutas completas a los archivos necesarios, subiendo un nivel desde 'pages'
base_dir = os.path.dirname(script_dir)  # Subir un nivel desde 'pages'

model_path = os.path.join(base_dir, "pickle_modelo", "xgboost_NO2.pkl")
video_path = os.path.join(base_dir, "data", "vehicles_detector.mp4")

# Comprobar si el archivo de video existe
if os.path.exists(video_path):
    # Leer el video y convertirlo a base64
    with open(video_path, 'rb') as video_file:
        video_bytes = video_file.read()
        encoded_video = base64.b64encode(video_bytes).decode()

    # Incrustar el video en HTML para reproducir automáticamente y en bucle, sin sonido
    video_html = f"""
        <video width="700" autoplay loop muted>
            <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
        </video>
        """
    st.markdown(video_html, unsafe_allow_html=True)
else:
    st.error(f"No se encontró el archivo de video en la ruta: {video_path}")
