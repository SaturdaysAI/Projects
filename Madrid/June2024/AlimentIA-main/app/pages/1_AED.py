import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title='Demo de la fase de análisis exploratorio de datos', 
    layout='wide',
    page_icon="📈",
    initial_sidebar_state='expanded'
    )

# Barra lateral con Logo, selección de modelo y nubes de palabras
with st.sidebar:
    st.header('Gráficos')
    # Desplegable para nubes de palabras (esto se manejará en otro fragmento de código)
    options = [
        'Antes de la limpieza',
        'Preprocesado',
        'Después de la limpieza',
        'Clustering'
    ]
    selected = st.selectbox('Selecciona un ámbito', options)
    st.write("---")
    st.image('logo.png', width=200)
    st.write("---")
    st.write('Andrés Peñafiel Rodas \n andres.pennafiel@gmail.com')
    st.write('David Monroy \n monroygonzalezdavid@gmail.com')
    st.write('Pablo Tomás \n 93pablotr@gmail.com')
    st.write('Mayra \n andres.pennafiel@gmail.com')
    st.write('Sergio Serna \n sgsernac@gmail.com')

# Títulos y métricas en el cuerpo principal
st.header(selected)
st.write('---')

if selected == 'Antes de la limpieza':
    cols = st.columns(6)
    for i, col in enumerate(cols):
        if i == 0:
            # centrar el st.caption y la imagen
            st.image('Frecuencia de ventas de familias de productos.png')
        if i == 1:
            st.image('Frecuencia de ventas de productos.png')
        if i == 2:
            st.image('Frecuencia de ventas por día.png')
        if i == 3:
            st.image('Frecuencia de ventas por semana.png')
        if i == 4:
            st.image('Frecuencia de ventas por mes.png')
        if i == 5:
            st.image('Ventas por fecha.png')

if selected == 'Preprocesado':
    #Contenedores para gráficos dispuestos en 1 columnas y tres filas
    cols = st.columns(1)
    for i, col in enumerate(cols):
        if i == 0:
            # centrar el st.caption y la imagen
            st.image('Muestras del conjunto de datos preprocesado.png')
        
if selected == 'Después de la limpieza':
    #Contenedores para gráficos
    cols = st.columns(4)
    for i, col in enumerate(cols):
        if i == 0:
            st.image('Frecuencia de ventas por dia preprocesado.png')
        if i == 1:
            st.image('Frecuencia de ventas por mes preprocesado copy.png')
        if i == 2:
            st.image('Frecuencia de ventas por hora.png')

if selected == 'Clustering':
    #Contenedores para gráficos
    cols = st.columns(3)
    for i, col in enumerate(cols):
        if i == 0:
            st.image('calinski scores dataset preprocesado.png')
        if i == 1:
            st.image('davies scores dataset preprocesado.png')
        if i == 2:
            st.image('Clusters dataset preprocesado.png')
