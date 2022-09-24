# Smurfs en LoL

## Web scraping leagueofgraphs
### Configuración entorno ejecución
Descargar [ChromeDriver](https://chromedriver.chromium.org/downloads) para la versión instalada de chrome en nuestro equipo en la siguiente ruta:
C:\Program Files (x86)\Google

### API key de RIOT
Acordarse de modificar y cambiar el api key en el archivo config.py (caduca todos los días)


## Fichero FULL

En la carpeta extracts se deja el fichero full que contine la info de todas las partidad del soloQ challege.

Este fichero esta enriquecido con los pasos: 
* calculate_score.py: calcula un escore entre 0 y 10 en función de el número de partidas diarias y el porcentaje de juego en una misma línea.
* smurf_tagger.py: indica si una partida es smurf tomando el Elo con el que finalizó el jugador el SoloQ Challenge como su elo actual, y si el elo de la partida es dos divisiones menor o mas se marca como jugador Smurf en dicha partida.
