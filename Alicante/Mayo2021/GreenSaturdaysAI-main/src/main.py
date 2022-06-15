#!/usr/bin/env python
import sys
import os
from utils import *
from visual import *


# Añade metadatos, limpia dataframe
medidas = integratemetadata()
medidas.drop(['CODI_PROVINCIA','PROVINCIA', 'CODI_MUNICIPI', 'MUNICIPI'], axis='columns', inplace=True)
medidas_clean = medidas[['ESTACIO','CODI_CONTAMINANT','CONTAMINANTE']]
(medidas_clean['CODI_CONTAMINANT'] == medidas_clean['CONTAMINANTE']).value_counts()
medidas_clean['CODI_CONTAMINANT'].isnull().value_counts()
medidas_clean['CONTAMINANTE'].isnull().value_counts()
medidas_wo_null = medidas_clean.dropna()
medidas_wo_null['CODI_CONTAMINANT'].isnull().value_counts()
medidas_bef_join = medidas_wo_null[['ESTACIO','CONTAMINANTE']]
(medidas_wo_null['CODI_CONTAMINANT'] == medidas_wo_null['CONTAMINANTE']).value_counts()
dat = pd.read_csv('qualitat_aire_contaminants.csv')
medidas_filter = medidas_bef_join.drop_duplicates()
medidas_fil_re = medidas_filter.rename(columns={'CONTAMINANTE':'Codi_Contaminant'})
res = dat.to_dict()

"""
dat = dat[0:9]
test_filter = test_filter.drop(index=2583)
test_filter = test_filter.rename(columns={'CONTAMINANTE':'Codi_Contaminant'})
test_filter['ESTACIO'] = test_filter['ESTACIO'].astype(int)
test_filter['Codi_Contaminant'] = test_filter['Codi_Contaminant'].astype(int)

# Realizamos la unión de los datos
res = test_filter.merge(dat, how='right')
res_final = res.sort_values('ESTACIO')
…  print(listado[i][0] +' ['+ listado[i][1]+']\n')

for i in range(50):
  # Guardamos el nombre de la estación
  num = data.Estacio[i]
  tooltip = 'Número de estación: '+ str(num)
  popup = 'Contaminantes:  '+listado_compo(num)
  # Asignamos al mapa los atributos de la estación y su ubicación
  fl.Marker([data.Latitud[i], data.Longitud[i]], popup = popup, tooltip = tooltip).add_to(map2)
"""