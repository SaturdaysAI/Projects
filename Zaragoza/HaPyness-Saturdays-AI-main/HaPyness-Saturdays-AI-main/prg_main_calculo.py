###
#
# Bucle principal de cálculo de valoraciones
#
# En base al vocabulario (IN_FelizTriste.csv), y al fichero de tweets (IN_train.csv),
# calcula automáticamente la valoración, según las palabras del vocabulario sean tristes o felices
# 
# Genera los ficheros de salida para su análisis:
# 
# OUT_es_errores.csv: tweets en los que ha fallado la valoración
#   Ayuda a entender por qué ha fallado la valoración en cada tweet
# OUT_es_sospechosas: palabras que han aparecido en los tweets que han fallado y son sospechosas, para su estudio 
#   Las palabras incluidas en esta salida pueden mejorar los resultados, tratándolas en el vocabulario
# OUT_es: fichero de salida con los tweets valorados algorítmicamente. 
#   Si el fichero de entrada es el TASS, incluyendo una valoración humana, esta salida incluye la valoración humana y la calculada
# OUT_FelizTriste_stemmed: inclue el vocabulario y su versión stemmed.
#    Permite mejorar el vocabulario cuando hay ambigüedades en la versión stemmed, o simplemente erróneas

###
#
# Bucle principal de cálculo. 
# Cuando se desea ejecutar la versión streamlit, se ejecuta prg_main_streamlit.py
# Cuando se desea valorar tweets en base al vocabulario, se ejecuta prg_main_calculo.py
#
###

import prg_pasos as pasos
import prg_globales as glb

def principal():

    print ("*** PASO 1: Importa el csv de vocabulario ***\n")
    pasos.PASO_1_importa_vocabulario()
    print ("*** PASO 2: Prepara vocabulario ***\n")
    pasos.PASO_2_prepara_vocabulario()
    print ("*** PASO 3: Lee los tweets en csv ***\n")
    pasos.PASO_3_lee_tweets()
    print ("*** PASO 4: Valora los tweets del fichero csv***\n")
    pasos.PASO_4_valora_tweets()
    print ("*** Guarda los resultados ***\n")
    pasos.guarda_resultados()

    # Resumen
    num_errores = len(glb.errores_valoracion)
    num_tweets = glb.tweets_pd.shape[0]
    print ("\n*** RESUMEN ***\n")
    print ("Total errores: " + str(num_errores))
    print ("Total tweets: " + str(num_tweets))
    print ("Efectividad: " + str(int(100 * (1 - num_errores / num_tweets))) + "%\n")

# Cuando se ejecuta este módulo desde otro, comentar principal():
principal()