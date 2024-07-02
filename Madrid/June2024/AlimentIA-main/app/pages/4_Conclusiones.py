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
    ### Objetivos del proyecto
    - Desarrollar modelos de predicción de series temporales basados en inteligencia artificial
    - Mejorar la precisión de las predicciones de demanda de productos
    - Reducir significativamente la merma de productos y optimizar el inventario

    ### Limitaciones del proyecto
    - Implementar un sistema de predicción de demanda preciso y eficiente, con unos datos reales pero sin continuidad a lo largo del tiempo, que permita a la empresa anticipar las necesidades de sus clientes y reducir la merma de productos.
    
    ### Conclusiones
    - La adopción de tecnologías de inteligencia artificial ha permitido a la empresa diferenciarse en el mercado y ofrecer soluciones más innovadoras.
    - La reducción de la merma y la optimización del inventario han generado ahorros significativos, mejorando la rentabilidad general del negocio.
    - Los modelos de predicción basados en IA han proporcionado información más precisa y oportuna para la toma de decisiones estratégicas.
    - La mejora en la disponibilidad de productos ha fortalecido la lealtad y la satisfacción de los clientes.
    """
)

