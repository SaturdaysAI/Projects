
import streamlit as st
import joblib
import numpy as np 
import pandas as pd
import plotly.graph_objects as go
import webbrowser
import time
from PIL import Image
import sklearn





def Settings():
    
    #st.markdown("<h1 style='text-align: center; color: black;'>CARDIOSIGHT</h1>", unsafe_allow_html=True)
    #st.write("<h1 style='text-align: center; color: black;'>Calculadora de Riesgo Cardiovascular</h1>", unsafe_allow_html=True)
    image = Image.open('logoblanco.png')
    st.image(image, use_column_width=True)
    Genero= st.sidebar.selectbox('Genero',options=['Femenino', 'Masculino'])
    Edad= st.sidebar.number_input("Edad: ")
    A_Fisica = st.sidebar.selectbox('¿Realiza actividad fìsica de forma frecuente?',options=['Sí', 'No'])
    Fumar = st.sidebar.selectbox('¿Fuma de forma frecuente?',options=['Sí', 'No'])
    Alcohol = st.sidebar.selectbox('¿Consume alcohol de forma frecuente?',options=['Sí', 'No'])
    Peso= st.sidebar.number_input("Peso en kg: ")
    Altura= st.sidebar.number_input("Altura en cm: ")
    P_hi= st.sidebar.number_input("Presión arterial sistólica mmHg: ")
    P_lo= st.sidebar.number_input("Presión arterial Distólica mmHg: ")
    Col = st.sidebar.selectbox('Nivel de colesterol',options=['Normal', 'Arriba de lo normal','Muy arriba de lo normal'])
    Gluc = st.sidebar.selectbox('Nivel de Glucosa',options=['Normal', 'Arriba de lo normal','Muy arriba de lo normal'])
  
    button = st.button("Presiona para realizar tu cálculo")

    return Genero, Edad, A_Fisica, Fumar, Alcohol, Peso, Altura, P_hi, P_lo, Col, Gluc,button

def Convertdata(GE_2):

    #Convert Genero variable from femenino and masculino to 0 and 1.
    if Genero=='Femenino':
        GE_2=1
    elif Genero=='Masculino':
        GE_2=2

    else:
        GE_2=0

    return GE_2

def Convertdata2(ED_2):

    #Convert Edad variable from years to days.
    ED_2=ED_2*365

    return ED_2

def Convertdata3(AFI_2):
    if AFI_2=='Sí':
        AFI_2=1
    elif AFI_2=='No':
        AFI_2=0
    else:
        AFI_2=3

    return AFI_2

def Convertdata4(ALC_2):
    if ALC_2=='Sí':
        ALC_2=1
    elif ALC_2=='No':
        ALC_2=0
    else:
        ALC_2=3

    return ALC_2

def Convertdata5(FUM):
    if FUM=='Sí':
        FUM_2=1
    elif FUM=='No':
        FUM_2=0

    return FUM_2

def Convertdata6(GLU):
    if GLU=='Normal':
        GLUC_3=1
    elif GLU=='Arriba de lo normal':
        GLUC_3=2
    else:
        GLUC_3=3
    return GLUC_3
    
    
def Convertdata7(CO):
    if CO=='Normal':
        CO_=1
    elif CO=='Arriba de lo normal':
        CO_=2

    else:
        CO_=3

    return CO_

def Convertdata8(AL,PES):

    BMI_=PES//((AL/100)**2)



    return BMI_
            
 
      
     




    

def loadmodel():
    RFM = joblib.load('RFC_M.pkl')
    return RFM
    

  
def pressbutton(GE, ED,A_F,ALC,FUM,GLU,CO,P_HI,P_LO,ALT,PES):

    if(button):
        url = 'http://www.imss.gob.mx/cita-medica'
        GENERO_DF=Convertdata(GE)
        EDAD_AOS_DF=Convertdata2(ED)
        AF_DF=Convertdata3(A_F)
        ALC_DF=Convertdata4(ALC)
        FUM_DF=Convertdata5(FUM)
        GLUC_DF=Convertdata6(GLU)
        COL_DF=Convertdata7(CO)
        BMI_DF=Convertdata8(ALT,PES)
        #LISTA=[GENERO_DF,EDAD_AOS_DF,AF_DF,ALC_DF,FUM_DF,GLUC_DF,COL_DF]
        LIST=[EDAD_AOS_DF,GENERO_DF,P_HI,P_LO,COL_DF,GLUC_DF,FUM_DF,ALC_DF,AF_DF,ALT,PES,BMI_DF]
        #st.write(LIST)

        RandomForestModel=loadmodel()
        df = pd.DataFrame(LIST)
        Columns=['age', 'gender', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'newvalues_height', 'newvalues_weight','New_values_BMI']
        #ass=pd.DataFrame(LIST, columns=Columns)
        
        a= RandomForestModel.predict_proba([LIST])[:,1]
          
    
        #st.write(a[0])

        if a[0]>0.475193:
            score='NIVEL DE RIESGO ALTO'
            score2= "Alto"
            st.success("Tu nivel de riesgo cardiovascular es: {}.                            \n Es importante que acudas con un profesional médico para que se pueda diseñar un programa de prevencion especialmente para ti.                            \n Serás redireccionado a la página principal del IMSS para que agendes tu cita ".format(score2))
            #Bu2 = st.button("Presiona para tener más informacion sobre los programas de salud activos")
            #if Bu2==1:
            #time.sleep(10)
            #webbrowser.open_new_tab(url)
            
                
    

        else:
            score='NIVEL DE RIESGO BAJO'
            score2= "Bajo"
            st.success("Tu nivel de riesgo cardiovascular es: {}".format(score2))

          

        fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = a[0],
        
        mode = "gauge+number",
        title = {"text": score2},
        delta = {'reference': .380},
        gauge = {'axis': {'range': [None, 1]},
             'steps' : [
                 {'range': [0, 1], 'color': "rgb(75, 204, 51, 80)"},
                 {'range': [.475194, 1], 'color':"rgb(240, 49, 42, 80)"}],
             'threshold' : {'line': {'color': "black", 'width': 5}, 'thickness': 0.8, 'value': 1}}))

        st.plotly_chart(fig)

        if score=='NIVEL DE RIESGO ALTO':
            time.sleep(10)
            webbrowser.open_new_tab(url)

        

   
       


    


Genero, Edad, A_Fisica, Fumar, Alcohol, Peso, Altura, P_hi, P_lo, Col,Gluc,button=Settings()

pressbutton(Genero, Edad,A_Fisica,Alcohol,Fumar,Gluc,Col,P_hi,P_lo,Altura,Peso)













