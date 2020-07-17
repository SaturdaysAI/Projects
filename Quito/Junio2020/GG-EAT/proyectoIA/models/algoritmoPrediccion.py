import numpy as np
import pandas as pd
from sklearn import metrics

#BAYES
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

#apertura del archivo para el entrenamiento
url='/www/proyectoIA/dataset/train.csv'
data=pd.read_csv(url,sep=';')

#apertura del archivo para el testeo
url='/www/proyectoIA/dataset/evaluacion.csv'
df_test=pd.read_csv(url,sep=';')

#print(df_test)
while True:
  msk = np.random.rand(len(data)) < 0.75
  data_train = data[msk]
  data_test = data[~msk]
  
  if len(data_train[data_train['gustar']==1])==18 and len(data_train[data_train['gustar']==0])==11 :
    break
# separacion de datos para el modelo
X_train = data_train.drop(['gustar','id_restaurante'],axis=1)
Y_train = data_train['gustar']

X_test = data_test.drop(['gustar','id_restaurante'],axis=1)
Y_test = data_test['gustar']

NB = GaussianNB()
NB_ajustado = NB.fit(X_train, Y_train)
y_pred = NB_ajustado.predict(X_test)


#prediccion con nuevo dato
ids = df_test['id_restaurante']

prediccion = df_test.drop(['id_restaurante'],axis=1)

prediccion = NB_ajustado.predict(prediccion)

df_prediccion = pd.DataFrame({'id_restaurante':ids,'gustar':prediccion})

if (len(df_prediccion.id_restaurante)>5):
    df_prediccion = df_prediccion[:5]

#print(df_prediccion)
df_prediccion.to_csv('/www/proyectoIA/results/resutaldo.csv', sep=';',index=False)