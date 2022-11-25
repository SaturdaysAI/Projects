
![Logo](https://avatars.githubusercontent.com/u/115894149?s=200&v=4)


# VAK.AI

El proyecto consiste en desarrollar una herramienta que recurra a algoritmos de Machie Learning (ML) 
para detectar los tipos de aprendizaje.

Está basado en el modelo VAK que se divide en tres categorias:\
    * Visual\
    * Auditivo\
    * Kinestésico

La Encuesta utilizada está basada en 40 preguntas.\
[ESTILOS DE APRENDIZAJES (PNL)](https://docs.google.com/forms/d/e/1FAIpQLSd-eQAlCLuWQrmWDy4lN2MZhcwxBIaBv5JOXW6lk2d-dDe8VA/viewform)

## Tecnologías Utilizadas

[Python](https://www.python.org/)

[Jupyter Notebooks](https://www.datacamp.com/community/tutorials/tutorial-jupyter-notebook)

[Google Colab](https://colab.research.google.com/notebooks/welcome.ipynb#recent=true)


## Para usar este proyecto

Via git
```bash
  git clone https://github.com/team-verde-mx/estilosdeaprendizaje.git
```


## Modelos usados

#### Random Forest Classification
Método de aprendizaje automático supervisado, que se basa en árboles de decisión.

#### Combinación de las predicciones de Random Forest Classification
Para los problemas de clasificación, que es nuestro caso, combina los resultados de los árboles de desición usando soft-voting\
cada árbol de desición da una clasificación y al final la desición con mayor "votos" es la predicción de nuestro análisis.

```http
  RandomForestClassifier(n_jobs=2, random_state=0)
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `n_jobs` | `int`     | **default=None**. No. de trabajos a ejecutar en paralelo. None significa 1 al menos. -1 significa todos los procesadores. |
| `random_state` | `int` | **default=None**. Controla la aleatoriedad del arranque de las muestras utilizadas. |


## Autores

- [@Manuel David Morales](https://www.github.com/ManuelDMorales)
- [@Rafael Rodriguez](https://www.github.com/rafaelropa)
- [@Guillermo Alcaraz](https://www.github.com/GuillermoAAD)
- [@Perla Tovar](https://www.github.com/PerlaTovarGarcia)
- [@María Rivas](https://github.com/MaryRivasB)

