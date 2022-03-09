###
#
# Variables globales
#
###

import pandas as pd

# Si esta activo el debug imprime los textos de debug
global debug_activado
debug_activado = 0

# GLOBALES
global const_peso_tristeza
const_peso_tristeza = -1.0

global const_peso_felicidad
const_peso_felicidad = 1.0

# Camino a los ficheros IN y OUT dependiendo del entorno de desarrollo
# const_directorio_fichero = '/content/' # Para Colab
global const_directorio_fichero 
const_directorio_fichero = '' # Para VS Code

#
# Prepara la lista de stopwords españolas para usarla en cualquier momento que se necesite eliminar
#
# Tienes que descargarte las stopwords primero via nltk.download()
# Sólo la primera vez, al iniciar el entorno de Colab (la VM se borra al salir)

# Stopwords que se van a permitir
global stopwords_permitidas 
stopwords_permitidas = ('no')

# Lista de stopwords definida
global spanish_stopwords

global vocabulario_sin_stopwords

# Pandas con el vocabulario leído del csv
global vocabulario_pd_csv
vocabulario_pd_csv = pd.DataFrame()

# Pandas con el vocabulario steemed
global vocabulario_stemmed_pd

# Objeto stemmer
global stemmer

# Pandas con los tweets del csv
global tweets_pd

# Usada en el flujo de streamlit para no dejar opción a analizar el tweet hasta que se haya cargado el vocabulario
global vocabulario_preparado
vocabulario_preparado = False

# Variables para almacenar el resultado de valora_tweet()
global valoracion_calculada # Resultado del algoritmo en base al tweet y el vocabulario
valoracion_calculada = 0.0
global palabras_encontradas # Palabras encontradas en el tweet que aparecen en el diccionario, en forma de una cadena. Se usa para el fichero de salida OUT_es_errores.csv
palabras_encontradas = []
global palabras_encontradas_lista # Palabras encontradas en el tweet que aparecen en el diccionario, en forma de lista
palabras_encontradas_lista = []

# Gestión de las palabas encontradas
global palabras_encontradas_sospechosas # Palabras sospechosas porque aparecen en tweets en los que la valoración calculada y la humana son diferentes
palabras_encontradas_sospechosas = []
global palabras_encontradas_sospechosas_resumen # palabras_encontradas_sospechosas pero sin duplicados, totalizando por palabra
palabras_encontradas_sospechosas_resumen = []
global palabras_encontradas_sospechosas_resumen_pd # Versión pandas de palabras_encontradas_sospechosas_resumen
palabras_encontradas_sospechosas_resumen_pd = pd.DataFrame(columns=['Palabra_sospechosa', 'Apariciones'])