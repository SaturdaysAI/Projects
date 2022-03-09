# -*- coding: utf-8 -*-
"""
Programa Machine Learning contra tablas

Created on Fri Jan 28 20:57:02 2022

@author: GERMÁN

"""

from terminal import preprocesamiento, terminal, confirma, borrarPantalla, es_flotante, imprimeLineasConMarco
import os
import sys
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import model_selection
import seaborn as sns
# https://stackabuse.com/ultimate-guide-to-heatmaps-in-seaborn-with-python/
# https://www.analyticslane.com/2018/07/20/visualizacion-de-datos-con-seaborn/
import matplotlib.pyplot as plt
# %matplotlib inline
from sklearn.model_selection import train_test_split #ML library
from sklearn.metrics import classification_report
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.datasets import make_blobs
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from xgboost import XGBClassifier
import scipy.cluster.hierarchy as shc
import pyreadstat
from sklearn.metrics import classification_report
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.datasets import make_blobs
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from xgboost import XGBClassifier
import scipy.cluster.hierarchy as shc

import pyreadstat
from kmodes.kmodes import KModes
from sklearn import preprocessing
from kmodes.kprototypes import KPrototypes

# =============================================================================
# Variables globales para esta sección: global dfTrab , meta 
df = dfTrab = meta = Xtrain = Ytrain = Xtest = Ytest = listaVarsYX = listaCategoricas = None

def leeDatos(archivo):
    # EJEMPLO: leeDatos("archivo.csv")
    global df, dfTrab , meta, Xtrain, Ytrain, Xtest, Ytest
    df = dfTrab = meta = Xtrain = Ytrain = Xtest = Ytest = None
    if os.path.isfile(archivo) :
        if archivo[-4:].lower() == ".sav":
            dfTrab , meta = pyreadstat.read_sav(archivo)
            df = dfTrab
        elif archivo[-4:].lower() == ".csv":
            dfTrab = pd.read_csv(archivo)
            df = dfTrab
        else:
            print("ERROR. Archivo ", archvo, "no es del tipo esperado.")
    else:
        print("ERROR. Archivo ", archvo, "no encontrado.")

def guardaDataFrameCSV(df, arch):
    arch = arch.strip()
    if arch[-4:].lower() == ".csv" :
        arch = arch[:-4]
    arch += ".csv"
    df.to_csv(arch, index = False)

def abreDataFrameCSV(df, arch) :
    arch = arch.strip()
    if arch[-4:].lower() == ".csv" :
        arch = arch[:-4]
    arch += ".csv"
    if os.path.isfile(arch) :
        df2 = pd.read_csv(arch)
        return df2
    else :
        print("No encontrado fichero ", arch)
        return None

# =============================================================================

def listaToStr(l) :
    '''
    l es una lista de strings, cada string representa una línea de texto. Devuelve un string con '\n\n' separando las líneas.
    Parameters
    ----------
    l : TYPE list
    Returns
    -------
    TYPE: str
    '''
    s = ""
    if len(l) > 0:
        for v in l:
            s += v + "\n\n"
    return s

def quitaUltLin(s):
    p = s.rfind("\n")
    if p >= 0:
        return s[:p-1]
    else : 
        return ""
    
def quitaPrimLin(s):
    p = s.rfind("\n")
    if p >= 0:
        return s[p+1:]
    else :
        return ""
    
def metaLin(meta, col):
    if meta != "":
        return str(col) + ": " + meta.column_names[col] + ": " + str(meta.column_labels[col]) + " (" + str(meta.column_names_to_labels[meta.column_names[col]]) + ")"
    else:
        return ""

def metaToList(meta) :
    l = []
    if meta != "":
        for col in range(len(meta.column_names)):
            l.append(metaLin(meta, col))
    return l

# Ejemplo: print(listaToStr(metaToList(meta)))

def is1Command(l, s):
    # Verifica que es un comando de texto sin más parámetros.
    if len(l) == 1  and type(l[0]) == str and l[0].lower() == s.lower():
        return True
    else:
        return False

def is2CommandStr(l, s):
    # Verifica que es un comando de dos parámetros, el primero el comando s y el segundo es de tipo texto.
    if len(l) == 2  and type(l[0]) == str and l[0].lower() == s.lower() and type(l[1]) == str:
        return True
    else:
        return False

def is2CommandInt(l, s):
    # Verifica que es un comando de dos parámetros, el primero el comando s y el segundo es de tipo entero.
    if len(l) == 2  and type(l[0]) == str and l[0].lower() == s.lower() and type(l[1]) == int:
        return True
    else:
        return False

def is2CommandFloat(l, s):
    # Verifica que es un comando de dos parámetros, el primero el comando s y el segundo es de tipo número.
    if len(l) == 2  and type(l[0]) == str and l[0].lower() == s.lower() and (type(l[1]) == int or type(l[1]) == float):
        return True
    else:
        return False

def esListaEnteros(l, desde):
    if type(l) == list and len(l) > 0:
        for indice, valor in enumerate(l):
            if indice >= desde and type(valor) != int:
                return False
        return True
    return False

def numEnColumna(l, s) :
    # Devuelve el índice de l (lista) donde se encuenta s. Es como un l.index(s) pero ignorando mayúsculas o minísculas.
    n = -1
    try:
        laux = [v.strip().lower() for v in l]
        n = laux.index(s.strip().lower())
    except:
        n = -1
    return n

def listaLower(l) :
    return [v.strip().lower() for v in l]

def verStrMuyLarga(s, numLineasPause):
    l = s.split("\n")
    nTot = len(l)
    lin = 0
    while lin < len(l):
        if lin> 0 and lin % numLineasPause == numLineasPause-1 :
            resp = input("¿Continuar [/N]?: ")
            if resp == "n" or resp == 'N':
                return
            elif resp.isdigit() and int(resp) >= 0 and int(resp) < len(l)-2:
                lin = int(resp)+2
            elif len(resp) > 0 and resp[0] == "+" and resp[1:].isdigit() and lin+int(resp[1:]) >= 0 and lin+int(resp[1:]) < len(l)-2:
                lin += int(resp[1:])
            elif len(resp) > 0 and resp[0] == "-" and resp[1:].isdigit() and lin-int(resp[1:]) < len(l)-2:
                lin -= int(resp[1:])
                if lin < 0:
                    lin = 0
            elif is2CommandStr(preprocesamiento(resp), "G"):
                # Guardar fichero s en prepocesamiento(resp)[1]
                with open(preprocesamiento(resp)[1], 'w') as f:
                    if not f.closed:
                        f.writelines(s)
            else:
                print (l[0]+"\n" + l[1])  # Cabecera y subrayado
        print(l[lin])
        lin += 1

def multidivideStr(s , l):
    '''
    S = "VER 1,5,7 ORDEN: 5d,1a FILTRO: NACE == 5"
    L = divideStr(S, ["VER","ORDEN:","FILTRO:","NADA"])
    print(L)  --> ['VER 1,5,7', 'ORDEN: 5d,1a', 'FILTRO: NACE == 5', '']
        
    S = "VER 1,5,7 FILTRO: NACE == 5 ORDEN: 5d,1a"
    L = divideStr(S, ["VER","ORDEN:","FILTRO:","NADA"])
    print(L) --> ['VER 1,5,7', 'ORDEN: 5d,1a', 'FILTRO: NACE == 5', '']
    
    Además no importan mayúsculas y minúsculas.

    '''
    n = len(l)
    result = ["" for x in range(n)]
    pos = []
    c = s.lower()
    for i in range(n):
        pos.append((i , c.find(l[i].lower())))
    pos.sort(key = lambda x: x[1])
    for i in range(n):
        if pos[i][1] > -1:
            if i == n-1:
                result[pos[i][0]] = s[pos[i][1]:].strip()
            else:
                result[pos[i][0]] = s[pos[i][1]:pos[i+1][1]].strip()
    return result
    
#------------------------------------------------------------------------------

