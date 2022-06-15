# GreenSaturdaysAI
Repositorio para proyecto de Saturdays AI.

# Estructura de carpetas
`Datasets` contiene todos los datasets que utilizamos para el proyecto.
Se organiza en subcarpetas:

- `maps` contiene los [mapas de immisión](https://opendata-ajuntament.barcelona.cat/data/es/dataset/mapes-immissio-qualitat-aire), divididos por año (ej: `2019`).
- `estaciones` contiene las [listas de estaciones](https://opendata-ajuntament.barcelona.cat/data/dataset/4dff88b1-151b-48db-91c2-45007cd5d07a/resource/3b2c1f22-2a64-40a7-9154-3d0258d847ed/download/2021_qualitat_aire_estacions.csv) por año (2021 y 2018)
- `medidas` contiene los [contaminantes medidos por estación](https://opendata-ajuntament.barcelona.cat/data/es/dataset/contaminants-estacions-mesura-qualitat-aire).
- `meta` tiene los detalles de [calidad del aire](https://opendata-ajuntament.barcelona.cat/data/es/dataset/qualitat-aire-detall-bcn)

`temp` incluye archivos intermedios y temporales

`src` incluye los scripts qye vamos usando.

`viz` es donde van los gráficos que se vayan utilizando

`docs` incluye enlaces a recursos

# Bases de datos de target de predicción:
https://opendata-ajuntament.barcelona.cat/data/es/dataset/culturailleure-parcsjardins

# Consejos:
- Modelar festivos y fines de semana 
- Manifestaciones
- Densidad de población
- Añadir Variable confinamiento 

## Licencia
Todos los datos están compartidos bajo [licencia CC 4.0](https://creativecommons.org/licenses/by/4.0/)


