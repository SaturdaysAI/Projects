###
#
# Funciones relativas al stemmer de palabras y del vocabulario en csv
#
###

import pandas as pd
import prg_globales as glb
import prg_auxiliares as aux

#
# Quita las stopwords del <vocabulario_pd>
# Atención: usar antes del stemmer, aún no existe en este punto la columna 'Stemmed'
#
def quita_stopwords(vocabulario_pd):
    vocabulario_sin_stopwords = glb.pd.DataFrame(columns=['Palabra','Sentimiento','Valoracion'])
    linea = pd.DataFrame(columns=['Palabra','Sentimiento','Valoracion'])
    for i in range(len(vocabulario_pd)): 
        item = vocabulario_pd.loc[i,"Palabra"]
        if item not in glb.spanish_stopwords or (item in glb.stopwords_permitidas):
            linea = {'Palabra':vocabulario_pd.loc[i,"Palabra"], 
                     'Sentimiento':vocabulario_pd.loc[i,"Sentimiento"], 'Valoracion':vocabulario_pd.loc[i,"Valoracion"]}
            vocabulario_sin_stopwords = vocabulario_sin_stopwords.append(linea, ignore_index=True)
    aux.debug_pd("QUITA STOPWORDS", vocabulario_sin_stopwords, 25)
    return vocabulario_sin_stopwords

#
# Esta función devuelve un dataframe con el vocabulario inicial, eliminando las raíces repetidas 
# Basado en el stemmer de español
#

#
# Aplica el stem a una sola <palabra_original>
#
def stem_palabra(palabra_original):
    palabra_revisada = aux.elimina_signos_puntuacion(glb.stemmer.stem(palabra_original))
    return palabra_revisada

#
# Aplica el stemmer al <vocabulario_pd> dado
#
def stem_vocabulario(vocabulario_pd):
    # Obtiene la columna stemmed y la coloca en la columna <Stemmed>
    vocabulario_stemmed = pd.DataFrame(columns=['Palabra','Sentimiento','Valoracion', 'Stemmed'])
    linea = pd.DataFrame(columns=['Palabra','Sentimiento','Valoracion', 'Stemmed'], index=['Palabra', 'Stemmed'])
    for num_fila in range(len(vocabulario_pd)): 
        palabra_revisada = stem_palabra(vocabulario_pd.loc[num_fila,"Palabra"])
        linea = {'Palabra':vocabulario_pd.loc[num_fila,"Palabra"], 
                 'Sentimiento':vocabulario_pd.loc[num_fila,"Sentimiento"], 'Valoracion':vocabulario_pd.loc[num_fila,"Valoracion"], 
                 'Stemmed':palabra_revisada}
        vocabulario_stemmed = vocabulario_stemmed.append(linea, ignore_index=True)
        print (".", end="")
        if (num_fila % 100) == 0:
            print (num_fila, end="")

    # Quita los posibles duplicados resultantes del stem
    vocabulario_stemmed = vocabulario_stemmed.drop_duplicates(subset=['Sentimiento', 'Valoracion', 'Stemmed'], ignore_index=True)

    # Comprueba si hay varios valores contradictorios en palabras tras el stemmer
    for num_fila in range(len(vocabulario_stemmed)): 
        palabra_revisada = vocabulario_pd.loc[num_fila,"Palabra"]
        palabras_encontradas = vocabulario_stemmed[vocabulario_stemmed.Palabra == palabra_revisada]
        cantidad_encontradas = len(palabras_encontradas)
        if cantidad_encontradas > 1 :
            print ("SV01 Error, " + str(cantidad_encontradas) + " valores para: " + palabra_revisada)

    return vocabulario_stemmed