def ListadoColumnas(df):
    """ Devuelve cadena con información amplia de un dataFrame. """
    s = "\n INFORMACIÓN NOMBRE COLUMNAS DEL DATAFRAME"
    s +="\n+-----------------------+-----------------------+-----------------------+-----------------------+"
    s +="\n| Nº    ID. COLUMNA     | Nº    ID. COLUMNA     | Nº    ID. COLUMNA     | Nº    ID. COLUMNA     |"
    s +="\n+-----------------------+-----------------------+-----------------------+-----------------------+"
    n = 4
    nlin = int((len(df.columns)-1)/n)
    if nlin == 0 or nlin % n > 0:
        nlin += 1
    for i in range(nlin):
        s1 = df.columns[i]
        n2 = s2 = ""
        if i+nlin < len(df.columns):
            n2 = str(i+nlin)
            s2 = df.columns[i+nlin]
        n3 = s3 = ""
        if i+2*nlin < len(df.columns):
            n3 = str(i+2*nlin)
            s3 = df.columns[i+2*nlin]
        n4 = s4 = ""
        if i+3*nlin < len(df.columns):
            n4 = str(i+3*nlin)
            s4 = df.columns[i+3*nlin]
        s +="\n|{0:>4}    {4:<15}|{1:>4}    {5:<15}|{2:>4}    {6:<15}|{3:>4}    {7:<15}|".format(i, n2, n3, n4, s1, s2, s3, s4)
    s += "\n+-----------------------+-----------------------+-----------------------+-----------------------+"
    return s

def infoDataFrame(df) :
    print("Número de registros:" + str(df.shape[0]) + "\nNúmero de campos:" + str(df.shape[1]) + "\n")
    if df.shape[0] > 6:
        head_tail_slice = list(range(5))+list(range(-5,0))
        print(quitaUltLin(str(df.iloc[head_tail_slice])))
    else:
        print(str(df.head(df.shape[0])))

def infoIColDF2(df, c):
    c = numColumna(df, c)
    s = "\n INFORMACIÓN DATOS DE COLUMNA " + str(c) + " '" + df.columns[c] + "':\n\n"
    describe = "    Estadísticas\n" + str(df[df.columns[c]].describe())
    describe = describe[:describe.rfind("\n")]
    s += describe
    s += "\n\n    Distribución\n"
    miSerie = df[df.columns[c]].value_counts(dropna = False)
    # https://re-thought.com/pandas-value_counts/
    inf = str(miSerie)
    s += inf[:inf.rfind("\n")]
    s += "\nNúmero de valores distintos: "+ str(len(miSerie))
    # plt.clf()   # https://www.it-swarm-es.com/es/matplotlib/cuando-usar-cla-clf-o-close-para-borrar-un-grafico-en-matplotlib/941340826/
    if (len(miSerie) < 50) : # Con un número muy elevado de datos, la representación gráfica se cuelga.
        sns.countplot(data=df, x=df.columns[c], order=df[df.columns[c]].value_counts(dropna=False).index)
        plt.show()
    del miSerie
    return s

def infoIColDF(df, c):
    c = numColumna(df, c)
    s = "\n INFORMACIÓN DATOS DE COLUMNA " + str(c) + " '" + df.columns[c] + "':\n\n"
    describe = "    Estadísticas\n" + str(df[df.columns[c]].describe())
    describe = describe[:describe.rfind("\n")]
    s += describe
    s += "\n\n    Distribución\n"
    miSerie = df[df.columns[c]]
    counts = miSerie.value_counts(dropna = False)
    percent = miSerie.value_counts(dropna = False, normalize = True).mul(100).round(1).astype(str) + '%'
    dfAux = pd.DataFrame({'Núm.': counts, '%Porc.':percent})
    s += str(dfAux)
    # https://softhints.com/pandas-count-percentage-value-column/
    # https://re-thought.com/pandas-value_counts/
    s += "\nNúmero de valores distintos: "+ str(len(counts))
    plt.clf()   # https://www.it-swarm-es.com/es/matplotlib/cuando-usar-cla-clf-o-close-para-borrar-un-grafico-en-matplotlib/941340826/
    if (len(counts) < 50) : # Con un número muy elevado de datos, la representación gráfica se cuelga.
        sns.countplot(data=df, x=df.columns[c], order=df[df.columns[c]].value_counts(dropna=False).index)
        plt.show()
    del miSerie
    return s

def listaColumnasConNan(df) :
    contador = 0
    numNulos = 0
    s = "DISTRIBUCIÓN DE np.nan POR COLUMNAS:\n"
    for index, c in enumerate(df.columns) :
        inf = df[c].value_counts(dropna = False)
        if np.nan in inf.index :
            contador += 1
            numNulos += inf[np.nan]
            s += "{:>5}   {:<15} {:>6}  {:>10}\n".format(index, c, inf[np.nan], "( "+str(round(inf[np.nan]/df.shape[0]*100,1))+"% )")
            # s += str(index) + ": "+ c + ": " + str(inf[np.nan]) + " (" + str(round(inf[np.nan]/df.shape[0]*100,1)) + "%).\n"
    if numNulos == 0:
        s += "No hay datos np.nan."
    else :
        s += "\nTotal " + str(contador) + " columnas tienen np.nan. Total " + str(numNulos) + " elementos son np.nan (" + str(round(numNulos/(df.shape[0]*df.shape[1])*100, 1)) + " %)."
    return s

def nombreColumna(df, n) :
    """ Devuelve el nombre de la columna del dataframe. n puede ser:
        - un número entero o una cadena que representa un número, si está en el rango devolverá el nombre de la columna.
        - Un nombre. Si corresponde a un nombre de columna, devuelve el mismo mombre.
        Si no se encuentra la columna (nombre no existe o entero fuera de rango) devuelve "".
    """
    if type(n) == str :
        n.strip()
    if type(n) == str and n.isdigit() :
        n = int(n)
    if type(n) == int :
        if n >= 0 and n < df.shape[1] :
            return df.columns[n]
        else :
            return ""
    if type(n) == str :
        n = numEnColumna(df.columns, n)
        if n >= 0:
            return df.columns[n]
    return ""


def numColumna(df, nombre) :
    """ Devuelve el número de columna. nombre puede ser:
        - Un entero con el número. Si está dentro del rango devolverá el mismo número.
        - Una cadena con el número de la columna, si éste es un número dentro del rango, devuelve el número.
        - El nombre de una columna. Si el df tiene una columna con ese nombre, devuelve su índice.
        Si no se encuentra devuelve -1.
    """
    n = -1
    if type(nombre) == str:
        nombre.strip()
        if nombre.isdigit():
            n = int(nombre)
        else:
            try:
                n = numEnColumna(df.columns, nombre)
            except:
                n = -1
    elif type(nombre) == int:
        n = nombre
    if n >= 0 and n < df.shape[1]:
        return n
    else:
        return -1

def listaColsToListaNombreCols(df, l) :
    return [nombreColumna(df, col) for col in l]

def listaColsToListaNumsCols(df, l) :
    return [numColumna(df, col) for col in l]
    
def verDatosColumnas(df, listaCols, strFiltro, listaOrden) :
    print("Listado columnas:", listaCols)
    # Primero validamos las columnas en la lista pasada. Si no se encuentra, se elimina.
    for i in range(len(listaCols)-1, -1, -1):
        if numColumna(df, listaCols[i]) == -1:
            print("ERROR: No encontrada columna ", listaCols.pop(i))
        else:
            listaCols[i] = nombreColumna(df, listaCols[i])
    if len(listaCols) == 0:
        listaCols = list(df.columns)
        
    ldir = []
    if len(listaOrden) > 0:
        for i, e in enumerate(listaOrden): # 34_a, NACE_d,..
            if str(e)[-2:] == "_d":
                ldir.append(False)
                listaOrden[i] = e[:-2]
            elif str(e)[-2:] == "_a":
                ldir.append(True)
                listaOrden[i] = e[:-2]
            else:
                ldir.append(True)
            listaOrden[i] = nombreColumna(df, listaOrden[i])
            
        for i in range(len(listaOrden)-1, -1, -1):
            if numColumna(df, listaOrden[i]) == -1:
                print("ERROR: No encontrada columna ", listaOrden.pop(i), "especificada para orden.")
                ldir.pop(i)
            else:
                listaCols[i] = nombreColumna(df, listaCols[i])

    #Construimos cabecera en las dos primeras líneas:
    s = "  NUM   "
    sSub = " ====="
    for c in listaCols: # Nombres de columnas seleccionadas
        # listaColumnasNumero.append(numColumna(df,c))
        s += "{:<19}".format(str(numColumna(df, c)) + " "+ nombreColumna(df, c))
        sSub += "  ================="
    s +="\n"+sSub
    # Ahora pasamos parámetros a las funciones de la librería.
    arry = []
    dfaux = []
    if strFiltro != "":
        try:
            dfaux = df.query(strFiltro)
            if len(listaOrden) > 0:
                dfaux.sort_values(by=listaOrden, ascending=ldir, inplace=True)
            arry = dfaux.loc[:, listaCols].values
        except:
            print("Filtro '" + strFiltro + "' sin éxito")
            if len(listaOrden) > 0:
                dfaux = df.sort_values(by=listaOrden, ascending=ldir)
                arry = dfaux.loc[:, listaCols].values
            else:
                arry = df.loc[:, listaCols].values
        
    else:
        if len(listaOrden) > 0:
            dfaux = df.sort_values(by=listaOrden, ascending=ldir)
            arry = dfaux.loc[:, listaCols].values
        else:
            arry = df.loc[:, listaCols].values
            
    # A partir de aquí trabajamos con el array arry para construir la cadena a devolver.
    if len(arry) > 0:
        print("Filas:", len(arry), "; Columnas:", len(arry[0]))
    else:
        print("No hay datos")
    for fila in range(len(arry)):
        # s += "\n" + str(fila)
        s += "\n{:>5}   ".format(int(fila))
        for col in range(len(arry[fila])):
            s += "{:<19}".format(arry[fila][col])
    del arry
    del dfaux
    return s



