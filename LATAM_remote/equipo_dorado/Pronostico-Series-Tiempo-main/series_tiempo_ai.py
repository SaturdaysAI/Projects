# -*- coding: utf-8 -*-


#!pip install yfinance
import yfinance
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from fbprophet import Prophet
import pandas as pd
#from pmdarima.arima import auto_arima
from statsmodels.tsa.holtwinters import ExponentialSmoothing


import numpy as np
import pmdarima as pm
from pmdarima import pipeline
from pmdarima import model_selection
from pmdarima import preprocessing as ppc
from pmdarima import arima
from matplotlib import pyplot as plt

"""Para obtener los precios de cierre de los índices SP500, FTSE, DAX y NIKKEI, especificar los nombres, la fecha de inicio y fin, y el intervalo (diario=1d):"""

raw_data = yfinance.download (tickers = "^GSPC ^FTSE ^N225 ^GDAXI", start = "2020-10-01", 
                              end = "2020-11-13", interval = "1d", group_by = 'ticker', auto_adjust = True, treads = True)

raw_data.tail()

df_comp=raw_data.copy()

"""Para cada día y cada precio obtenemos 4 datos, los precios de: apertura, máximo, bajo, cierre y volumen. Queremos los precios de cierre así que seleccionamos sólo la variable cierre para cada precio, los guardamos en 4 nuevas variables en el dataset y les ponemos los nombres del indice al que corresponden."""

df_comp['spx'] = df_comp['^GSPC'].Close[:]
df_comp['dax'] = df_comp['^GDAXI'].Close[:]
df_comp['ftse'] = df_comp['^FTSE'].Close[:]
df_comp['nikkei'] = df_comp['^N225'].Close[:]

df_comp.head()

"""Pre-procesado: eliminar las variables que sobran, arreglar la frecuencia a business days y rellenar datos faltantes."""

df_comp = df_comp.iloc[1:]
del df_comp['^N225']
del df_comp['^GSPC']
del df_comp['^GDAXI']
del df_comp['^FTSE']
df_comp=df_comp.asfreq('b')
df_comp=df_comp.fillna(method='ffill')
df_comp.reset_index(inplace=True)

df_comp.columns = ['Date', 'spx', 'dax', 'ftse', 'nikkei']
#df_comp.set_index('Date', inplace=True)

df=pd.melt(df_comp, id_vars=['Date'])
df.columns = ['ds', 'variable', 'y']
df


#definir funcion MAPE
def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) 



#df.reset_index(inplace=True)
#del df['index']
#df.set_index('Date', inplace=True)
############################################################
#### MODELO FACEBOOK PROPEHT



#vector a iterar por ejemplo: Analgan, Truxa, Etec

vector= df.loc[:,'variable']
vector = vector.drop_duplicates()
vector= vector.values.tolist()
print("Hay",len(vector),"series de tiempo")

#vector con los resultados por cada método
vector_rmse_train= []
vector_rmse_test=[]
algoritmo=[]
vector_serie=[]


vector_a_min=[]
vector_b_min=[]
vector_c_min=[]
vector_serie_min=[]

#iterar las n series de tiempo
for s in range(len(vector)): 
  

    
  #dividir en conjunto de entrenamiento y conjunto de prueba
  df_serie= df[df['variable'] == vector[s]]
  
  #eliminar variable solo me quedo con ds(fecha) y y(venta)
  del df_serie['variable']
  
  #dividir con conjunto de entrenamiento y conjunto de prueba
  tamanio_entrenamiento=int(round(len(df_serie)*0.7, ndigits=0))
  train=df_serie.iloc[0:tamanio_entrenamiento,:]
  test=df_serie.iloc[tamanio_entrenamiento:,:]
  
  #preprocesado arima
  train_arima= train.set_index('ds')
  test_arima=test.set_index('ds')
  train_arima=train_arima.asfreq('b')
  test_arima=test_arima.asfreq('b')
