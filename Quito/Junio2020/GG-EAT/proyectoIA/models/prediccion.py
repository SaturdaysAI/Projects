import numpy as np
import pandas as pd
import joblib
#print(GaussianNB.__version__)
modelo = joblib.load('/www/proyectoIA/models/modelo_Entrenado.pkl')
cl = joblib.load('/www/proyectoIA/models/clasificar.pkl')

#apertura del archivo para la evaluacion
url='/www/proyectoIA/dataset/evaluacion.csv'
df_evaluacion=pd.read_csv(url,sep=';')

prediccion = modelo.predict(df_evaluacion)

df_evaluacion['gustar']=prediccion
clasificar = df_evaluacion.drop(['id_restaurante'],axis=1)
clas = cl.predict(clasificar)

ids = df_evaluacion['id_restaurante']
df_prediccion = pd.DataFrame({'id_restaurante':ids,'gustar':prediccion})

nuevo = pd.DataFrame({'id_restaurante':[clas[0]],'gustar':[prediccion[0]]})
df_prediccion=pd.concat([nuevo,df_prediccion])

if (len(df_prediccion.id_restaurante)>5):
    df_prediccion = df_prediccion[:5]
df_prediccion.to_csv('/www/proyectoIA/results/resutaldo.csv', sep=';',index=False)

