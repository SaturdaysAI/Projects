###
#
# Pasos realizados para el cálculo automático de felicidad (pasos 1 a 4)
# Para la parte interactiva de streamlit sólo se ejecutan los pasos 1 y 2
# 
# Ficheros utilizados:
#
# Entrada (añadirlo a Colab antes de ejecutar):
#   - IN_FelizTriste.csv => vovabulario previamente valorado en un excel
#   - IN_es.csv => Tweets en csv
#
# Salida
#   - OUT_FelizTriste_stemmed.csv =s contiene las raíces de "FelizTristeIN.csv", eliminado duplicadas. 
#     Si se producen errores es porque hay una misma raíz valorada con valores contradictorios
#   - OUT_es.csv => es_IN.csv pero con una columna adicional con la valoración calculada
#   - OUT_es_errores.csv => tweets en los que la valoración del corpus y la calculada son diferentes
#
###

# Nomenclatura: los comentarios con ## se pueden borrar en la versión final 

import nltk
import pandas as pd
import string

from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Fichero .py propios del proyecto
import prg_auxiliares as aux
import prg_tweets as twe
import prg_stemmer as stem
import prg_globales as glb

# Subir al raíz de Colab: FelizTristeIN.csv

#
# PASO 1: Importar el vocabulario
#
def PASO_1_importa_vocabulario():
    # Dada una lista de vocabulario, genera otra con las palabras steemed 
    # (steemed significa con sólo las raíces
    # Genera la misma tabla inicial con una columna al final, con la raíz)
    # Ejemplo: abandonado, abandonar, abandono => abandon

    glb.stemmer = SnowballStemmer('spanish')

    new_names = ['Palabra','Sentimiento','Valoracion']
    # Sin entrada csv, para debug directo, sería: vocabulario_pd_csv = (("abandonado","Triste", -1), ("abandonar","Triste", -2), ("abandono", "Triste", -1))
    glb.vocabulario_pd_csv = glb.pd.read_csv(glb.const_directorio_fichero + "IN\IN_FelizTriste.csv", names=new_names, skiprows=1, delimiter=";", encoding='latin1', index_col=False)

    aux.debug_pd ("LEE VOCABULARIO", glb.vocabulario_pd_csv.head(5), 15)
    aux.debug_pd ("PALABRAS", glb.vocabulario_pd_csv['Palabra'], 15)

#
# PASO 2: Prepara vocabulario stemmed (vocabulario_stemmed_pd)
#
def PASO_2_prepara_vocabulario():
    # Carga de las stopwords standard
    print ('*** Para cargar las stops words introducir: ***\n\nOpción d) -> stopwords -> q\n')
    nltk.download('stopwords')
    glb.spanish_stopwords = stopwords.words('spanish')
    print ('Stopwords descargadas, continúa la ejecución...')

    # Se asegura de que el vocabulario no incluye stopwords
    glb.vocabulario_sin_stopwords = stem.quita_stopwords(glb.vocabulario_pd_csv)

    #
    # Aplica el stemmer al vocabulario inicial
    # Deja sólo las raices de las palabras y elimina los acentos
    #
    glb.vocabulario_stemmed_pd = stem.stem_vocabulario(glb.vocabulario_sin_stopwords)
    print(glb.vocabulario_stemmed_pd.shape)
    print(glb.vocabulario_stemmed_pd.head(25))

#
# PASO 3: Lee los tweets del csv
#
def PASO_3_lee_tweets():
    # Lee los tweets del corpus
    new_names = ['ID','texto_tweet_original','valoracion_corpus', 'Texto_tweet']
    glb.tweets_pd = pd.read_csv(glb.const_directorio_fichero + 'IN\IN_train.csv', names=new_names, skiprows=1, delimiter=';', encoding='UTF-8') # Si no va con UTF-8 usar latin1, depende del csv

    # Añade una columna donde se dejará la valoración calculada
    glb.tweets_pd.insert(4, "valoracion_calculada", 99.0)
    print (glb.tweets_pd.head(5))
    print (glb.tweets_pd.shape)

    aux.debug_pd ("TWEETS", glb.tweets_pd['texto_tweet_original'], 25)
    glb.tweets_pd.info

