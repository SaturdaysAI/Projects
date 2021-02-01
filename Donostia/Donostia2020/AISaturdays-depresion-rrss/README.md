![alt tag](https://github.com/serNAVARRO7/AISaturdays-depresion-rrss/blob/main/header.png)

# Proyecto final AI Saturdays Euskadi 2020

[AI Saturdays](https://www.saturdays.ai/) (o AI6) es un movimiento comunitario y global, comprometido a promover la educación en Inteligencia Artificial a través de contenido de calidad y el rigor de las mejores universidades.

En resumen, una forma de hacer que esta tecnología sea accesible para todos a través del desarrollo de proyectos con impacto social.

Este repositorio engloba el proyecto realizado durante la edición de AI Saturdays Euskadi 2020 en Donostia - San Sebastián. El proyecto se basa en un trabajo científico previo realizado por un grupo de investigadores neerlandeses y estadounidenses (accesible en abierto en el repositorio de la [Universidad de Leiden](https://openaccess.leidenuniv.nl/bitstream/handle/1887/73951/Aalbers_et_al_2018_T.pdf?sequence=1)): 

> Aalbers, G., McNally, R. J., Heeren, A., De Wit, S., & Fried, E. I. (2019). Social media and depression symptoms: A network perspective. *Journal of Experimental Psychology: General*, 148(8), 1454.
> http://dx.doi.org/10.1037/xge0000528
> 

En este estudio, los investigadores analizaron si el uso pasivo de las redes sociales (es decir, hacer *scrolling* en el *feed* de noticias o publicaciones de nuestros amigos y contactos) provoca síntomas depresivos, o viceversa. El conjunto de datos que acompaña a la publicación se puede encontrar en este repositorio del [Open Science Framework](https://osf.io/czs6y/).

El proyecto *Facemood* propone usar estos datos para desarrollar un modelo predictivo que ayude a identificar individuos en riesgo de sufrir una depresión.

Para conocer más sobre el desarrollo del proyecto, consulta nuestro [post](https://medium.com/saturdays-ai/an%C3%A1lisis-de-depresi%C3%B3n-en-redes-sociales-una-aplicaci%C3%B3n-en-bioestad%C3%ADstica-3d276738ad33) en Medium.

### Miembros del equipo

- Henry Corazza
- Daniel Alcalá
- Ana Patricia Bautista
- Sergio Hernando
- Sergio Navarro

### Planning

Durante siete semanas, el equipo trabajó en el proyecto *Facemood* siguiendo el siguiente [plan de acción colaborativo](https://docs.google.com/spreadsheets/d/18FCTqPB3jZHNGhPPGIMsuiDSaqBj1YsWza4AiPS8J2w/edit?usp=sharing).

### Directorio
>
    .
    ├── docs/              # Documentos, imágenes, y presentaciones de diapositivas usadas durante el desarrollo del proyecto.
    ├── figures/           # Versión final de las figuras creadas.
    ├── processed-data/    # Conjunto de datos utilizado para la construcción del modelo tal y como resulta del proceso de análisis exploratorio de los datos.
    ├── raw-data/          # Copia del conjunto de datos tal y como fue obtenido de la fuente original (ver arriba).
    ├── scripts/           # Conjuntos de código utilizados para las distintas fases del proyecto: análisis exploratorio de los datos, clustering, ANOVA de medidas repetidas y regresión, así como funciones básicas.
    ├── datapackage.json   # Archivo JSON con la meta-información del conjunto de datos original.
    ├── LICENSE
    └── README.md