def setDatosColumnas(df, listaCols, strFiltro, listaOrden) :
    print("Listado columnas:", listaCols)
    # Primero validamos las columnas en la lista pasada. Si no se encuentra, se elimina.
    for i in range(len(listaCols)-1, -1, -1):
        if numColumna(df, listaCols[i]) == -1:
            print("ERROR: No encontrada columna ", listaCols.pop(i))
        else:
            listaCols[i] = nombreColumna(df, listaCols[i])
    
    ldir = []
    if len(listaOrden) > 0:
        for i, e in enumerate(listaOrden): # 34_a, NACE_d,..
            if str(e)[-2:] == "_d":
                ldir.append(False)
                listaOrden[i] = e[:-2]
            elif str(e)[-2:] == "_a":
                ldir.append(True)
                listaOrden[i] = e[:-2]
            else:
                ldir.append(True)
            listaOrden[i] = nombreColumna(df, listaOrden[i])
            
        for i in range(len(listaOrden)-1, -1, -1):
            if numColumna(df, listaOrden[i]) == -1:
                print("ERROR: No encontrada columna ", listaOrden.pop(i), "especificada para orden.")
                ldir.pop(i)
            else:
                listaCols[i] = nombreColumna(df, listaCols[i])

    # Ahora pasamos parámetros a las funciones de la librería.
    if strFiltro != "":
        try:
            df.query(strFiltro, inplace=True)
        except:
            print("Filtro '" + strFiltro + "' sin éxito")
    if len(listaOrden) > 0:
        df.sort_values(by=listaOrden, ascending=ldir, inplace=True)
        
    if len(listaCols) > 0:
        for c in df.columns:
            if c not in listaCols:
                df.drop([c], axis='columns', inplace=True)


def nuevaColumna(df, colIni, listaIni, colFin, listaFin, confirmar=True) :
    """ Genera una nueva columna a partir de otra, cmbiando sus valores.
        colIni es la columna de la que se parten los datos.
        listaIni son los datos que deben cambiarse.
        colFin es el nuevo nombre de la columna.
        listaFin es cómo debe transformar los datos de listaIni.
        Si colFin se omite, sustituirá la columna de la que se parten los datos.
        Si colFin no existe en el dataFrame, se pondrá inmediatamente después de colIni.
        Si colFin existe previamente, sustituirá a esa columna.
    """
    
    def normalizaLista(lista):
        for index, value in enumerate(lista) :
            if type(value) == str:
                value = value.strip()
                if value.lower() == "nan":
                    value = np.nan
                elif es_flotante(value) :
                    value = float(value)
                lista[index] = value
        
    # print("nuevaColumna(df, ", colIni, ",", listaIni, ",", colFin, ",", listaFin,")")
    # Primera parte, depuración de datos.
    colIni = nombreColumna(df, colIni)
    if colIni == "":
            print("ERROR, no encontrada cadena origen")
            return -1
    
    if colFin == "":
        colFin = colIni
    else :
        colF = nombreColumna(df, colFin)    # colFin puede especificarse por el nombre o por el número.
        if colF != "":
            colFin = colF

    normalizaLista(listaIni)    
    normalizaLista(listaFin)

    if confirmar:
        if len(listaIni) != len(listaFin) :
            print("ERROR: el número de elementos de las listas no coinciden.")
            return -1
        # Informamos de qué se va a hacer con los datos y pedimos confirmación.
        print("Genera Nueva columna:\nColumna inicial:", colIni,"\nLista valores:", listaIni,"\nColumna Nueva:", colFin,"\nLista valores:", listaFin)
        if colFin in df.columns :
            print("La nueva columna sustituirá a la columna", colFin)
        else:
            print("La nueva columna", colFin,"se situará a continuación de la columna", colIni)

        if not confirma() :
            return -1
    
    # Generamos en l los valores de la nueva columna.
    contador = 0
    l = []      # En esta lista ponemos los elementos de la nueva columna, para todos los registros
    for v in df[colIni]:
        if not type(v) == str and np.isnan(v) :
            v = np.nan
        if v in listaIni:
            l.append(listaFin[listaIni.index(v)])
        else:
            l.append(v)
        contador += 1
    
    if colF in df.columns :
        pos = list(df.columns).index(colFin)
        df.drop([colFin], axis='columns', inplace=True)
        df.insert(pos, colFin, l)
    else:
        pos = list(df.columns).index(colIni) + 1
        df.insert(pos, colFin, l)

    if "_MEDIA_" in listaFin or "_MEDIANA_" in listaFin or "_MODA_" in listaFin or "_MIN_" in listaFin or "_MAX_" in listaFin:
        s = str(df[colFin].value_counts(dropna = False, normalize = True))
        est = s.split('\n')
        media=0
        aux1 = 0
        moda = None
        minim = None
        maxim =  None
        l = []
        for s in est:
            aux = s.split()
            if  es_flotante(aux[0]):
                l.append((aux[0], aux[1]))
                if minim == None or minim > float(aux[0]):
                    minim = float(aux[0])
                if maxim == None or maxim < float(aux[0]):
                    maxim = float(aux[0])
                aux1 += float(aux[1])
                media += float(aux[0]) * float(aux[1])
                if moda is None:
                    moda = float(aux[0])
        media /= aux1
        # mediana = df.median(numeric_only=True)[pos]
        l.sort(key = lambda x: x[0])
        # print(l)
        mediana = None
        aux2 = 0
        for valor in l:
            if  es_flotante(valor[0]):
                aux2 += float(valor[1])
                if mediana == None and aux1*aux2 > 0.5:
                    mediana = valor[0]
                    break
        # print("\n Media:", media, "; Moda:", moda, "Mediana:", mediana, "Max:", maxim, "Min:", minim, "\n")
        nuevaColumna(df, colFin, ["_MEDIA_", "_MODA_", "_MEDIANA_","_MAX_", "_MIN_"], colFin, [media, moda, mediana, maxim, minim], confirmar = False)
    return contador

        
def correlacion(df) :
    limiteCorrelacion = 0.3
    corr = df.corr(method="pearson")    # Métodos posibles: 'pearson', 'kemdall', 'spearman', 'callable'
    # Ver https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.corr.html
    s = "Matriz de correlaciones (Pearson):\n"
    s += str(corr) + "\n"
    # sns.heatmap(corr,xticklabels=corr.columns.values,yticklabels=corr.columns.values,annot=True)
    # plt.show()
    cont = 0;
    s += "\n Pares de variables correladas (>" + str(limiteCorrelacion) + "):\n"
    for i in range(corr.shape[0]-1):
        for j in range(i+1, corr.shape[1]):
            if corr.values[i, j] > limiteCorrelacion :
                s += "\n{:>12}  -  {:<12}  :  {:<6}".format(df.columns[i], df.columns[j], round(corr.values[i,j],2))
                cont += 1
            elif corr.values[i, j] < -limiteCorrelacion :
                s += "\n{:>12}  -  {:<12}  :  {:<6}".format(df.columns[i], df.columns[j], round(corr.values[i,j],2))
                cont += 1
    s += "\n\nTotal " + str(cont) + " columnas correlacionadas."
    return s

def normaliza(df, columna, vInf, vSup) :
    sCol = nombreColumna(df, columna)
    if sCol == "":
        print("Error al normalizar columna", columna)
        return
    estadisticas = str(df[sCol].describe())
    linEst = estadisticas.split('\n')
    minim = maxim = 0
    for lin in linEst:
        words = lin.split()
        if words[0] == "min":
            minim = float(words[1])
        if words[0] == "max":
            maxim = float(words[1])
    if maxim <= minim:
        print("ERROR al normalizar. Máximo y mínimo coinciden")
    l = []      # En esta lista ponemos los elementos de la nueva columna, para todos los registros
    k = (vSup-vInf)/(maxim-minim)
    for v in df[sCol]:
        if not type(v) == str and np.isnan(v) :
            l.append(np.nan)
        elif es_flotante(v):
            if maxim == minim:
                l.append((vInf+vSup)/2)
            else:
                l.append((v-minim) * k + vInf)
        else:
            l.append(v)
    pos = list(df.columns).index(sCol)
    df.drop([sCol], axis='columns', inplace=True)
    df.insert(pos, sCol, l)

