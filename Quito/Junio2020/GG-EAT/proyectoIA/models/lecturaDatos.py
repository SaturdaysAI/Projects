#!/usr/bin/python3.7

#importar librerias necesarias 
import numpy as np
import pandas as pd
import json
from os import remove
import os.path as path
import pickle

# Lectura del archivo json
def lecturaArchivo_JSON():
    ubicacion = '/www/proyectoIA/documents/cliente.json'
    with open(ubicacion) as contenido:
        cliente = json.load(contenido)
    return pd.DataFrame([cliente])


# Agregar nuevo cliente al archivo cliente.csv
def generarArchvio_CLIENTE(df_nuevo):
    # Lectura del archivo cliente
    ruta_csv_cliente = '/www/proyectoIA/dataset/cliente.csv'
    df_cliente = pd.read_csv(ruta_csv_cliente,sep=';')
    # Comprobar si  no exite en el registro y guardarlo
    if(df_nuevo.id_cliente[0] not in df_cliente.values):
        df_cliente = pd.concat([df_cliente, df_nuevo], ignore_index=True)
        df_cliente.to_csv(ruta_csv_cliente, sep=';',index=False)


# Generar dataset
def generarData_CLIENTE(df_nuevo):
    ruta_csv_restaurante = '/www/proyectoIA/dataset/restaurante.csv'
    df_restaurante = pd.read_csv(ruta_csv_restaurante,sep=';')
    df_restaurante = df_restaurante.drop(['tipo','nombre','latitud','longitud','raiting','direccion','status','price_level'],axis=1)
    
    columnas = df_nuevo.columns.values
    for i in columnas:
        df_restaurante[i] = df_nuevo[i][0] 
    df_restaurante.to_csv('/www/proyectoIA/dataset/evaluacion.csv', sep=';',index=False)




# Eliminar arcchivo JSON
def eliminarArchivo_JSON():
    file='/www/proyectoIA/documents/cliente.json'
    if (path.exists(file)):
        print('el archivo existe procedo a eliminar')
        remove(file)
    
def existeArchivo_JSON(file):
    if (path.exists(file)):
        return True
    else:
        return False
    

if __name__ == "__main__":

    file='/www/proyectoIA/documents/cliente.json'
    
    if existeArchivo_JSON(file):
        cliente = lecturaArchivo_JSON()

        generarArchvio_CLIENTE(cliente.drop(['ambiente','menu','vegetariana','pollo','carne','comida_rapida','lacteos','menestra'],axis=1))
        
        cliente1 = cliente[['id_cliente','ambiente','menu','vegetariana','pollo','carne','comida_rapida','lacteos','menestra']]
        generarData_CLIENTE(cliente1)

        eliminarArchivo_JSON()

        cliente = cliente[['genero','ambiente','vegetariana','carne','pollo','lacteos','menu','comida_rapida','menestra']]
    
        infile = open('/www/proyectoIA/models/GG_Bayes.sav','rb')
        NB_ajustado = pickle.load(infile)
        infile.close()
        y=NB_ajustado.predict(cliente)
        print("El resultado es: ", y)
        #df.loc[:, df.columns != 'gustar']
    else:
        print('archivo cliente.json no existe')