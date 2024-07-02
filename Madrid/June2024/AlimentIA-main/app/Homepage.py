import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title='Home', 
    page_icon="🎓",
    layout='wide',
    initial_sidebar_state='expanded'
    )


st.title('AlimentIA: Análisis de negocio y predicción de ventas')

# Barra lateral con Logo, selección de modelo y nubes de palabras
with st.sidebar:
    st.sidebar.success("Selecciona una demostración de la lista de arriba")
    st.write("---")
    st.image('logo.png', width=200)
    st.write("---")
    st.write('Andrés Peñafiel Rodas \n andres.pennafiel@gmail.com')
    st.write('David Monroy \n monroygonzalezdavid@gmail.com')
    st.write('Pablo Tomás \n 93pablotr@gmail.com')
    st.write('Mayra \n andres.pennafiel@gmail.com')
    st.write('Sergio Serna \n sgsernac@gmail.com')
    

st.write("## AI Saturdays Madrid - Proyecto de ML")

# añade una línea de separación
st.write('---')

st.markdown(
    """
    Este proyecto es una demostración de la aplicación de técnicas de predicción de ventas en un entorno de negocio real.
        
    **👈 Selecciona una demostración de la barra lateral** para ver gráficos, modelos y sus 
    métricas, calcular predicciones e interactuar con la interfaz.

    ### ¿Qué fuentes de datos hemos usado?
    Hemos partido de un conjunto de datos reales que recogen el registro de venta de diversos productos de una tienda de alimentación.
    Nuestro dataset consiste, previo análisis exploratorio de los datos, en 37 atributos con más de 70.000 registros reales.
    Entre los datos, se pueden encontrar registros temporales de la venta de distintos productos y la cantidad vendida de cada uno de ellos.

    ### ¿Qué artículos hemos consultado?
    Con el fin de emplear las técnicas más adecuadas, consultamos artículos relacionados con la predicción basada en series temporales como:
    Time Series Forecasting: A Practical Guide to Exploratory Data Analysis | by Maicol Nicolini | May, 2024 | Towards Data Science (medium.com)

    ### ¿Qué modelos de aprendizaje automático hemos usado?
    Aprovechando la dimensión temporal con la que cuentan nuestros datos iniciales, decidimos utilizar un modelo de forecasting para la predicción de series temporales.
    Estudiamos modelos como PROPHET, que resulta muy efectivo a la hora de tratar series temporales con una fuerte dependencia estacional, 
    y ARIMA como modelo dinámico cuyas estimaciones futuras vienen explicadas por los datos del pasado.

    """
)