def dropnaF(df, v) :
    """ Elimina filas con NaN si de esta forma quitamos todos los NaN de la columna,
    no quitando un total de v filas """
    while True :
        nNan = v+1
        cNan = -1
        for c in range(df.shape[1]) :
            inf = df[df.columns[c]].value_counts(dropna = False)
            if np.nan in inf.index :
                nNan_c = inf[np.nan]    # nº de np.nan que tiene la columna nº c.
                if nNan > nNan_c and nNan_c > 0 and nNan_c <= v:
                    nNan = nNan_c
                    cNan = c
        if cNan > -1:
            df.dropna(subset = [df.columns[cNan]], inplace=True)
            v -= nNan
        else :
            break

def dropnaC(df, v) :
    """ Elimina columnas con número de NaN mayor a v. """
    for c in range(df.shape[1]-1, -1, -1) :
        inf = df[df.columns[c]].value_counts(dropna = False)
        if np.nan in inf.index :
            nNan = inf[np.nan]    # nº de np.nan que tiene la columna nº c.
            if nNan > v:
                df.drop([df.columns[c]], axis='columns', inplace=True)

# ===============================================================================

def numValoresDistintos(df, col):
    miSerie = df[nombreColumna(df,col)].value_counts(dropna = False)
    return len(miSerie)

def valorMasFrecuente(df, col):
    miSerie = df[nombreColumna(df,col)].value_counts(dropna = False)
    strMasRepetido = str(miSerie).split("\n")[0].split()
    print(strMasRepetido[0], strMasRepetido[1], df.shape[0])
    if es_flotante(strMasRepetido[0]):
        return float(strMasRepetido[0]) , int(strMasRepetido[1]) , int(df.shape[0])
    else:
        return strMasRepetido[0] , int(strMasRepetido[1]) , int(df.shape[0])
    

def preAnalisis(df):
    global listaVarsYX
    if listaVarsYX == None:
        print("Se debe definir columnas YX")
        return ""
    else:
        s = "\nAnálisis de complejidad:\n"
        s += "Número de valores distintos de variable dependiente: " + listaVarsYX[0] + ":" + str(numValoresDistintos(df, listaVarsYX[0])) + "\n"
        s += "Número de valores distintos de variables independientes:   "
        comb = 1
        for c in listaVarsYX[1:]:
            n = numValoresDistintos(df, c)
            comb *= n
            s += c + ": (" + str(n) + ").  "
        s += "\n\nCombinaciones posibles: "
        if comb > 1E6:
            s += format(comb,'.1E')
        else:
            s += str(comb)
        return s

class modeloMax:
    def __init__(self):
        self.v = 0
        self.feature_importances_ = "No implementado"

    def __del__(self):
        pass

    def fit(self, Xtrain, y_train):
        global Ytrain, listaVarsYX
        if listaVarsYX == None:
            return ""
        self.v, n, tot = valorMasFrecuente(Ytrain, listaVarsYX[0])
    
    def predict(self, X):
        return np.array([self.v for i in range(X.shape[0])])
    

    
def analisisModelo(model):
    global df, dfTrab, Xtrain, Ytrain, Xtest, Ytest, listaVarsYX
    if listaVarsYX is None :
        return "ERROR en la ejecuón de modelo: no definidas variables YX"
    s = "<LINEA>\n"
    y_train = Ytrain[Ytrain.columns[0]]
    y_test = Ytest[Ytrain.columns[0]]

    s += "Resultados sobre datos de entrenamiento:\n"
    s += "<LINEA>\n"
    model.fit(Xtrain, y_train)
    predictionTrain = model.predict(Xtrain)  # Es una columna que devuelve para cada registro de Xtrain, el valor Y que se ha predecido.
    s += classification_report(y_train, predictionTrain)  # Devuelve precision, recall y f1-score para cada valor existente.
    
    s += "<LINEA>\n"
    acc  = accuracy_score(y_train, predictionTrain)
    s += "Accuracy (exactitud)      : " + str(round(acc, 4)) + '\n'  # Devuelve el % de veces que prediction coincide con y_test.
    prec = precision_score(y_train, predictionTrain, average="weighted")
    s += "Aciertos    : "  + str(round(prec, 4)) + '\n' # 
    rec  = recall_score(y_train, predictionTrain, average="weighted")
    s += "Precision   : " + str(round(rec, 4)) + '\n'
    f1   = f1_score(y_train, predictionTrain, average="weighted")
    s += "F1 Score    : " + str(round(f1, 4)) + '\n'
    s += "<LINEA>\n<LINEA>\n"
    s += "Resultados sobre datos de test:\n"
    s += "<LINEA>\n"
    prediction = model.predict(Xtest)  # Es una columna que devuelve para cada registro de Xtest, el valor Y que se ha predecido.
    s += classification_report(y_test, prediction) + '\n'  # Devuelve precision, recall y f1-score para cada valor existente.
    s += "<LINEA>\n"
    conf = confusion_matrix(y_test, prediction)
    s += "Confusion Matrix: \n" + str(conf) + "\n\n"   # Por filas: casos reales, por columnas: predicciones.
    s += "<LINEA>\n"
    acc  = accuracy_score(y_test, prediction)
    s += "Accuracy (exactitud)      : " + str(round(acc, 4)) + '\n'  # Devuelve el % de veces que prediction coincide con y_test.
    prec = precision_score(y_test, prediction, average="weighted")
    s += "Aciertos    : "  + str(round(prec, 4)) + '\n' # 
    rec  = recall_score(y_test, prediction, average="weighted")
    s += "Precision   : " + str(round(rec, 4)) + '\n'
    f1   = f1_score(y_test, prediction, average="weighted")
    s += "F1 Score    : " + str(round(f1, 4)) + '\n'

    if hasattr(model, 'feature_importances_') and model.feature_importances_ != "No implementado":
        s += "<LINEA>\n"
        s += "Peso variables:\n"
        importance = model.feature_importances_
        #https://inria.github.io/scikit-learn-mooc/python_scripts/dev_features_importance.html
        s += str(importance) + '\n'
        indices = np.argsort(importance)
        fig, ax = plt.subplots()
        ax.barh(range(len(importance)), importance[indices])
        ax.set_yticks(range(len(importance)))
        _ = ax.set_yticklabels(np.array(Xtrain.columns)[indices])
    s += "<LINEA>"
    return s
        
def analisisModelo2(model) :
    global df, dfTrab, Xtrain, Ytrain, Xtest, Ytest, listaVarsYX
    # dfaux = df.dropna(subset = listaVarsYX, inplace = true)
    if listaVarsYX is None :
        return "ERROR en la ejecuón de modelo: no definidas variables YX"
    print("Si continúas se eliminarán las filas con NaN.")
    if not confirma():
        return "Se cancela aplicación de modelo"
    df.dropna(subset = listaVarsYX, inplace = True)
    s = "\n<LINEA>\n"
    dfmodelo2 = df[listaVarsYX]
    y = model.fit_predict(dfmodelo2)
    dfmodelo2["Cluster"] = y
    dfTrab["Cluster"] = y
    ngrupos = len(pd.Series(y).value_counts())
    if ngrupos > 1:
        s += "Número de grupos: " + str(ngrupos) + ".\n"
        silhouette_avg = silhouette_score(dfmodelo2, y)    # mejor 0 / peor 1,
        s += "The average silhouette_score is: " + str(silhouette_avg)
        if hasattr(model, 'inertia_'):
            distortions = model.inertia_
            s += "\nThe distorsion is: " + str(distortions)
    if hasattr(model, 'cluster_centers_') or hasattr(model, 'cluster_centroids_'):
        if hasattr(model, 'cluster_centers_'):
            centers = model.cluster_centers_
        else:
            centers = model.cluster_centroids_
        s += "\n<LINEA>\nCentros:\n" + str(centers)
        print("Deseas realizar un análisis de centros")
        if confirma():
            print("Dimensión del array de centros", centers.shape)
            difGrande = 0.5
            for j in range(centers.shape[1]) :
                maxim = 0
                minim = 1
                for i in range(centers.shape[0]):
                    if maxim is None or abs(centers[i][j]) > maxim :
                        maxim = abs(centers[i][j])
                    if abs(centers[i][j]) < minim :
                        minim = abs(centers[i][j])
                if maxim-minim > difGrande:
                    print("Diferencia en variable", j, "vale", maxim-minim)
    
    s += "\n<LINEA>\n"
    s += "La clasificación de las filas queda distribuido en los siguientes grupos:\n"
    s += infoIColDF(dfmodelo2, "Cluster")+"\n<LINEA>"
    print("A continuación se muestra el dataframe, con columna 'Cluster' la clasificiación hecha para cada fila.")
    if confirma():
        verStrMuyLarga(verDatosColumnas(dfmodelo2, listaVarsYX+["Cluster"], "", ""), 25)
    return s


