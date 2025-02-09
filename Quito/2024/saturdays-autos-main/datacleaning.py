import pandas as pd
import numpy as np

# Cargar el conjunto de datos
url = 'https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv'
data = pd.read_csv(url)

# Mostrar las primeras filas del conjunto de datos
print(data.head())

# Limpieza de datos
# Eliminar filas con valores nulos en las columnas importantes
data = data.dropna(subset=['fare_amount', 'trip_distance', 'PULocationID', 'DOLocationID'])

# Eliminar valores atípicos en la tarifa y la distancia
data = data[(data['fare_amount'] > 0) & (data['fare_amount'] < 100)]
data = data[(data['trip_distance'] > 0) & (data['trip_distance'] < 100)]

# Convertir las fechas a datetime
data['tpep_pickup_datetime'] = pd.to_datetime(data['tpep_pickup_datetime'])
data['tpep_dropoff_datetime'] = pd.to_datetime(data['tpep_dropoff_datetime'])

# Calcular la duración del viaje en minutos
data['trip_duration'] = (data['tpep_dropoff_datetime'] - data['tpep_pickup_datetime']).dt.total_seconds() / 60

# Eliminar filas con duración de viaje negativa o cero
data = data[data['trip_duration'] > 0]

# Mostrar el resumen del conjunto de datos limpio
print(data.describe())
