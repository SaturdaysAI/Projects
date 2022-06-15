#!/usr/bin/env python

import pandas as pd
import numpy as np
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt
import folium as fl

def basic_bargraph(medidas): 
	"""

	Toma medidas 2020 (después de agregar metadatos)
	"""
	return medidas


def mapas_medidas():
	"""
	mapas_medidas() genera un mapa de medidas de Barcelona por cada año disponible de 3 contaminantes.
	"""
	gdf1 = gpd.read_file("../datasets/maps/2018/2018_tramer_pm2-5_mapa_qualitat_aire_bcn.gpkg")
	gdf2 = gpd.read_file("../datasets/maps/2018/2018_tramer_pm10_mapa_qualitat_aire_bcn.gpkg")
	gdf3 = gpd.read_file("../datasets/maps/2018/2018_tramer_no2_mapa_qualitat_aire_bcn.gpkg")

	gdf4 = gpd.read_file("../datasets/maps/2019/2019_tramer_pm2-5_mapa_qualitat_aire_bcn.gpkg")
	gdf5 = gpd.read_file("../datasets/maps/2019/2019_tramer_pm10_mapa_qualitat_aire_bcn.gpkg")
	gdf6 = gpd.read_file("../datasets/maps/2019/2019_tramer_no2_mapa_qualitat_aire_bcn.gpkg")

	f, axes = plt.subplots(figsize=(30, 30), ncols=3, nrows=2)

	axes[0][0].set_title('2018 - PM2,5')
	axes[0][1].set_title('2018 - PM10')
	axes[0][2].set_title('2018 - NO2')

	axes[1][0].set_title('2019 - PM2,5')
	axes[1][1].set_title('2019 - PM10')
	axes[1][2].set_title('2019 - NO2')

	gdf1.plot(ax=axes[0][0], column='Rang', legend=True)
	gdf2.plot(ax=axes[0][1], column='Rang', legend=True)
	gdf3.plot(ax=axes[0][2], column='Rang', legend=True)
	gdf4.plot(ax=axes[1][0], column='Rang', legend=True)
	gdf5.plot(ax=axes[1][1], column='Rang', legend=True)
	gdf6.plot(ax=axes[1][2], column='Rang', legend=True)
	f.savefig("../viz/mapas_medidas.pdf", bbox_inches='tight')

# Path de notebook
def mapa_estaciones():
	"""
	Bibliografía:
	https://python-visualization.github.io/folium/quickstart.html#Getting-Started
	https://e-archivo.uc3m.es/bitstream/handle/10016/31974/TFG_Isabel-Maria_San-Jose_Garcia.pdf?sequence=1
	https://python-visualization.github.io/folium/modules.html
	https://www.kaggle.com/code/cheyenneamoroso/drawing-geojson-barcelona/notebook
	"""
	s = fl.Map(location=[41.390205, 2.154007],
	           zoom_start=13)
	data = pd.read_csv('/content/2021_qualitat_aire_estacions.csv')
	uno = data.loc[0]
	uno
	data.iloc[9]
	data.Estacio.value_counts()
	for i in range(50):
	  # Guardamos el nombre de la estación
	  num = data.Estacio[i]
	  tooltip = 'Número de estación: '+ str(num)
	  popup = 'Estación: '+ str(num)
	  # Asignamos al mapa los atributos de la estación y su ubicación
	  fl.Marker([data.Latitud[i], data.Longitud[i]], popup = popup, tooltip = tooltip).add_to(s)

	# Visualización del mapa con las estaciones
	s