def analisisModeloKPrototipos(model) :
    # model = KPrototypes(n_clusters=k, init='Cao')
    # https://medium.com/analytics-vidhya/customer-segmentation-using-k-prototypes-algorithm-in-python-aad4acbaaede
    # https://medium.com/analytics-vidhya/clustering-on-mixed-data-types-in-python-7c22b3898086
    # https://github.com/nicodv/kmodes/blob/master/kmodes/kprototypes.py
    global df, dfTrab, Xtrain, Ytrain, Xtest, Ytest, listaVarsYX, listaCategoricas
    # from sklearn import preprocessing
    print("No debe haber valores NaN, si continúas se eliminarán las filas con NaN.")
    if not confirma():
        return "Se cancela aplicación de modelo"
    df.dropna(subset = listaVarsYX, inplace = True)
    # Escalamos variables numéricas
    if listaVarsYX is None :
        return "ERROR en la ejecuón de K-prototypes: no definidas variables YX"
    elif listaCategoricas is None :
        return "ERROR en la ejecuón de K-prototypes: no definidas variables categóricas"
    scaler = preprocessing.MinMaxScaler()
    dfkProt = df[listaVarsYX].copy()
    listaNumCols = [x for x in listaVarsYX if x not in listaCategoricas]
    print("Control 1: lista variables numéricas:", listaNumCols, "Les aplicamos normalización de datos.")
    dfkProt[listaNumCols] = scaler.fit_transform(dfkProt[listaNumCols])
    
    lNumsColsCat = [numColumna(dfkProt, nombre) for nombre in listaCategoricas if nombre in listaVarsYX]
    print("Control 2: lista números de variables categóricas:", lNumsColsCat)
    print("\nEsperar unos minutos..")
    y = model.fit_predict(dfkProt, categorical=lNumsColsCat)
        # diferencia: antes era y = model.fit_predict(dfmodelo2)
    print("YA SE HA EJECUTADO EL MODELO")
    
    s = "\n<LINEA>\n"
    dfkProt["Cluster"] = y
    dfTrab["Cluster"] = y
    
    ngrupos = len(pd.Series(y).value_counts())
    if ngrupos > 1:
        s += "Número de grupos: " + str(ngrupos) + ".\n"
        silhouette_avg = silhouette_score(dfkProt, y)    # mejor 0 / peor 1,
        s += "The average silhouette_score is: " + str(silhouette_avg)
        if hasattr(model, 'inertia_'):
            distortions = model.inertia_
            s += "\nThe distorsion is: " + str(distortions)
    if hasattr(model, 'cluster_centers_') or hasattr(model, 'cluster_centroids_'):
        if hasattr(model, 'cluster_centers_'):
            centers = model.cluster_centers_
        else:
            centers = model.cluster_centroids_
        s += "\n<LINEA>\nCentros:\n" + str(centers)
        print("Deseas realizar un análisis de centros")
        if confirma():
            print("Dimensión del array de centros", centers.shape)
            difGrande = 0.5
            for j in range(centers.shape[1]) :
                maxim = 0
                minim = 1
                for i in range(centers.shape[0]):
                    if abs(centers[i][j]) > maxim :
                        maxim = abs(centers[i][j])
                    if abs(centers[i][j]) < minim :
                        minim = abs(centers[i][j])
                if maxim-minim > difGrande:
                    print("Diferencia en variable", j, "vale", maxim-minim)
    
    s += "\n<LINEA>\n"
    s += "La clasificación de las filas queda distribuido en los siguientes grupos:\n"
    s += infoIColDF(dfkProt, "Cluster")+"\n<LINEA>"
    print("A continuación se muestra el dataframe, con columna 'Cluster' la clasificiación hecha para cada fila.")
    if confirma():
        verStrMuyLarga(verDatosColumnas(dfkProt, listaVarsYX+["Cluster"], "", ""), 25)
    return s

def analisisParticularG1():
    ejecutaComando("A DF1_conNaN.csv")
    ejecutaComando("DROPNA PAISES1, PAISES2, PAISES3, NACE, SIZE, SEX, POS,   RCPUES1, RCPUES2, RCPUES3, RCPUES4")
    ejecutaComando("MERGE DF3_analG1.csv")
    ejecutaComando("K PAISES1, PAISES2, PAISES3, NACE, SIZE, SEX, POS,   RCPUES1, RCPUES2, RCPUES3, RCPUES4, Clust_KPROT5")
    ejecutaComando("G DF4_G1.csv")
    ejecutaComando("L")
    
	# ejecutaComando("SET 1,..,22,39,..,41 filtro: Cluster_KM_4==1.0 ORDEN: 39"
    # Gráficas tipo rádar: https://programmerclick.com/article/9016716044/
    # https://claudiovz.github.io/scipy-lecture-notes-ES/intro/matplotlib/matplotlib.html
    for nc in range(0, df.shape[1]): # -1 porque el cluster no hay que representarlo
        miSerie = df[df.columns[nc]].value_counts(dropna = False)
        print(nombreColumna(df, nc))
        dV = dict(miSerie)  # diccionario ordenado por valores.
        # print("DICCIONARIO:", dV)
        for k in dV:
            rMax = dV[k]
            break
        lok = sorted(dV)    # lista ordenada por claves.
        theta = np.zeros(len(lok)+1)
        r = []
        p = 0
        for k in lok:
            theta[p] = k
            r.append(dV[k])
            p += 1
        rango = (lok[len(lok)-1] - lok[0])*(len(lok)+1)/len(lok)

        
        # transformamos theta a ángulos en radianes:
        for i in range(len(lok)):
            theta[i] = theta[i]/rango*2*np.pi

        # cerramos la curva polar
        theta[len(lok)] = theta[0]
        r.append(r[0]) # r.append(dV[lok[0]])
        
        plt.title(nombreColumna(df, nc))
        plt.polar(theta, r, 'bo-', lw=1)
        plt.fill(theta, r ,facecolor='b',alpha=0.25)
        # plt.polar(theta/(lok[len(lok)-1] - lok[0]+2)*2*np.pi, r, 'bo-', lw=2)
        # plt.fill(theta/(lok[len(lok)-1] - lok[0]+1)*2*np.pi, r ,facecolor='r',alpha=0.25)
        for ind, val in enumerate(lok):
            plt.text(theta[ind], (r[ind]*1.1*0.8 + rMax*0.2), str(val), fontsize=8, horizontalalignment = 'center')
        plt.show()
    ejecutaComando("SET 0,..,10 filtro: Clust_KPROT5==0.0")
        
    
# =============================================================================


def dataFrameTrab() :
    global df, dfTrab, Xtrain, Ytrain, Xtest, Ytest
    if df is dfTrab :
        return "DF"
    elif df is Xtrain :
        return "Xtrain"
    elif df is Ytrain :
        return "Ytrain"
    elif df is Xtest :
        return "Xtest"
    elif df is Ytest :
        return "Xtest"
    else:
        return ""

def promt(n, listaArchivosGrabacion, listaArchivosReproduccion) :
    r = "Instrucción " + str(n)
    if len(listaArchivosGrabacion) > 0: 
        r += '[>'+ listaArchivosGrabacion[len(listaArchivosGrabacion)-1] + ']'
    if len(listaArchivosReproduccion) > 0: 
        r += '[' + listaArchivosReproduccion[len(listaArchivosReproduccion)-1] + '>]'
    # El return devuelve cadena que pone colores. Ver https://python-para-impacientes.blogspot.com/2016/09/dar-color-las-salidas-en-la-consola.html
    return "\x1b[1;33m" + r + "[" + dataFrameTrab() + "]: " + "\x1b[1;34m"

