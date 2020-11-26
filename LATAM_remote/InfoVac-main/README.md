<p align="center">
  <img src="https://raw.githubusercontent.com/christianvadillo/InfoVac/main/reports/figures/logo_infovac.png" />

<p align="center">
============================================================================
</p>

<a href="https://www.saturdays.ai/" rel="Saturdays.ai">![saturdays](https://www.saturdays.ai/images/logo.png)</a>

<a href="https://www.linkedin.com/school/saturdaysai/" rel="link.Saturdays.ai">![linkedin](https://img.flaticon.com/icons/png/512/174/174857.png?size=48x48f&pad=10,10,10,10&ext=png&bg=FFFFFFFF)</a>
<a href="https://www.facebook.com/AISaturdaysEsp/" rel="face.Saturdays.ai">![Facebook](https://www.eyesteelfilm.com/wp-content/uploads/2017/02/facebook-icon-preview-1-45x45.png)</a>



Proyecto final para [Saturdays AI](https://www.saturdays.ai/) edición [LATAM](https://www.saturdays.ai/edicion-latam.html)


Equipo: Turquesa

Mentor: [Edwin Jiménez Lepe / Data Engineer](https://www.linkedin.com/in/edwinjimenezlepe)

1. Miembros del equipo 
    - [Irene Velasco Rocha / Project manager - Líder de equipo](https://www.linkedin.com/in/irene041204) 
    - [Christian J. Vadillo Mejía / ML Engineer](https://www.linkedin.com/in/christian-vadillo)
    - [Alejandro Tapia / Web Developer/BI- Líder de equipo (respaldo)](https://www.linkedin.com/in/atapiabueno/)
    - [Esteban Molina Saez / Developer](https://www.linkedin.com/in/estebanmolinasaez)
    - [Antonio Calzadilla Miranda /  Business Analyst](https://www.linkedin.com/in/antonio-calzadilla-miranda-8a86747b/)
    
3. Nombre detallado del proyecto 
    - Plataforma web de detección de noticias e información confiables relacionadas a la pandemia de COVID-19 en habla hispana
    
4. Nombre corto o comercial del proyecto 
   - InfoVac.IA
    
5. Eje rector o impacto social
   - SALUD
    
6. Alineación o impacto hacia objetivos de desarrollo sostenible
   -  Salud y Bienestar 

7. Descripción del problema específico
   - Se pueden detectar más de 3 mil millones de mensajes y más de 100 mil millones de publicaciones que utilizan #covid19, #coronavirus y otras etiquetas similares
“Infodemia” es un término acuñado por la Organización Mundial de la Salud (OMS) en el pasado mes de mayo para describir la propagación de la desinformación sobre el virus que hace difícil que la gente encuentre recursos fiables para obtener noticias claras por los medios de comunicación tradicionales, ya que el público se encuentra con material relacionado con el coronavirus en las redes sociales.
Encuestas en Estados Unidos, Brasil y México muestran que aproximadamente la mitad de los adultos están estresados por la emergencia sanitaria. Esto ha incrementado el consumo de drogas y alcohol, lo cual “puede exacerbar los problemas de salud mental” (REUTERS)

8. Hipótesis
    - Es posible que por medio de una plataforma web conectada a un sistema de aprendizaje automático los millennials de habla hispana puedan diferenciar una noticia falsa o información de baja confiabilidad de una noticia o información real, todo lo anterior en el contexto de noticias referentes a la pandemia de COVID-19 que se está desarrollando actualmente. 


# Docker Container 

A one paragraph description about the container.

### Prerequisities


In order to run this container you'll need docker installed.

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)

### Usage

#### clone the repository
```shell
git clone https://github.com/christianvadillo/InfoVac/
```
#### Compile the Dockerfile
```shell
docker build -t infovac-app .
```

#### Run the docker with the server
```shell
docker run -p 8001:8001 infovac-app
```

Estructura del proyecto
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── app
    │   ├── main.py       <- Main application that contains the FastAPI server that is used in the Docker container.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │   └── train          <- Splits used in the training step.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