###################################################
############# inicia facebook prophet    
    

    
  #vector de errores
  errores_proceso_fb=[]
  try:
      #modelar facebook prophet
      m = Prophet(growth='linear',
                  seasonality_mode='additive', 
                  weekly_seasonality=True, 
                  daily_seasonality=False, 
                  yearly_seasonality=False)#,interval_width=0.90)
      m.fit(train)
      future = m.make_future_dataframe(periods=len(test)+10, #+10 por los fines de semana
                                       freq = 'D',
                                       include_history=True)
      forecast = m.predict(future)
         
      #dejar solamente las dos columnas
      forecast= forecast.loc[:,['ds','yhat']]
      
      #fijar el indice antes de unir archivos
      forecast.set_index('ds', inplace=True)
      df_serie.set_index('ds', inplace=True)
      
      #unir con el conjunto original
      forecast=pd.merge(df_serie, forecast, left_index=True, right_index=True)
      
      #medir el error
      rmse_train = mean_squared_error(forecast['y'].iloc[0:tamanio_entrenamiento], 
                                      forecast['yhat'].iloc[0:tamanio_entrenamiento], 
                                      squared=False)
      rmse_test = mean_squared_error(forecast['y'].iloc[tamanio_entrenamiento:], 
                                     forecast['yhat'].iloc[tamanio_entrenamiento:], 
                                     squared=False)
      
      #añadir los errores al dataframe
      vector_rmse_train.append(rmse_train)
      vector_rmse_test.append(rmse_test)
      algoritmo.append('Facebook')
      vector_serie.append(vector[s])
      
  except:
      errores_proceso_fb.append(vector[s])
  
  #Imprimir errores en el proceso
  if len(errores_proceso_fb)>0:
      print('Se presentaron errores en las siguientes variables ', errores_proceso_fb)
  else:
      print('No se encontraron errores en el proceso ;)', vector[s])




##########################################################33
########## MODELO Holt Winters REDUCIR A INCREMENTOS DE 0.1

      
  ###### empecemos la iteracción  ######
  vector_a=[]
  vector_b=[]
  vector_c=[]
  errores_proceso_hw=[]


  
  
  try:
      for a in range(0, 110,10): #start=0, stop=100, step=5
          for b in range(0, 110,10):
              for c in range(0, 110,10):
                  vector_a.append(a)
                  vector_b.append(b)
                  vector_c.append(c)
      #crear el dataframe y filtrar los valores
      vector_combinaciones = pd.DataFrame({
                   'vector.a' : vector_a,
                   'vector.b' : vector_b,
                   'vector.c' : vector_c})
      #eliminar combinacion (0,0,0)
      vector_combinaciones.drop(axis=0, index=0, inplace=True)
      vector_combinaciones=vector_combinaciones/100
      ###### terminar iteraccion  ######
      
      
      
      ###### iterar el dataframe #####
      vector_error_train=[]
      vector_error_test=[]

      
      for m in range(len(vector_combinaciones)):
          modelo_winters = ExponentialSmoothing(train_arima,
                                                trend='add',
                                                seasonal='add',
                                                seasonal_periods=5,
                                                freq='B')
          #ajustar el modelo use_boxcox=True
          results_winters = modelo_winters.fit(smoothing_level=vector_combinaciones.iloc[m].loc['vector.a'],
                                           smoothing_slope=vector_combinaciones.iloc[m].loc['vector.b'],
                                           smoothing_seasonal=vector_combinaciones.iloc[m].loc['vector.c'])
          #estimar el periodo de prueba
          forecast_winters= results_winters.forecast(len(test_arima))
      
          #calcular el error
          rmse_test_winters = mean_squared_error(forecast_winters,
                                                 test_arima,
                                                 squared=False)
          rmse_train_winters = mean_squared_error(results_winters.fittedvalues,
                                                 train_arima,
                                                 squared=False)

          vector_error_test.append(rmse_test_winters)
          vector_error_train.append(rmse_train_winters)
        
      vector_combinaciones['rmse_test']=vector_error_test
      vector_combinaciones['rmse_train']=vector_error_train
      vector_combinaciones['dif']=abs(vector_combinaciones['rmse_test']-vector_combinaciones['rmse_train'])
      vector_combinaciones=vector_combinaciones[vector_combinaciones['dif']==min(vector_combinaciones['dif'])]
      del vector_combinaciones['dif']
      vector_a_min.append(vector_combinaciones.iloc[0,0])
      vector_b_min.append(vector_combinaciones.iloc[0,1])
      vector_c_min.append(vector_combinaciones.iloc[0,2])
      vector_serie_min.append(vector[s])
      
#      GRAFICO RMSE TEST VS RMSE TRAIN
#      plt.plot(vector_combinaciones['rmse_test'],vector_combinaciones['rmse_train'], 'ro' ,markersize=2)
#      plt.xlabel('Rmse_test')
#      plt.ylabel('Rmse_train')
#      plt.title('RMSE train vs test Holt Winters')
#      plt.show()
      


  except:
      errores_proceso_hw.append(vector[s])   

  vector_rmse_train.append(vector_combinaciones.iloc[0,4])
  vector_rmse_test.append(vector_combinaciones.iloc[0,3])
  algoritmo.append('Holt_winters')
  vector_serie.append(vector[s])       
      
