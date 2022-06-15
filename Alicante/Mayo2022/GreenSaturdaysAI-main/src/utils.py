#!/usr/bin/env python

import pandas as pd
import numpy as np
import datetime as dt

def join_mapas():
	"""
	join_mapas() genera un único csv para los csvs de /maps
	Return: un único csv con dos columnas extra para diferenciar:
		- Año
		- Contaminante
	"""
	maps_path = "../datasets/maps/"
	anyo = ['2018', '2019']
	contaminante = ['no2', 'pm10', 'pm2-5']

	final = pd.DataFrame()
	
	for i in anyo:
		for k in contaminante:
			path = maps_path+i+"/"+i+"_tramer_"+k+"_mapa_qualitat_aire_bcn.csv"
			df = pd.read_csv(path)
			df['año'] = i
			df['contaminante'] = k
			final = final.append(df)

	path = maps_path+"mapas_qualitat_aire_bcn.csv"
	final.to_csv(path)
	return final

def mediciones_unif(ruta1, ruta2, ruta3):
	'''
	Leemos y unificamos el dataset de contaminantes con los datos de las estaciones y descripción de contaminante:
	'''
	#Leemos los csv y convertimos a dataframe saltando las líneas que no tengan el mismo formato:

	df_21 = pd.read_csv(ruta1+"2020-21.csv")
	df_estaciones_21 = pd.read_csv(ruta2+"2021_qualitat_aire_estacions.csv")
	df_contaminantes = pd.read_csv(ruta3+"qualitat_aire_contaminants.csv")

	#Unificamos dataframes y eliminamos las columnas que no aportan información:
	df_21 = df_21.drop(["CODI_PROVINCIA", "PROVINCIA", "CODI_MUNICIPI", "MUNICIPI"], axis=1)
	df_estaciones_21 = df_estaciones_21.drop(["codi_eoi","Nom_districte","Codi_barri","zqa","Codi_districte","Clas_1"], axis=1)

	#Limpiamos y unificamos con descripción de estaciones el df del 21:
	df_21 = df_21.merge(df_estaciones_21, how='left', left_on="ESTACIO", right_on='Estacio')

	#Sustituimos los contaminantes por sus descripciones:
	df_21 = df_21.merge(df_contaminantes, how='left', left_on="CODI_CONTAMINANT", right_on='Codi_Contaminant')
	df_21 = df_21.drop(["CODI_CONTAMINANT","Unitats"],axis=1)

	return df_21

def integratemetadata(ruta1, ruta2):
	"""
	integratemetadata() arregla el problema de que en las medidas de 2020-21 los contaminantes salen por código en vez de por nombre propio.
	devuelve una copia de las medidas de 2020-2021 con una columna nueva (CONTAMINANTE) con el nombre del contaminante
	"""
	medidas_str = ruta1
	medidas = pd.read_csv(medidas_str)
	
	meta = ruta2
	meta = pd.read_csv(meta)

	# crea diccionario con código de contaminante y nombres, reemplaza la columna
	dic = dict(meta[["Codi_Contaminant","Desc_Contaminant"]].values)
	medidas["CONTAMINANTE"] = medidas["CODI_CONTAMINANT"].replace(dic)
	return medidas

def convert_fecha(cadena):
    '''
    Función que rellena los día y meses de un solo carácter para crear un formato de fecha aaaa-mm-dd
    '''
    dd = cadena.split('/')[0]
    mm = cadena.split('/')[1]
    aaaa = cadena.split('/')[2]
    if int(mm) < 10:
        mm = '0' + mm
    if int(dd) < 10:
        dd = '0' + dd
    return aaaa + '-' + mm + '-' + dd 

def add_festivos_findes(df):
    #Introducimos fecha y eliminamos subcolumnas
    df["fecha"] = df[["DIA", "MES", "ANY"]].astype(str).agg('/'.join, axis=1)
    df = df.drop(["DIA", "MES", "ANY"],axis=1)

    # Creamos una columna que determuine las fecha en las que había confinamiento
    df["confinamiento"] = 0
    confi = pd.date_range(start="15/3/2020", end="21/6/2020", freq="D")
    df['confinamiento'] = df['fecha'].apply(lambda x: 1 if x in confi else 0)

    #Aplicamos los festivos y los fines de semana
    festivos = ["1/1/2018","6/1/2018","30/3/2018","2/4/2018","1/5/2018","21/5/2018","15/8/2018","11/9/2018","24/9/2018","12/10/2018","1/11/2018","6/12/2018","8/12/2018","25/12/2018","26/12/2018","1/1/2019","6/1/2019","19/4/2019","22/4/2019","1/5/20…/9/2019","24/9/2019","12/10/2019","1/11/2019","6/12/2019","8/12/2019","25/12/2019","26/12/2019","1/1/2020","6/1/2020","10/4/2020","13/4/2020","1/5/2020","1/6/2020","24/6/2020","15/8/2020","11/9/2020","24/9/2020","12/10/2020","8/12/2020","25/12/2020","26/12/2020","1/1/2021","6/1/2021","2/4/2021","5/4/2021","1/5/2021","24/6/2021","11/9/2021","12/10/2021","1/11/2021","6/12/2021","8/12/2021","25/12/2021"]
    df['festivo'] = 100
    df['festivo'] = df['fecha'].apply(lambda x: 1 if x in festivos else 0)
    h = df.fecha.unique()

    inicio = pd.datetime.strptime('01/01/2020', '%d/%m/%Y')
    fin = pd.datetime.strptime('31/12/2021', '%d/%m/%Y')

    dates = pd.date_range(start=inicio, end=fin, freq="D")

    aux_finde = []
    aux_fecha = []
    
    for i in range(len(dates)):
        # Extraemos el formato fecha en string de cara al merge con el dataframe
        aux_fecha.append(str(dates[i]).split(' ')[0])
    
        # Cuantificamos el dia de la semana que es finde 
        if dates[i].day_name() == 'Saturday' or dates[i].day_name() == 'Sunday':
            aux_finde.append(1)
        else:
            aux_finde.append(0)

    # Comprobamos que tienen la misma longitud
    dic_findes = dict(zip(aux_fecha , aux_finde))
 
    df['fecha'] = df['fecha'].apply(convert_fecha)
    
    findes = []
    for i in range(len(df.fecha)):
        # Obtenemos la fecha
        fecha = df.fecha[i]
        findes.append(dic_findes.get(fecha))

    df["findes"]=findes
    return df  
  

