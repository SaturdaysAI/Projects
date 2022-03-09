![alt img](https://github.com/desertificacion-AI/desertificacion-AI/blob/main/desertIArag%C3%B3n.png)

## Predicción de zonas de desertificación en Aragón usando IA. 
## Una aproximación.
Este proyecto hace parte de la iniciativa Saturdays AI en su 1a. edición, en la ciudad de Zaragoza, donde se busca que la Inteligencia Artificial (IA) sea accesible a cualquier persona a través de la creación de comunidades y formación en machine learning realizando proyectos con impacto.

Nuestra idea es explorar una aproximación a la predicción de zonas de desertificación en Aragón usando las estrategias y metodologías de IA. Exploramos a su vez la obtención de imágenes satelitales y su correspondiente tratamiento para posteriores usos adicionales.
## 

### Dataset
Ya que se hará un análisis sobre cambios en la superficie terrestre, la desertificación, utilizamos los productos del instrumento Sentinel 2A. Usando  la librería de Python SentinelSat para la descarga automática de imágenes en el área que nos interesa.
Metodología de desarrollo

Hemos tomado 12 imágenes descargadas de forma automática para el instrumento Sentinel 2A. Se ha calculado sobre cada una de ellas el NDVI y se ha obtenido una imagen resultante con extensión .tif. 

### Modelado de datos 
Para establecer una relación entre los valores medidos NDVI y cómo estos cambian en el tiempo (nuestra variable continua) para anticipar una conjunto de nuevos valores, construiremos  un modelo que nos permita predecir los valores de una variable a partir de los valores de la otra. Se ha elegido Random Forest Regressor
Una vez obtenemos las imágenes NDVI se han tomado 5 imágenes de ellas para entrenar al algoritmo y 5 para probarlo. Es de aclarar que se ha tenido que recurrir a la toma de subsets de una dimensión reducida para evitar saturación en el procesamiento de datos con las máquinas disponibles.

### A futuro
La aplicabilidad de esta aproximación puede encaminarse hacia:
- Cultivos y mejoramiento de zonas agrícolas
- Zonas de pastoreo
- Variación climática y relacion con la vegetación
- Procesamiento y enriquecimiento del algoritmo con ayuda de las tecnologías en la Nube y el procesamiento paralelo o distribuído.

### Tecnología Involucrada
- Python
- Sentinelsat
- Matplotlib
- Pandas
- rasterio
- osgeo
- sklearn
- Pillow
- Streamlit

### DEMO
[Demo en Streamlit](https://github.com/desertificacion-AI/desertificacion-AI-Streamlit)

## 

### Participantes
- [Eva de Miguel Morales](https://www.linkedin.com/in/eva-de-miguel-morales-a63938a0/)
- [Pedro Biel](https://www.linkedin.com/in/pedrobiel/)
- [Yineth Castiblanco Rojas](https://www.linkedin.com/in/yinethcastiblancorojas/)
