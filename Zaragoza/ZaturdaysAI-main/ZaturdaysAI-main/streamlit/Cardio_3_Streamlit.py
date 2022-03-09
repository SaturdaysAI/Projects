import pandas as pd
import streamlit as st
import seaborn as sns
import joblib as jb
import os
# Limpieza y tratamiento de datos, incluyendo el modelo

# from Cardio_analisis
st.set_page_config(page_title='Card.IO - Predicción de Enfermedades Cardiovasculares',
                page_icon='❤')

cardio = pd.read_csv('local', delimiter=';')
cardio_nuevo = cardio[cardio.height>140]
cardio_nuevo = cardio_nuevo[cardio.height<200]
# cardio.shape[0]-cardio_nuevo.shape[0]

cardio_nuevo = cardio_nuevo[cardio_nuevo.weight>40]
cardio_nuevo = cardio_nuevo[cardio_nuevo.weight<200]
# cardio_nuevo = cardio.shape[0]-cardio_nuevo.shape[0]

cardio_nuevo = cardio_nuevo[cardio_nuevo.ap_hi>80]
cardio_nuevo = cardio_nuevo[cardio_nuevo.ap_hi<200]
# cardio_nuevo = cardio.shape[0]-cardio_nuevo.shape[0]

cardio_nuevo = cardio_nuevo[cardio_nuevo.ap_lo>40]
cardio_nuevo = cardio_nuevo[cardio_nuevo.ap_lo<160]
# cardio_nuevo = cardio.shape[0]-cardio_nuevo.shape[0]


st.write("""
# Card.IO 
## Predicción de Enfermedades Cardiovasculares con Inteligencia Artificial
""")

# Introduction Text
st.write('''
### ¿Qué es Card.IO?
Card.IO es un modelo de inteligencia artificial que toma datos como presión arterial, colesterol, hábitos de
consumo de tabaco y alcohol, entre otros, de forma anonima y de miles de pacientes de edades a partir de los 16 años. 
Estos datos son filtrados y procesados para alimentar el modelo, que arroja una prediccción de que tan probable 
es que el usario padezca una enfermedad cardiovascular o sea propenso a ella. 
''')

# Text that introduces the variable selection for boxplot plotting
st.write('''
## ¿Te has preguntado que afecta más a tu salud cardiovascular?
Selecciona el habito o variable que más te interese cononcer, la gráfica te dará un indicador de si puede o no ser 
relevante en el desarrollo o padecimiento de una enfermedad cardiovascular. La gráfica esta divida por el número de 
personas sin y con enfermedad cardiovascular, representada por el 0 o 1, respectivamente.
''')

st.set_option('deprecation.showPyplotGlobalUse', False)

headers = {'edad':'age',
           'género':'gender',
          'altura':'height',
          'peso':'weight',
          'presión sistólica':'ap_hi',
          'presión diastólica':'ap_lo',
          'colesterol':'cholesterol',
           'glucosa':'gluc',
          'tabaquismo':'smoke',
          'alcoholismo':'alco',
           'Actividad':'active'}
var_select = st.selectbox('Selecciona la variable', ("Edad", "Altura","Peso","Género",
                                                        "Presión Sistólica", "Presión Diastólica",
                                                        "Colesterol","Glucosa",
                                                        "Tabaquismo","Alcoholismo"),)
if var_select.lower() in headers.keys():
    # headers[var_select.lower()]
    sns.boxplot(data = cardio_nuevo, y = headers[var_select.lower()], x ="cardio").set_title(f'{var_select} con Relación a Enfermedad Cardíaca')
    # boxplots.set_xlabel('Género Hombres: 0, Mujeres: 1', fontsize=20)
    # boxplots.set_ylabel('Número de Pacientes (u.a.)', fontsize=20)
    st.pyplot()




st.write('''
# Veamos que nos cuentan tus datos...
## Cumplimenta el formulario y así el modelo podrá generar una predicción con tu perfil.
Esta predicción es solo una recomendación, no un diagnóstico, solo un médico especialista
puede diagnosticar con certeza el padecimiento de una enfermedad.
''')

