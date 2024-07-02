import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title='Machine Learning Demo', 
    page_icon=":robot_face:",
    initial_sidebar_state="expanded"
    )

# Barra lateral con Logo, selección de modelo y nubes de palabras
with st.sidebar:
    st.header('Gráficos')
    # Desplegable para nubes de palabras (esto se manejará en otro fragmento de código)
    options = [
        'Aceites',
        'Bebidas',
        'Bocadillos',
        'Bolsas',
        'CC- Corte a cuchillo',
        'Embutidos en tercios',
        'Hornazos',
        'Merma',
        'MQ-Corte tradicional',
        'Panadería',
        'PE - Patas enteras',
        'Quesos',
        'Servicios',
        'Snacks',
        'Sobres al vacío',
        'Varios',
        'Vinos'
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

if selected == 'Aceites':
    st.image('Gráfico de líneas de la familia Aceites.png')
if selected == 'Bebidas':
    st.image('Gráfico de líneas de la familia Bebidas.png')
if selected == 'Bocadillos':
    st.image('Gráfico de líneas de la familia Bocadillos.png')
if selected == 'Bolsas':
    st.image('Gráfico de líneas de la familia Bolsas.png')
if selected == 'CC- Corte a cuchillo':
    st.image('Gráfico de líneas de la familia CC - Corte a cuchillo.png')
if selected == 'Embutidos en tercios':
    st.image('Gráfico de líneas de la familia Embutidos en tercios.png')
if selected == 'Hornazos':
    st.image('Gráfico de líneas de la familia Hornazos.png')
if selected == 'Merma':
    st.image('Gráfico de líneas de la familia Merma.png')
if selected == 'MQ-Corte tradicional':
    st.image('Gráfico de líneas de la familia MQ - Corte tradicional.png')
if selected == 'Panadería':
    st.image('Gráfico de líneas de la familia Panaderia.png')
if selected == 'PE - Patas enteras':
    st.image('Gráfico de líneas de la familia PE - Patas enteras.png')
if selected == 'Quesos':
    st.image('Gráfico de líneas de la familia Quesos.png')
if selected == 'Servicios':
    st.image('Gráfico de líneas de la familia Servicios.png')
if selected == 'Snacks':
    st.image('Gráfico de líneas de la familia Snacks.png')
if selected == 'Sobres al vacío':
    st.image('Gráfico de líneas de la familia Sobres al vacio.png')
if selected == 'Varios':
    st.image('Gráfico de líneas de la familia Varios.png')
if selected == 'Vinos':
    st.image('Gráfico de líneas de la familia Vinos.png')