def ejecutaComando(s):
    global df, dfTrab, meta, Xtrain, Ytrain, Xtest, Ytest, listaVarsYX, listaCategoricas
    l = preprocesamiento(s)
    
    if is2CommandStr(l, "G") or is2CommandStr(l, "S") :    # Guarda datos del Dataframe en archivo
        guardaDataFrameCSV(dfTrab, s[2:])
        print("OK")
        
    elif is2CommandStr(l, "A") or is2CommandStr(l, "O") :    # Lee datos del Dataframe de un archovo
        df2 = abreDataFrameCSV(pd, s[2:])
        if  df2 is not None :
            dfTrab = df2
            df = df2
            Xtrain = Ytrain = Xtest = Ytest = None
            print("Ok: (filas. columnas) =", df.shape)
        else:
            print("No OK")
    
    elif is1Command(l, "L"):
        print(ListadoColumnas(df))
        
    
    elif type(l[0]) == int or l[0].lower() in listaLower(df.columns) : # Listas características de las columnas indicadas.
        for c in l:
            if type(c) == int :
                n = c
            elif type(c) == str:
                n = numEnColumna(df.columns, c)
            if n >= 0 and n < df.shape[1]:
                print(infoIColDF(df, n)+"\n")
            else:
                print("ERROR: No encontrada columna", c, "en dataframe.")
            
    elif s == "*" :         # Información de los valores de todas las columnas
        print("Información de todas las columnas (total", df.shape[1], "):")
        for col in range(df.shape[1]) :
            print(infoIColDF(df, col),"\n")
    
            
    elif is1Command(l, "DF") :   # información dataFrame
        if (dfTrab is not None):
            df = dfTrab
            infoDataFrame(df)
        else:
            print("No tenemos definido dataframe")


    elif is1Command(l, "XTrain") :   # información dataFrame
        if (Xtrain is not None):
            df = Xtrain
            infoDataFrame(df)
        else:
            print("No tenemos definido dataframe. Ejecutar instrucción YX")

    elif is1Command(l, "YTrain") :   # información dataFrame
        if (Ytrain is not None):
            df = Ytrain
            infoDataFrame(df)
        else:
            print("No tenemos definido dataframe. Ejecutar instrucción YX")

    elif is1Command(l, "XTest") :   # información dataFrame
        if (Xtest is not None):
            df = Xtest
            infoDataFrame(df)
        else:
            print("No tenemos definido dataframe. Ejecutar instrucción YX")
            

    elif is1Command(l, "YTest") :   # información dataFrame
        if (Ytest is not None):
            df = Ytest
            infoDataFrame(df)
        else:
            print("No tenemos definido dataframe. Ejecutar instrucción YX")

    elif is1Command(l, "MT") or is1Command(l, "Meta"):   # información dataFrame
        if (meta is not None):
            print(listaToStr(metaToList(meta)))
        else:
            print("No hay fichero de metadatos.")
    
    elif type(l[0]) == str and l[0].lower() == "meta" or l[0].lower() == "mt" :
        for c in l[1:]:
            if type(c) == int :
                n = c
            elif type(c) == str:
                n = numEnColumna(dfTrab.columns, c)
            if n >= 0 and n < dfTrab.shape[1]:
                print(metaLin(meta, n))
            else:
                print("ERROR: No encontrada columna", c, "en metadatos.")
    
    elif is1Command(l, "NULL") :   # Columnas que contienen NULL
        print(listaColumnasConNan(df))
    
    elif type(l[0]) == str and l[0].lower() == "v":
        # V N,38,..,40 filtro: NACE==2.0 ORDEN: 38_a, 39_d
        sl = multidivideStr(s , ["V", "FILTRO:", "ORDEN:"])
        # sl[0] = "V N,38,..,40"
        # sl[1] = "filtro: NACE==2.0"
        # sl[2] = "ORDEN: 38_a, 39_d" --> '_a': ascendente; '_d': descendente
        filtro = ""
        if sl[1] != "": # sl[1] cadena de filtro
            filtro = sl[1][8:].strip()  # "NACE==2.0"
            # print("FILTRO: '" + filtro + "'")
        l = preprocesamiento(sl[0]) # ['V','N',38,39,40]
        lo = []
        if sl[2] != "":
            lo = preprocesamiento(sl[2][7:]) # ['38_a', '39_d']
            # print("ORDEN:",lo)
            
        verStrMuyLarga(verDatosColumnas(df, l[1:], filtro, lo), 25)

    elif l[0].lower() == "CORR".lower() :   # Correlación
        if len(l) == 0:
            print(correlacion(df))
        else:
            df2 = df.loc[:,listaColsToListaNombreCols(df, l[1:])]
            print(correlacion(df2))
            del df2
    
    elif is1Command(l, "R") or is1Command(l, "RESET"):     # Reset
        print("Se van a volver al estado inicial leyendo de nuevo los datos.")
        if confirma() :
            dfTrab , meta = pyreadstat.read_sav(archivoTrabajo)
            df = dfTrab
            Xtrain = Ytrain = Xtest = Ytest = None
            print("Hecho.")
    
    elif is1Command(l, "dir"):
        contenido = os.listdir()
        print("Ficheros con Dataframes (.sav o .csv):")
        for nombre in contenido:
            if nombre[-4:].lower() == '.sav' or nombre[-4:].lower() == '.csv':
                print("    ", nombre)
        print("\nFicheros con macros (.mcr):")
        for nombre in contenido:
            if nombre[-4:].lower() == '.mcr':
                print("    ", nombre)

    elif type(l[0]) == str and (l[0].lower() == "d" or l[0].lower() == "del"): # Borra columnas
        print("Se van a ELIMINAR las columnas ", l[1:])
        if confirma() :
            for c in l[1:]:
                idCol = nombreColumna(df, c)
                if idCol != "":
                    df.drop([idCol], axis='columns', inplace=True)
    
    elif type(l[0]) == str and (l[0].lower() == "k" or l[0].lower() == "keep"): # Borra las columnas que no se especifican
        listaKeep = []
        for c in l[1:]:
            idCol = nombreColumna(df, c)
            if idCol != "":
                listaKeep.append(idCol)
        print("Se van a ELIMINAR las columnas que no están en la lista", listaKeep)
        ld = []
        if confirma() :
            for col in df.columns:
                if col not in listaKeep:
                    ld.append(col)
                    df.drop([col], axis='columns', inplace=True)
        print("Eliminadas columnas ", ld)
    
    elif len(l) == 3 and type(l[0]) == str and l[0].lower() == "ren" and type(l[1]) == str and type(l[2]) == str:   # renombra columna
        nombreI = nombreColumna(df, l[1])
        nombreF = nombreColumna(df, l[2])
        if nombreF != "" :
            print("ERROR, Existe una columna con el nombre final", nombreF)
        elif nombreI == "" :
            print("ERROR, No encontrada columna con nombre", nombreI)
        else :
            print("Se van a cambiar la columna", nombreI, "por", l[2])
            if confirma() :
                df.rename(columns={nombreI : l[2]}, inplace = True)
    
    elif type(l[0]) == str and l[0].lower() == "set":
        # €jemplo: "SET N,38,..,40 filtro: NACE==2.0 ORDEN: 38_a, 39_d, 40"
        print("El dataframe cambiará sus valores.")
        if confirma() :
            sl = multidivideStr(s , ["SET", "FILTRO:", "ORDEN:"])
            filtro = ""
            if sl[1] != "": # sl[1] cadena de filtro
                filtro = sl[1][8:].strip()  # "NACE==2.0"
            l = preprocesamiento(sl[0]) # ['V','N',38,39,40]
            lo = []
            if sl[2] != "":
                lo = preprocesamiento(sl[2][7:]) # ['38_a', '39_d']
            setDatosColumnas(df, l[1:], filtro, lo)
        
    elif len(l) == 3 and type(l[0]) == str and l[0].lower() == "m":
        nIni =  numColumna(df, l[1])
        ndest = numColumna(df, l[2])
        cols = list(df.columns.values)
        if nIni == ndest:
            return
        if nIni < 0:
            print("ERROR. no recononocida columna a mover.")
            return
        if ndest < 0:
            if (type(l[2]) == str and l[2].lower() == "_final_") or (type(l[2]) == int and l[2] >= len(cols)):
                ndest = len(cols)
            else:
                print("ERROR. no recononocido el destino final de la columna a mover.")
                return
        # if ndest > nIni:
        #     ndest -= 1
        etiq = cols.pop(nIni)
        if ndest >= len(cols):
            cols.append(etiq)
        else:
            cols.insert(ndest, etiq)
        df = df[cols]
        print("OK")
    
    elif type(l[0]) == str and l[0].lower() == "dropna" :   # Elimina filas que tienen datos nulos en lista de columnas indicadas
        nFilas = df.shape[0]
        lc = []
        for c in l[1:]:
            sc = nombreColumna(df, c)
            if sc != "":
                lc.append(sc)
        if len(lc) > 0:
            df.dropna(subset = lc, inplace = True)
            print("Eliminadas", (nFilas-df.shape[0]), "filas. (", round((nFilas-df.shape[0])/nFilas*100,2), "%)")
        else:
            print("Ejecución de DROPNA sin especificar columnas válidas")

    elif is2CommandFloat(l, "DROPNAF"):  # Elimina filas de columnas que menos nan tienen, hasta quitar no más del número indicado
        v = l[1]
        nReg = df.shape[0]
        # v = round(v/100*nReg)   era para introducir v en %.
        print("Se pueden eliminar hasta", v, "filas del dataFrame")
        if confirma() :
            dropnaF(df, v)
            print("DROPNA Eliminadas", nReg - df.shape[0], "filas.")

    elif is2CommandInt(l, "DROPNAC"): # Elimina columnas que tienen más de un número de nan dado.
        v = l[1]  # Expresado en %. Si v es 5, lo interpretamos como 5%.
        nCol = df.shape[1]
        print("Se pueden eliminar columnas del dataFrame")
        if confirma() :
            dropnaC(df, v)
            print("Eliminadas", nCol - df.shape[1], "columnas.")

    elif type(l[0]) == str and l[0].lower() == "new": #sólo debe aplicar a una única columna, porque damos nombre de columna destino
        # Nombre de columna de la que obtenemos los datos:
        # print("Comando NEW")
        s = s[4:].strip()
        
        colIni = numColumna(df, l[1])
        # print("Columna de la que obtenemos los datos:", colIni)
        if s.index('[') == -1 or s.index(']') == -1:
            print("No interpretado (1).")
            return
        listaValIni = preprocesamiento(s[s.index('[')+1 : s.index(']')])
        
        # print("Lista de valores a cambiar", listaValIni)
        sCols = s[:s.find("[")]
        cols = preprocesamiento(sCols) # sólo se aplicará si no hay columna de destino.
        # print("Columnas afectadas",sCols, cols)
        s = s[s.index("]")+1:].strip()
        if s[0] == "[" :    # Si no indicamos columna final, sustituirá a la columna origen
            colFin = colIni
        else :
            p = s.find("[")-1
            if p < 0 :
                print("No interpretado (3).")
                return
            colFin = s[:p].strip()
        # print("Columna destino", colFin)
        if s.index("]") < 0:
            print("No interpretado")
            return
        listaValFin = preprocesamiento(s[s.index("[")+1 : s.index("]")])
        # print("Nuevos valores:", listaValFin)
        if colIni != colFin:
            nuevaColumna(df, colIni, listaValIni, colFin, listaValFin)
            print("Generada columna", colFin)
        elif len(cols) > 0:
            n = 0
            for c in cols:
                n += nuevaColumna(df, c, listaValIni, c, listaValFin)
            print("Realizadas cambios en", len(cols), "columnas:", cols)
            
    
    elif type(l[0]) == str and l[0].lower() == "norm": # NORM P25 5 [0,1]
        limInf = limSup = None
        if s.find("[") == -1:
            limInf = 0
            limSup = 1
        else:
            try:
                slim = s[s.find("[")+1 : s.find("]")]
                lim = slim.split(",")
                if len(lim) != 2:
                    lim = s.split()
                if len(lim) != 2:
                    print("ERRROR en NORM: límites incorrectos", slim, "-->", lim)
                    return
                if es_flotante(lim[0]) and es_flotante(lim[1]):
                    limInf = float(lim[0])
                    limSup = float(lim[1])
            except:
                print("Error en NORM en lectura de límites", s)
        sCols = s[5:s.find("[")]
        cols = preprocesamiento(sCols)
        for c in cols:
            print("NORMALIZA VALORES DE COLUMNA", c, "para que sus valores estén entre", limInf, "y", limSup)
            normaliza(df, c, limInf, limSup)
        print("OK")
        
        #===== Falta CALC para construir columnas resultado de operaciones con otras columnas. =====
        #===== Desarrollé en la primera versión dropna, dropnaf, dropnac que pudieran ser interesantes.
        #================================ MODELOS MACHINE LEARNING ==============================
            
    elif l[0].lower() == 'yx' : # Se especifica la variable dependiente e independientes. YX 1,10,..,16
        if (len(l) == 1) :
            print(listaVarsYX)
            return
        l.pop(0)
        if nombreColumna(df, l[0]) == "":
            print("ERROR: No encontrada la variable dependiente", l[0])
            return
        else:
            varDepend = nombreColumna(df, l[0])
        listaVarsYX = []
        
        for ind, v in enumerate(l):
            if nombreColumna(df, v) != "":
                listaVarsYX.append(nombreColumna(df, v))
            else:
                print("Warming: No encontrada columna", v)
        l = listaVarsYX[1:].copy()
        t = "<LINEA>\n"
        t += "Valiable dependiente: " + nombreColumna(df, varDepend) + "\n"
        t += "<LINEA>\n"
        t += "Valiables independientes:" + str(listaVarsYX[1:]) + "\n"
        t += "<LINEA>\n"

        t += preAnalisis(df) + "\n"
        t += "<LINEA>\n"
        
        # x_train, x_test, y_train, y_test = train_test_split(df.drop(labels=l[n], axis=1), df.iloc[:,n], test_size=0.3, random_state=1) 
        Xdf = df.loc[:,l]
        Ydf = pd.DataFrame(df.iloc[:,numColumna(df, varDepend)])
        Xtrain, Xtest, y_train, y_test = train_test_split(Xdf, Ydf.iloc[:,0], test_size=0.3, random_state=1)
        Ytrain = y_train.to_frame(name=varDepend)
        Ytest = y_test.to_frame(name=varDepend)
        t += "Dimensión X/Y TRAIN: " + str(Xtrain.shape) + ", " + str(Ytrain.shape) + "\n"
        t += "Dimensión X/Y TEST:  " + str(Xtest.shape) + ", " + str(Ytest.shape) + "\n"
        t += "<LINEA>"
        imprimeLineasConMarco(t)
    
    elif l[0].lower() == 'cat' : # Se especifican las variables categóricas.
        if (len(l) == 1) :
            print(listaCategoricas)
            return
        l.pop(0)
        listaCategoricas = []
        for c in l:
            sc = nombreColumna(df, c)
            if sc != "":
                listaCategoricas.append(sc)
        print(listaCategoricas)
    
    elif is2CommandStr(l, "MERGE"):
        # Añade al DF actual las columnas de otro dataframe, especificado por el nombre del archivo, que no se encuentran en el dataframe actual.
        # Los dos dataframes deben tener el mismo número de filas, deben provenir del mismo dataframe (no se deben haber reordenado las filas).
        # Ejemplo addDF otroDF.csv
        df2 = abreDataFrameCSV(pd, l[1])
        if  df2 is None :
            print("ERROR: No se ha podido leer", l[1])
            return
        if df.shape[0] != df2.shape[0] : 
            print("ERROR: No coincide el número de filas de los dataframes")
            return
        l = [x for x in df2.columns if x not in df.columns]
        for x in l:
            df[x] = df2[x]
        print ("OK")
        
    elif is1Command(l, "Tonto") :
        model = modeloMax()
        imprimeLineasConMarco(analisisModelo(model))
    
    elif is2CommandInt(l, "TREE") :
        # https://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html#sphx-glr-auto-examples-tree-plot-unveil-tree-structure-py
        # https://www.aprendemachinelearning.com/sets-de-entrenamiento-test-validacion-cruzada/
        s = "<LINEA>\nclass sklearn.tree.DecisionTreeClassifier ( * ,\n"
        s += "criterion='gini',              ['gini' | 'entrppy'],\n"
        s += "splitter='best',               [best | random]\n"
        s += "max_depth=None,                [None | int]\n"
        s += "min_samples_split=2,           [int | float]\n"
        s += "min_samples_leaf=1,            [int | float]\n"
        s += "min_weight_fraction_leaf=0.0,  [float]\n"
        s += "max_features=None,             [None | int | float | 'auto' | 'sqrt' | 'log2']\n"
        s += "random_state=None,             [None | int | RandomState instance]\n"
        s += "max_leaf_nodes=None,           [None | int] * \n"
        s += "min_impurity_decrease=0.0,     [float]\n"
        s += "class_weight=None,             [None | dict, list of dict | 'balanced']\n"
        s += "ccp_alpha=0.0)                 [float >= 0]\n<LINEA>"
        imprimeLineasConMarco(s)
        modelDT = DecisionTreeClassifier(max_leaf_nodes = l[1], random_state=1)
            # Ver https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
        imprimeLineasConMarco(analisisModelo(modelDT))
        print("\nVer representación del árbol en gráfico.")
        plt.figure(figsize=(20,8))
        tree.plot_tree(modelDT,fontsize=8) 
        plt.show()
        # import random
        # Pasar una columna a lista: l = df[<nombre_col>].tolist()
        # Desordenar una lista: random.shuffle(l)
        # reemplazar los valores de una columna: df[<nombre_col>] = ds[<nombre_col>].map(l, na_action=None) o na_action=ignore Ver https://www.delftstack.com/es/howto/python-pandas/pandas-replace-values-in-column/
        # Tal vez más sencillo en https://ajaxhispano.com/ask/barajar-permutar-un-dataframe-en-pandas-40555/

    elif is1Command(l, "RF"):
        print("\n\n    RANDOM FOREST\n")
        modelRF = RandomForestClassifier(random_state = 1)  #valores por defecto
        imprimeLineasConMarco(analisisModelo(modelRF))

    elif is1Command(l, "SVM"):
        print("Ver https://www.cienciadedatos.net/documentos/py24-svm-python.html");
        print("Puede llevar un tiempo..")
        modelSVM=svm.SVC(random_state = 1) #valores por defecto
        imprimeLineasConMarco(analisisModelo(modelSVM))
    
    elif is1Command(l, "XGB"):
        print("\n\n    XGBOOST\n")
        print("Ver https://www.themachinelearners.com/xgboost-python/")
        modelXGB=XGBClassifier() #valores por defecto
        imprimeLineasConMarco(analisisModelo(modelXGB))
        
    elif is1Command(l, "LR"):
        print("\n\n    LOGISTIC REGRESSION\n")
        print("No debe haber filas que el las columnas involucradas tengan valor nulo. De lo contrario dará error. ¿Quieres continuar?\n")
        if confirma():
            modelLR =linear_model.LogisticRegression()
            imprimeLineasConMarco(analisisModelo(modelLR))
    
    elif is1Command(l, "RL"):
        print("\n\n    LINEAR REGRESSION\n")
        print("No debe haber filas que el las columnas involucradas tengan valor nulo. De lo contrario dará error. ¿Quieres continuar?\n")
        if confirma():
            modelRL = linear_model.LinearRegression()
            imprimeLineasConMarco(analisisModelo(modelRL))


    # ALGORITMOS DE CLUSTERING: https://chadwilken.com/es/los-5-algoritmos-de-clustering-los-cient%C3%ADficos-de-datos-necesitan-saber/
    # K-Means, K-Medianas,  mean-shift, Gaussian mixture models (Mgm) (GMMs),
    elif is2CommandInt(l,"BU") : # Gerárquico Aglomerativo (bottom-up)
        print("\n\n    BOTTOM-UP (gerárquico aglomerativo)\n")
        k = max(2, l[1])
        dfBU = df[listaVarsYX]
        a_model = AgglomerativeClustering(n_clusters=k, affinity='manhattan', linkage='average').fit(dfBU)  # ... ver https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html
        s = "<LINEA>\n    BOTTOM-UP (gerárquico aglomerativo) de " + str(k) + " clusters"
        s += analisisModelo2(a_model)
        imprimeLineasConMarco(s)
            
    elif is2CommandInt(l,"K-M"):
        print("\n\n    KMEANS\n")
        k = max(2, l[1])    # nº de clusters.
        dfMeans = df[listaVarsYX].copy()
        # scaler = preprocessing.MinMaxScaler()
        # dfMeans[dfMeans.columns] = scaler.fit_transform(dfMeans[dfMeans.columns])
        km_model = KMeans(n_clusters=k).fit(dfMeans)
        s = "<LINEA>\n    Modelo KMeans " + str(k) + " clusters:\n<LINEA>\n"
        s += analisisModelo2(km_model)
        imprimeLineasConMarco(s)
    
    elif is2CommandInt(l,"KModes"):
        # Para datos categóricos.
        # https://pypi.org/project/kmodes/
        # https://stackoverflow.com/questions/42639824/python-k-modes-explanation
        print("\n\n    KMODES\n")
        k = max(2, l[1])    # nº de clusters.
        kmodes_model = KModes(n_clusters=k, init='Huang', verbose=1)
        s = "<LINEA>\n    Modelo KModes " + str(k) + " clusters:\n<LINEA>\n"
        s += analisisModelo2(kmodes_model)
        imprimeLineasConMarco(s)

    elif is2CommandInt(l,"KProt"):
        # https://medium.com/analytics-vidhya/clustering-on-mixed-data-types-in-python-7c22b3898086
        print("\n\n    KPROTOTYPES\n")
        k = max(2, l[1])    # nº de clusters.
        kproto = KPrototypes(n_clusters=k, init='Cao')
        # otro KPrototypes(n_clusters=k, init='Huang', random_state=42)
        # Otro kproto = KPrototypes(n_clusters = 4, init='Huang',n_jobs=-1,n_init=10,verbose=1) en https://www.kaggle.com/mustafasmaileyi/basic-implementation-of-kprototypes-k-prototypes
        s = "<LINEA>\n    Modelo KPrototypes " + str(k) + " clusters:\n<LINEA>\n"
        s += analisisModeloKPrototipos(kproto)
        imprimeLineasConMarco(s)
    
    elif len(l) >= 3 and l[0].upper() ==  "DB" and es_flotante(l[1]) and type(l[2]) == int:
        print("\n\n    DBScan (por densidad)\n")
        radio = float(l[1])
        n = l[2]
        dbscan_model = DBSCAN(eps=radio, min_samples=n)
        s = "<LINEA>\n   DBSCAN radio = " + str(radio) + ", num. vecinos = " + str(n) + "\n<LINEA>\n"
        s += analisisModelo2(dbscan_model)
        imprimeLineasConMarco(s)

    elif len(l) == 3 and type(l[0]) == str and l[0].upper() == "SCAN" and \
    type(l[1]) == str and (l[1].upper() == "BU" or l[1].upper() == "K-M" or l[1].upper() == "KMODES") and \
    type(l[2]) == int:
        # Hacer gráfica.
        distortions = {}
        silhouette = {}
        nClusters = l[2]
        dfmodel = df[listaVarsYX]
        s = "<LINEA>\n Resultados:\n i   silhouette"
        if l[1].upper() == "K-M" :
            s += "           Inertia"
        s += "\n"
        s = "<LINEA>\n Resultados:\n i   silhouette           Inertia\n"
        if nClusters < 2:
            nClusters = 2
        for i in range(2, nClusters+1):
            print("\n Cálculo para", i, "clusters:")
            s += str(i)
            if l[1].upper() == "K-M":
                model = KMeans(n_clusters=i).fit(dfmodel)
            elif l[1].upper() == "BU":
                model = AgglomerativeClustering(n_clusters=i, affinity='manhattan', linkage='average').fit(dfmodel)
            elif l[1].upper() == "KMODES":
                model = KModes(n_clusters=i, init='Huang', verbose=1)
            # y = model.predict(dfmodel)
            y = model.fit_predict(dfmodel)
            silhouette[i] =  silhouette_score(dfmodel, y)
            s += str(silhouette[i])
            if l[1].upper() == "K-M":
                distortions[i] = model.inertia_
                s += "   " + str(distortions[i])
                centers = model.cluster_centers_
                plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
            s += "\n"
        # Plotting the ebow graphic:
        imprimeLineasConMarco(s+"<LINEA>")
        if l[1].upper() == "K-M":
            plt.plot(list(distortions.keys()), list(distortions.values()))
            plt.xlabel("Number of cluster")
            plt.ylabel("Inertia")
            plt.show()
        plt.plot(list(silhouette.keys()), list(silhouette.values()))
        plt.xlabel("Number of cluster")
        plt.ylabel("silhouette_avg")
        plt.show()
        
    elif is1Command(l, "Grupo1") :
        analisisParticularG1()
    
    else :
        print("PROCESAR INSTRUCCIÓN CON ARGUMENTOS:", l)
        

# VER https://github.com/Roche/pyreadstat
# archivoTrabajo = "prueba.sav"
# archivoTrabajo = "20220107_MM.sav"
# archivoTrabajo = "PROYECTO_5/ZA 7735/ZA7735_v1-0-0.sav"  <-- Europea original. Ver encuesta en ZA7735_bp-1.pdf
carpeta = "../../IA_trabajo\DataFrame_G"
archivoTrabajo = "20220130_DATA.sav"
# archivoTrabajo = "20220219_DATOS.sav"  ## Definitivo

# Otros posibles valores para archivo: "C:/Users/Usuario/Documents/IA/IA_trabajo/20220107_MM.sav")

if (carpeta != "") :
    os.chdir(carpeta)
leeDatos(archivoTrabajo)
# print(listaToStr(metaToList(meta)))

terminal(ejecutaComando, promt)

# https://scikit-learn.org/stable/user_guide.html