![RolEmpatIA](https://github.com/Sarya92/RolEmpatIA/blob/4f9992647b46b1726e6f19912237e239c3c8f476/8.jpeg)

# RolEmpatIA 

## Descripción del Proyecto
En una sociedad cada vez más individualizada, la creación de vínculos reales y significativos puede ser un desafío. El objetivo de RolEmpatIA es ofrecer un entorno seguro donde los usuarios puedan experimentar y practicar diferentes estilos de socialización sin el temor al fracaso o las consecuencias negativas. Nuestro chatbot, diseñado para interactuar de manera natural y empática, ofrece una forma divertida y educativa de mejorar las interacciones sociales a través de juegos de rol.

## Herramientas 
Desde el equipo trabajamos con diversas plataformas, desde UiPath para WebScarp a Colab, Jupyter Notebook o Visual Studio Code para programar. Es por ello importante aclarar que para instalar las dependencias en VSC utilizamos Poetry. 

## Dataset
En este caso, el data set es creado. No encontramos dataset en español que cumplieran los requisitos que necesitábamos. Procedimos a realizar WebScraping en foros de rol donde había partidas terminadas, pero al ser creada por los usuarios sin tener un patron claro, tras comenzar el WebScraping con Uipath, Scrapy o BeautifulSoup, finalmente completamos el dataset de forma manual, extrayendo nosotras mismas el dataset de dichos foros. Es por ello que no es tan extenso como nos gustaría. Además, decidimos hacer una selección de qué partidas utilizar, ya que había muchas +18, +21 o algunas con un claro componente folklórico como "Poseidos en Vallekas" que utilizaba personajes históricos del imaginario español como Antonio Resines, Bertín Osborne o el Rey Emérito Juan Carlos de Borbón. 

## Preprocesamiento de datos 

Lo primero que debíamos completar era la limpieza de los datos. El dataset se compone de tres columnas: Personaje - Hora del Mensaje - Texto. Para organizarnos a la hora de crear el dataset venía perfecto, pero debíamos limpiar la columna que nos interesaba, "Texto", para poder empezar a utilizarla.  

```python
nltk.download("stopwords")
    # Convertimos el contenido de la comuna texto en string
data["Texto"] = data["Texto"].astype(str)

    # Preprocesamiento de texto
data["texto_limpio"] = data["Texto"].str.lower()  # Convertimos a minúsculas
data["texto_limpio"] = data["texto_limpio"].apply(unidecode)  # Eliminamos acentos
data["texto_limpio"] = data["texto_limpio"].apply(lambda x: re.sub(r"\d+", " ", x))  # Eliminamos números
data["texto_limpio"] = data["texto_limpio"].str.translate(
    str.maketrans(string.punctuation, " " * len(string.punctuation))
)  # Eliminamos signos de puntuación
data["texto_limpio"] = data["texto_limpio"].str.replace(r"\s{2,}", " ", regex=True).str.strip()  # Eliminamos espacios innecesarios
    # Palabras a eliminar adicionales
stop = stopwords.words("spanish") + palabras_a_eliminar
data["texto_limpio"] = data["texto_limpio"].apply(
    lambda x: " ".join([word for word in x.split() if word not in (stop)])
)  # Eliminamos las stopwords
``` 
Más tarde vimos, por las características de las partidas de Rol, quedebíamos eliminar algunas palabras extras: 

```python
palabras_a_eliminar = ['mas', 'si', 'tan', 'habia', 'asi', 'oh', 'vez', 'y', 'h', 'mismo', 'aunque', 'mientras',
                       'que', 'aun', 'seras', 'cualquier', 'misma', 'mmpppfff', 'rurik', 'jum', 'wilfrick', 'jeet',
                       'julgram', 'thrommel', 'beran', 'dennek', 'caranthir', 'groak', 'jimblecap', 'gulgram', 'orsik',
                       'soren', 'ay', 'grit', 'tambien', 'groac']

```

## Tokenización y Vectorización

Para poder utilizar el contenido de la nueva columna llamada 'texto_limpio', realizamos una tokenización palabra por palabra y creamos un modelo word2vec para vectorizar las mismas. Lo aplicamos a la lista creada con las palabras y verificamos si funciona a través de la propiedad del modelo most_similar: 

```python
similar_words_magia = rol2vec.wv.most_similar("magia")
print("Palabras similares a 'magia':", similar_words_magia)

```
_Palabras similares a 'magia': [('continuo', 0.5517002940177917), ('grabo', 0.46825912594795227), ('lado', 0.46211525797843933), ('disculpad', 0.42598873376846313), ('forma', 0.41744449734687805), ('cautivo', 0.4152204692363739), ('ocurriros', 0.41037052869796753), ('sintieron', 0.4026062786579132), ('jugar', 0.40196770429611206), ('guardias', 0.3986649513244629)]_

```python
similar_words_disciplina = rol2vec.wv.most_similar("disciplina")
print("Palabras similares a 'disciplina':", similar_words_disciplina)

```
_Palabras similares a 'disciplina': [('recuerdos', 0.5104620456695557), ('creo', 0.4909777045249939), ('horda', 0.4846702516078949), ('marcho', 0.451127290725708), ('asientos', 0.38866427540779114), ('embargo', 0.38759520649909973), ('rebosa', 0.3807078003883362), ('detente', 0.37873977422714233), ('pilares', 0.3767443001270294), ('sorprendente', 0.37432533502578735)]_
```python
similar_words_dano = rol2vec.wv.most_similar("dano")
print("Palabras similares a 'dano':", similar_words_dano)

```
_Palabras similares a 'dano': [('cercenemos', 0.46414145827293396), ('pequeno', 0.4534483850002289), ('desalmados', 0.43120548129081726), ('cazadores', 0.4102203845977783), ('pretencioso', 0.40368127822875977), ('caso', 0.3865625858306885), ('requieren', 0.385661780834198), ('vas', 0.3841119706630707), ('sali', 0.3817184567451477), ('ventrue', 0.3800927400588989)]_

Como podemos ver, la vectorización tiene una visión lógica dado el tamaño del dataset. Una vez verificado esot vamos con la clusterización para organizar los datos en diferentes categorías.

## Clusterización

Configuramos y aplicamos HDBScan y generamos unos datos ficticios para comprobar que funciona correctamente con _make_blobs_ para realizar la prueba de clusterización. 

Utilizamos esta muestra para aplicarlos a los datos y trabajamos con ello. 

## Análisis de Sentimientos y Análisis de Temas/Roles

Por último decidimos utilizar TextBlob con la finalidad de hacer agrupaciones, apoyados con HDBScan y con todo lo aprendido, para añadir un perfil Psicológico ajustado a los factores DISC, pudiedon así identificar las palabras más comunes, el sentimiento promedio y los temas/roles identificados.
```python
def sentiment_analysis(texts):
    sentiments = [TextBlob(text).sentiment.polarity for text in texts]
    average_sentiment = sum(sentiments) / len(sentiments)
    return average_sentiment

def topic_analysis(texts):
    disc_keywords = {
        'D': ['combate', 'liderazgo', 'desafío', 'estrategia', 'competencia'],
        'I': ['diálogo', 'colaboración', 'amistad', 'negociación', 'influencia'],
        'S': ['aventura', 'camaradería', 'tradición', 'familia', 'hogar'],
        'C': ['estrategia', 'misión', 'disciplina', 'objetivos', 'responsabilidad']
    }
    
    temas_comunes = [keyword for keywords in disc_keywords.values() for keyword in keywords]
    
    temas_encontrados = {}
    
    for tema in temas_comunes:
        temas_encontrados[tema] = sum(text.lower().count(tema) for text in texts)
    
    return temas_encontrados

```
Con ello, realizamos análisis de los diferentes clusters generados, como podemos ver en el archivo ANALISIS_CLUSTERS_PRE_EMBEDDINGS

## Testing (TestRol)

Como pequeñas pruebas, decidimos ir preparando el camino para poder implementar el chatbot en próximas iteraciones. Para ello, realizamos una estructura de análisis según embeddings, con una serie de definiciones para cada elemento DISC como los siguientes: 
_("Me siento motivado por nuevas experiencias", "Influyente"),
    ("Me gusta estar rodeado de personas", "Influyente"),
    ("Disfruto de la tranquilidad y la paz", "Estable"),
    ("Prefiero mantener un ambiente predecible", "Estable"),
    ("Me gusta resolver conflictos de manera justa", "Dominante"),
    ("Me enfoco en hacer las cosas correctamente", "Dominante"),
    ("Siempre busco mejorar mis habilidades", "Dominante"),
    ("Valoro el cumplimiento de las normas", "Concienzudo"),
    ("Disfruto aprendiendo cosas nuevas", "Concienzudo")_

También utilizamos un modelo Doc2Vec 

Proyecto realizado por: 

- * Iván Bueno Ferreyra.
- * Víctor Moreno García.
- * Sara Poderoso Serrano.
- * Gemma Rodríguez Martínez.

Para Saturdays.IA Madrid en la edición 2024


