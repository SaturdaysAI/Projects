import gensim.downloader
import numpy as np

GloveModel = gensim.downloader.load('glove-twitter-50')

# Función para obtener/calcular el vector de representación para cada tweet
def get_w2v_vectors(processed_text, model = GloveModel):
    # Guardamos el vocabulario del modelo Word2Vec en un objeto
    words = model.index_to_key

    # Guardamos el tamaño de los vectores creados por el modelo en un objeto
    size = model.vector_size

    # Iteramos sobre los tokens del tweet para obtener su vector en el modelo
    text_vectors = []  # Lista vacía para poder guardar los vectores calculados

    for token in processed_text:
        if token in words:
            text_vectors.append(model[token])  # Si el token existe dentro del vocabulario, añadimos el valor de su vector

        else:
            text_vectors.append(np.zeros(size))  # En caso de no existir, creamos un vector del mismo tamaño que sea todo 0's

    # Calculamos la media de todos los vectores de un tweet para poder crear una representación de todo el tweet
    text_vectors_avg = np.mean(text_vectors, axis=0)

    return text_vectors_avg