##########################################################33
########## MODELO AUTOARIMA

  errores_proceso_ar=[]
  try:
      # Let's create a pipeline with multiple stages... the Wineind dataset is
      # seasonal, so we'll include a FourierFeaturizer so we can fit it without
      # seasonality
      pipe = pipeline.Pipeline([
              ("fourier", ppc.FourierFeaturizer(m=5)), #modela la estacionalidad con periodicidad 5
              ("arima", arima.AutoARIMA(stepwise=True, trace=1, error_action="ignore",
                              seasonal=False,  # because we use Fourier
                              suppress_warnings=True))
              ])

      pipe.fit(train_arima)
      print("Model fit:")
      print(pipe)

      # We can compute predictions the same way we would on a normal ARIMA object:
      forecast_arima = pipe.predict(n_periods=int(len(test)))
      

      rmse_test_arima = mean_squared_error(test_arima, 
                                     forecast_arima, 
                                     squared=False)      

  except:
      errores_proceso_ar.append(vector[s])        
      
      #añadir los errores al dataframe
  vector_rmse_train.append(np.nan)
  vector_rmse_test.append(rmse_test_arima)
  algoritmo.append('Autoarima')
  vector_serie.append(vector[s])
#!pip install pmdarima


#CREAR DATAFRAME
matriz_parametros_hw = pd.DataFrame({
                   'vector_a_min' : vector_a_min,
                   'vector_b_min' : vector_b_min,
                   'vector_c_min' : vector_c_min,
                   'vector_serie' : vector_serie_min
                   })

matriz_rmse_producto = pd.DataFrame({
                   'algoritmo' : algoritmo,
                   'train_rmse' : vector_rmse_train,
                   'test_rmse' : vector_rmse_test,
                   'vector_serie' : vector_serie
                   })

#Podemos seleccionar el mejor modelo de acuerdo a las necesidades del problema, por ejemplo: menor RMSE sin sobreajuste
print(matriz_rmse_producto)
#En este caso el modelo que cumple mejor con los criterios antes expuesto es: Holt Winters, con el cual se realizará el pronóctico. 

    


######### PRONOSTICO



    
#crear un dataframe vacío con las siguientes columnas

vector_serie=[]
rmse=[]
mape=[]
algoritmo=[]

#df_pronostico
df_pronostico = pd.DataFrame({
                   'ds' : [],
                   'y' : [],
                   'variable' : [],
                   'tipo' : []
                   })


for s in range(len(vector)):
  df_serie= df[df['variable'] == vector[s]]
  
  #eliminar variable solo me quedo con ds(fecha) y y(venta)
  del df_serie['variable']
  
  #preprocesado arima

  df_serie=df_serie.set_index('ds')
  df_serie=df_serie.asfreq('b')
  
  modelo_winters = ExponentialSmoothing(df_serie,
                                        trend='add',
                                        seasonal='add',
                                        seasonal_periods=5,
                                        freq='B')
#ajustar el modelo use_boxcox=True
  results_winters = modelo_winters.fit(smoothing_level=matriz_parametros_hw[matriz_parametros_hw['vector_serie']==vector[s]].iloc[0,0],
                                       smoothing_slope=matriz_parametros_hw[matriz_parametros_hw['vector_serie']==vector[s]].iloc[0,1],
                                       smoothing_seasonal=matriz_parametros_hw[matriz_parametros_hw['vector_serie']==vector[s]].iloc[0,2])
#estimar el periodo de prueba
  forecast_winters= results_winters.forecast(5)
  forecast_winters=forecast_winters.reset_index()
  forecast_winters = forecast_winters.rename(columns={'index':'ds', 0:'y'})
  forecast_winters['variable']=vector[s]
  forecast_winters['tipo']='Proyectado'
  df_pronostico=pd.concat([df_pronostico, forecast_winters])    
#calcular el error
  rmse_serie_winters = round(mean_squared_error(results_winters.fittedvalues,
                                                 df_serie,
                                                 squared=False),2)
  mape_serie_winters = round(mean_absolute_percentage_error(results_winters.fittedvalues, df_serie),4)
  
  vector_serie.append(vector[s])
  rmse.append(rmse_serie_winters)
  mape.append(mape_serie_winters)
  algoritmo.append('Holt_Winters')
  
Resumen = pd.DataFrame({
                   'vector_serie' : vector_serie,
                   'algoritmo' : algoritmo,
                   'rmse' : rmse,
                   'mape' : mape
                   })
    
    
#crear dataframe final
df['tipo']='Real'
df=pd.concat([df_pronostico, df])       
df = df.rename(columns={'ds':'fecha',
                        'y':'precio',
                        'variable':'producto',
                        'tipo':'Tipo'})
Resumen = Resumen.rename(columns={'vector_serie':'producto'})

df.to_csv('/home/jjacho/Escritorio/Series Tiempo Saturdays/Pronostico.csv', index=False)
Resumen.to_csv('/home/jjacho/Escritorio/Series Tiempo Saturdays/Resumen Modelos.csv', index=False)
matriz_rmse_producto.to_csv('/home/jjacho/Escritorio/Series Tiempo Saturdays/matriz_rmse.csv', index=False)      
