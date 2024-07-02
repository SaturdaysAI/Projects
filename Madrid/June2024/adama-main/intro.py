import streamlit as st
import os

# Page title
st.set_page_config(page_title='ADAMA', page_icon='☁️')
st.title('🚗🚗☁️☁️ ADAMA ☁️☁️🏃🏃‍♂️')



# with st.expander('About this app'):
#   st.markdown('**What can this app do?**')
#   st.info('This app allow users to build a machine learning (ML) model in an end-to-end workflow. Particularly, this encompasses data upload, data pre-processing, ML model building and post-model analysis.')

#   st.markdown('**How to use the app?**')
#   st.warning('To engage with the app, go to the sidebar and 1. Select a data set and 2. Adjust the model parameters by adjusting the various slider widgets. As a result, this would initiate the ML model building process, display the model results as well as allowing users to download the generated models and accompanying data.')

#   st.markdown('**Under the hood**')
#   st.markdown('Data sets:')
#   st.code('''- Drug solubility data set
#   ''', language='markdown')
  
#   st.markdown('Libraries used:')
#   st.code('''- Pandas for data wrangling
# - Scikit-learn for building a machine learning model
# - Altair for chart creation
# - Streamlit for user interface
#   ''', language='markdown')



st.header("¿Sabríais decirme cuando se registró el primer dato de tráfico de la historia?")

st.caption("Desde ADAMA Project hemos trabajando para aportar un punto de vista distinto sobre el deporte y la polución generada por el tráfico. La primera vez que se hizo referencia y se registró un dato de tráfico fue en 1240. El accidente involucró a un caballero alemán llamado Berthold Schwartz, que se golpeó con un carro mientras cabalgaba cerca de la localidad de Liegnitz.")
st.caption("Actualmente gozamos de un gran repositorio de datos y de gran cantidad de estaciones que recogen información sobre datos ambientales, polución e intensidad de tráfico.")

st.caption("Nuestro proyecto ADAMA está orientado a cómo afecta en tiempo real a la salud de los viandantes, deportistas y personas en general. En este caso recogemos los datos provenientes de la Comunidad de Madrid.")

st.subheader("Recogemos los siguientes datos:")

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
rel_path = "data/bodytext.txt"
with open(os.path.join(script_dir, rel_path), 'r', encoding='utf-8') as file:
    for line in file:
        st.caption(line)

st.subheader("Referencias")
st.page_link("https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=2ac5be53b4d2b610VgnVCM2000001f4a900aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default", label = "(1) Datos meteorológicos")
st.page_link("https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=41e01e007c9db410VgnVCM2000000c205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD", label = "(2) Datos de polución")
st.page_link("https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=02f2c23866b93410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD", label = "(3) Datos de tráfico")
st.page_link("https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=9f710c96da3f9510VgnVCM2000001f4a900aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default", label = "(4) Festivos comunidad de Madrid")