def get_user_info():
    user_data = {}

    edad_user = st.text_input("Tu edad en años", '16')  # EDAD
    user_data['Edad']= edad_user

    genero_user = st.text_input("Sexo, M/F", 'M')  # La variable se convierte a 0 si es hombre 1 si es mujer
    if genero_user.lower() == 'm':
        genero_user = 0
    elif genero_user.lower() == 'f':
        genero_user = 1
    else:
        st.warning('Por favor introduce una respuesta válida')
    user_data["Genero"] = genero_user

    altura_user = st.text_input("Tu altura en cm", '167')
    user_data["Altura"] = altura_user

    peso_user = st.text_input("Peso en Kg", '65')
    user_data["Peso"] = peso_user

    ap_hi_user = st.text_input("Ingresa la ultima medición de tu presión diastólica", '120')
    user_data["Presión diastólica"] = ap_hi_user

    ap_lo_user = st.text_input("Ingresa la ultima medición de tu presión sistólica", '80')
    user_data["Presión sistólica"] = ap_lo_user


    colesterol_user = int(st.text_input("Ingresa la ultima medición de tu colesterol mg/dL", '140'))
    if colesterol_user < 150:
        colesterol_user = 1
        user_data["Colesterol"] = colesterol_user
    elif colesterol_user >= 150 and colesterol_user < 175:
        colesterol_user = 2
        user_data["Colesterol"] = colesterol_user
    elif colesterol_user >= 175:
        colesterol_user = 3
        user_data["Colesterol"] = colesterol_user
    else:
        st.warning('Por favor introduce una respuesta válida')

    glucosa_user = int(st.text_input("Ingresa la ultima medición de tu glucosa mg/dL",'120'))
    if glucosa_user < 140:
        glucosa_user = 1
        user_data["Glucosa"] = glucosa_user
    elif glucosa_user >= 140 and glucosa_user < 199:
        glucosa_user = 2
        user_data["Glucosa"] = glucosa_user
    elif glucosa_user >= 199:
        glucosa_user = 3
        user_data["Glucosa"] = glucosa_user
    else:
        st.warning('Por favor introduce una respuesta válida')

    tabaco_u = st.text_input("Consumo de tabaco S/N", 'N')
    if tabaco_u.lower() == 's':
        tabaco_u = 1
    elif tabaco_u.lower() == 'n':
        tabaco_u = 0
    else:
        st.warning('Por favor introduce una respuesta válida')
    user_data["Consumo de tabaco"] = tabaco_u

    alcohol_u = st.text_input("Consumo de alcohol, S/N", 'S')
    if alcohol_u.lower() == 'n':
        alcohol_u = 0
    elif alcohol_u.lower() == 's':
        alcohol_u = 1
    else:
        st.warning('Por favor introduce una respuesta válida')
    user_data["Consumo de alcohol"] = alcohol_u

    actividad_user = int(st.text_input("Actividad física: Activo - 1, No Activo - 0", '1'))
    user_data["Actividad física"] = actividad_user

    return user_data

user_data = get_user_info()
st.write('''### Estos son tus datos, que serán ingresados al modelo''', user_data)

# Here we turn the dictionary to a DF using pandas
pd.DataFrame(user_data,index=[0]).to_csv('local/df_user_info.csv', index=False)


df_user_info = pd.read_csv('local/df_user_info.csv')  # delimiter=';')
st.write(df_user_info)

st.write('''
# Predicción basada en IA ❤️🤖❤️
El uso de inteligencia artificial nos permite generar predicciones, basadas en estadísticas, acerca de algún fenomeno
observable y medible. Card.IO se basará en más de 70,000 voluntarios con o sin enfermedades cardiovasculares, para 
mostrar un indicador sobre si es pertinente que el usuario visite al médico especialista.

Recuerda, Card.IO, es solo una herramienta que puede guiarte para cuidar de tu salud cardiovascular, no es una
herramiento de diagnóstico. Si el resultado es positivo, es recomendable que acudas a tu médico para una revisión. 
''')

filename_model = os.path.join('/Users/erick/Desktop/Courses/Saturdays.AI', 'model.joblib')

col1, col2, col3 , col4, col5 = st.columns(5)
with col1:
    pass
with col2:
    pass
with col4:
    pass
with col5:
    pass
with col3 :
    predecir = st.button('Predecir', )

if predecir:
    final_model = jb.load(filename_model)
    estimated = round(float(final_model.predict(df_user_info)[0]), 3)
    if estimated > 0.5:
        st.write(f'''
        ## Estimado: {estimated*100} % Recomendable visitar al médico especialista
        ## Puedes mejorar tu salud cardiovascular
        ## 💔-🤖-🏋️-🥬🥕🥦-🚭-❤️
        
        ''')
    else:
        st.write('''
                ## ❤️ Tu salud cardiovascular es buena.
                # ¡Sigue así! ️❤️
                ''')


