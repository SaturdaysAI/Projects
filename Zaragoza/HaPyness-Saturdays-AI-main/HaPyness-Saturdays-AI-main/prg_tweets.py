###
#
# Funciones relativas a la limpieza, preparación y valoración automática de tweets
#
###

import re
import nltk
import string

import prg_globales as glb
import prg_auxiliares as aux
import prg_stemmer as stem

#
# LIMPIEZA DE TWEETS: elimina menciones @, retweets, #, links y TAGS
#
# La funcion limpia_tweet elimina stopwords y algunos caracteres peculiares de twitter
# 
def limpia_tweet(text):
  text = str(text)
  text = re.sub(r'@[A-Za-z0-9]+', ' ', text) #Remover menciones @
  text = re.sub(r'RT[|\s]', ' ', text) # Remover RTs
  text = re.sub(r'#', ' ', text) #Remover # en el tweet
  text = re.sub(r'https?:\/\/\S+', ' ', text) #Remover links

  #Nuevas incluidas remove links
  text = re.sub(r'http\S+', ' ', text) # remove http links
  text = re.sub(r'bit.ly/\S+', ' ', text) # remove http links
  text = re.sub(r'pic.twitter\S+', ' ', text) # remove links
  text = text.strip('[link]') # remove links

  #Remove hashtags """Takes a string and removes any hash tags"""
  text = re.sub('(#[A-Za-z]+[A-Za-z0-9-_]+)', '', text)  # remove hash tags
  text = re.sub('HASHTAG', '', text)  # remove hash tags)
  text = re.sub('USER', '', text)  # remove hash tags)

  pattern = r'''(?x)                    # set flag to allow verbose regexps
              (?:[A-Z]\.)+            # abbreviations, e.g. U.S.A
              | \w+(?:-\w+)*          # Words with optional internal hyphens
              | \$?\d+(?:\.\d+)?%?    # Currency and precentages, e.g. $12.40 82%
              | \.\.\.                # Ellipsis
              | [][.,;"'?():-_`]      #These are separate tokens; includes ],[
              '''
  words = nltk.regexp_tokenize(text, pattern)
  re_punc = re.compile('[%s]' % re.escape(string.punctuation)) # Remover signos de puntuacion
  stripped = [re_punc.sub('', w) for w in words]

  no_garbage = [w for w in stripped if (w.lower() not in glb.vocabulario_sin_stopwords)] # Remover stopwords

  return (" ".join(no_garbage))

  # df['tweets_transform'] = df['text'].apply(transform)

#
# Preparación del tweet: eliminación de signos de puntuación y limpieza de elementos típicos de un tweet
#
def prepara_tweet(texto_tweet):
    tweet_final = aux.elimina_signos_puntuacion(texto_tweet)
    tweet_final = limpia_tweet(tweet_final)
    # tweet_final = repara_acentos(tweet_final) -> no es preciso si se abre en UTF-8
    return tweet_final

def valora_tweet(vocabulario_base_pd, texto_tweet):
    if texto_tweet is not None:
        palabras_tweet = prepara_tweet(texto_tweet).split()
        # print (palabras_tweet)
        valoracion_calculada = 0.0
        contador = 1
        palabras_encontradas = ""
        palabras_encontradas_lista = []

        for palabra_buscada in palabras_tweet:
            ## Alternativo: palabra_vocabulario = vocabulario_base_pd.query('Palabra == "'+ palabra_buscada +'"')
            # Averigua si la palabra_buscada está en el vocabulario. 
            # Ambas deben tener el stem aplicado
            palabra_buscada_stemmed = stem.stem_palabra(palabra_buscada)
            # print ("valora_tweet_01:", palabra_buscada_stemmed)
            palabra_vocabulario = vocabulario_base_pd[vocabulario_base_pd.Stemmed == palabra_buscada_stemmed]

            # Evita el riesgo de que el stemmer genere una palabra que acabe siendo una raíz incluida en el vocabulario, 
            # pero el riesgo de que ocurra es muy bajo
            aux.debug_print ("VT02 "+ "Buscada: " + palabra_buscada_stemmed)
            cantidad_encontradas = len(palabra_vocabulario)
            if cantidad_encontradas > 1 :
                print ("Error, varios valores para: " + palabra_vocabulario.Palabra)

            # Si la palabra está en el vocabulario, añade su valoracion
            if not palabra_vocabulario.empty:
                valoracion = float(palabra_vocabulario.Valoracion)
                # Importante cuando no se entiende una valoración
                palabra_vocabulario.describe
                aux.debug_print ('VT03 Encontrada palabra: ' + palabra_buscada_stemmed + " - Val: " + str(valoracion))
                palabras_encontradas = palabras_encontradas + " " + palabra_buscada_stemmed + "(" + str(valoracion) + ")"
                palabras_encontradas_lista.append([palabra_buscada_stemmed, valoracion])
                # palabras_encontradas_lista.append([palabra_buscada_stemmed])
                # print ("valora_tweet_02:", palabra_buscada_stemmed, palabras_encontradas)
                aux.debug_print ('VT04 Palabras encontradas:' + palabras_encontradas)
                valoracion_calculada += valoracion
            else:
                valoracion = 0
            contador += 1
            # print('VT05 Valoración ' + str(contador) + '/' + str(len(palabras_tweet)) + ': <' + palabra_buscada + '> = ' + str(valoracion) + " - Total valoración = " + str(valoracion_total))
        
        # Normaliza los valores, si es mayor que 1 es entiende que es felicidad, igual con tristeza y <=-1
        if valoracion_calculada >= 1.0 :
            valoracion_calculada = 1.0
        elif valoracion_calculada <= -1.0 :
            valoracion_calculada = -1.0
        else : 
            valoracion_calculada = 0.0

    return valoracion_calculada, palabras_encontradas, palabras_encontradas_lista