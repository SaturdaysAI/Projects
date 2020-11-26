# Extracción de datos

Este es el repositorio para la extracción de datos de **Twitter**.
Las instrucciones de ejecución están hasta el final.

---

Para llevar a cabo el análisis se recolectaron datos de tweets de 3 diferentes ciudades para poder tener muestras variadas y esperar resultados diferentes. Las ciudades fueron elegidas solamente tomando en cuenta que fueran ciudades grandes en diferentes países angloparlantes.

Las ciudades de las que se obtuvieron los datos fueron las siguientes:
- **Brisbane, Australia** (2225 tweets)
- **San Francisco, Estados Unidos** (5000 tweets)
- **Vancouver, Canadá** (1699 tweets)

Cabe mencionar que los datos fueron recolectados el 24 de Octubre y los tweets tienen fecha mínima de publicación una semana anterior a la fecha de recolección y máxima el mismo día de la recolección.

La estructura de los datos es idéntica para los 3 datasets. Cada dataset está organizado en 14 columnas y está ordenado por ‘favorites’.

Columnas del dataset:

- user_name: 		Nombre de usuario quien publica el tweet.	
- tweet_id: 		Identificador único del tweet.
- user_location: 		Ubicación aproximada del usuario (si su ubicación está activada).
- user_description: 	Biografía del usuario.
- user_created:		Fecha de creación de la cuenta del usuario.
- user_followers: 	Número de seguidores del usuario.
- retweets: 		Número de retweets del tweet.
- favorites: 		Número de favoritos del tweet.
- user_verified: 		Verdadero si el usuario es verificado.
- date: 			Fecha de publicación del tweet.
- text: 			Texto del tweet.
- source:		Fuente desde donde se publicó (app, web, hootsuite, etc.).
- is_quote_status: 	Verdadero si el tweet es una cita de otro tweet.
- is_retweet: 		Verdadero si el tweet es retweet.

Los datos se obtuvieron a través de la API de Twitter a través de un script de Python utilizando Tweepy. El código fuente es abierto y puede consultarse [aquí](https://github.com/SaturdayAI-Green/DataExtraction_Section/blob/master/RecolectorTweets.ipynb). 


# Instrucciones de ejecución

1. Generar las API Keys en [https://apps.twitter.com/](https://apps.twitter.com/)
2. Copiar las keys en un nuevo archivo llamado `.env` con los contenidos de `.env.example`
3. Correr `python ejemplo.py` o correr el notebook `RecolectorTweets.ipynb`