#
# PASO 4: Valora tweets del csv
#
# Dada una lista de tweets, genera otra con los tweets valorados, 
# a la vez que detecta cuándo la valoración del tweet y la calculada son diferentes
# En ese caso genera un dataframe con las diferencias <errores_valoracion>
#
def PASO_4_valora_tweets():
    palabras_encontradas = []
    palabras_encontradas_lista = []
    palabras_encontradas_sospechosas = []
    # Prepara el dataframe para guardar los errores de valoración
    glb.errores_valoracion = pd.DataFrame(columns=['Texto_tweet','valoracion_corpus','valoracion_calculada', 'Palabras_encontradas'])

    # Prepara el dataframe usado para añadir líneas al dataframe de errores
    linea_error_pd = pd.DataFrame(columns=['Texto_tweet','valoracion_corpus','valoracion_calculada', 'Palabras_encontradas'])

    # Recorre todos los tweets
    for num_fila in range(len(glb.tweets_pd)): #range(0, 20) : #
    
        # Prepara el tweet limpio sin hastag etc., conservando el original para depuración
        glb.tweets_pd.loc[num_fila,"Texto_tweet"] = twe.limpia_tweet(glb.tweets_pd.loc[num_fila,"texto_tweet_original"])

        # Obtiene la valoración según el corpus y la guarda en tweets_pd
        if glb.tweets_pd.loc[num_fila,"valoracion_corpus"] == "NEU": # Depende del fichero de entrada revisar estos valores
            glb.tweets_pd.loc[num_fila,"valoracion_corpus"] = 0
        elif glb.tweets_pd.loc[num_fila,"valoracion_corpus"] == "tristeza":
            glb.tweets_pd.loc[num_fila,"valoracion_corpus"] = glb.const_peso_tristeza
        elif glb.tweets_pd.loc[num_fila,"valoracion_corpus"] == "felicidad":
            glb.tweets_pd.loc[num_fila,"valoracion_corpus"] = glb.const_peso_felicidad
        valoracion_corpus = glb.tweets_pd.loc[num_fila,"valoracion_corpus"]
        
        # Obtiene la valoración calculada
        valoracion_calculada, palabras_encontradas, palabras_encontradas_lista = twe.valora_tweet(glb.vocabulario_stemmed_pd, glb.tweets_pd.loc[num_fila, "Texto_tweet"])
        
        # Guarda el resultado en el dataframe tweets_pd
        glb.tweets_pd.loc[num_fila, "valoracion_calculada"] = valoracion_calculada
        print ("Valoración = " + str(num_fila) + "/" + str(len(glb.tweets_pd)) + ' - ' + str(valoracion_calculada) + " - Tweet = " + glb.tweets_pd.loc[num_fila, "Texto_tweet"])  

        # Registra los errores de valoración
        aux.debug_print ("Valoraciones: ", valoracion_corpus, valoracion_calculada)
        if valoracion_corpus != valoracion_calculada :
            if ((valoracion_corpus == -1 and valoracion_calculada >= 0) or (valoracion_corpus == 0 and valoracion_calculada > 0) or (valoracion_corpus == 1 and valoracion_calculada <= 0)) :
                aux.debug_print ("VTS01: " + palabras_encontradas + "\n")
                linea_error_pd = {'Texto_tweet':glb.tweets_pd.loc[num_fila, "Texto_tweet"], 
                        'valoracion_corpus':glb.tweets_pd.loc[num_fila,"valoracion_corpus"],
                        'valoracion_calculada':glb.tweets_pd.loc[num_fila,"valoracion_calculada"],
                        'Palabras_encontradas': palabras_encontradas}
                # Registra el error en el dataframe de errores 
                glb.errores_valoracion = glb.errores_valoracion.append(linea_error_pd, ignore_index=True)
                
                # Añade esa palabra a la lista de palabras sospechosas de generar diferencia entre la valoración del corpus y la calcula,
                # para su posterior análisis
                glb.palabras_encontradas_sospechosas.extend(palabras_encontradas_lista)

    # Elimina repetidos en la lista de palabras sospechosas y cuenta las apariciones
    glb.palabras_encontradas_sospechosas_resumen = Counter(aux.dime_columna(glb.palabras_encontradas_sospechosas, 0))
    # print (glb.palabras_encontradas_sospechosas_resumen)

#
# Guardado de resultados
#
def guarda_resultados():
    # Guarda el vocabulario stemmed para su revisión cuando hay repetidos que generan errores
    glb.vocabulario_stemmed_pd.to_csv(glb.const_directorio_fichero + "OUT\OUT_FelizTriste_stemmed.csv", sep=";", encoding='latin1')

    # Guarda los tweets valorados
    glb.tweets_pd.to_csv(glb.const_directorio_fichero + "OUT\OUT_es.csv", sep=";") # con encoding='latin1' da error

    # Guarda los errores de validación
    glb.errores_valoracion.to_csv(glb.const_directorio_fichero + "OUT\OUT_es_errores.csv", sep=";") # con encoding='latin1' da error
    aux.debug_pd("ERRORES VALIDACION", glb.errores_valoracion, 25)
    # print("GR01: ", glb.errores_valoracion.shape)

    # Guarda las palabras sospechosas por aparecer en los errores de validación

    # Convierte la serie a pandas para exportar a csv
    # print("GR02: ", glb.palabras_encontradas_sospechosas_resumen)
    glb.palabras_encontradas_sospechosas_resumen_pd = pd.DataFrame(pd.Series(glb.palabras_encontradas_sospechosas_resumen), columns=['Palabra_sospechosa'])
    # print("GR03: ", glb.palabras_encontradas_sospechosas_resumen_pd.shape)

    # Ordena de forma descendente, primero las  palabras sospechosas más frecuentes
    glb.palabras_encontradas_sospechosas_resumen_pd = glb.palabras_encontradas_sospechosas_resumen_pd.sort_values('Palabra_sospechosa', ascending=False)

    # Exporta a csv las palabras sospechosas
    glb.palabras_encontradas_sospechosas_resumen_pd.to_csv(glb.const_directorio_fichero + "OUT\OUT_es_sospechosas.csv", sep=";") # con encoding='latin1' da error
    aux.debug_pd("PALABRAS SOSPECHOSAS", glb.palabras_encontradas_sospechosas_resumen_pd, 25)