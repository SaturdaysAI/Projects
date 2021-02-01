# Pancreas Artificial

## Participantes

En caso de duda no dudéis en contactar con alguno de nosotros.

* Juan Enrique Martinez jmartnav@gmail.com
* Pablo Aragonés López pabloaragones97@gmail.com
* Gilberto Jesús Brito gjbrito17@gmail.com

## Motivación

Siendo la diabetes una enfermedad que afecta a muchísimas personas (400 millones aprox. en el mundo) nuestra intención era realizar un enfoque que aplicase técnicas de machine learning para mejorar la calida de vida de las personas que sufren esta enfermedad.

Actualmente las personas que sufren esta enfermedad llevan una bomba de insulina y sensor de glucosa que realiza mediciones y suministra la insulina que requiere el paciente.

De estos sensores hemos obtenido nuestros datos.

## Dataset y tratamiento del dato

El dataset con el que se ha trabajado ha sido obtenido por parte de un paciente con diabetes tipo 1. Este dato era guardado en una web conectada al sensor y de ahí se extrían tres ficheros de extensión .json: entries.json, treatments.json y devices.json.

Realizando transformaciones sobre estos ficheros obtenemos finalmente nuestro dataset final en extensión .csv.

Durante la fase de preparación del dataset se incluyó la generación de nuevas variables además de limpiar el dato previamente capturado. Este proceso de limpieza consistío en reducir outliers, eliminar nulos, etc.

En este repositorio encontraréis en formato .sgv el workflow de KNIME que muestra las transformaciones realizadas sobre los .json.

![](ETL_Dataset.png?raw=true)

## Modelos probados

- Random Forest (OOB)
- Linear Regression

En este repositorio podréis encontrar el notebook de jupyter que hemos elaborado así podréis obtener más información.

## Referencias

* https://nbviewer.jupyter.org/gist/mariusae/18a62db9cc32d09dc691fd4f78dcdbfa
* openaps.org


