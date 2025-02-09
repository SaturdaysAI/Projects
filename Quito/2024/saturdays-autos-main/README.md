# Predicción de Tarifas de Taxis con Machine Learning

Este proyecto utiliza machine learning para predecir las tarifas de taxis en Nueva York. El modelo se entrena con un conjunto de datos de taxis de Nueva York y se despliega como una aplicación web utilizando Flask.

## Contenido

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Ejemplo de Solicitud](#ejemplo-de-solicitud)
- [Créditos](#créditos)

## Requisitos

Asegúrate de tener instalado Python 3.8 o superior. También necesitarás instalar las dependencias listadas en el archivo `requirements.txt`.

## Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio

## Uso

python train_model.py

1. Entrena el modelo (opcional):
Si deseas entrenar el modelo desde cero, puedes ejecutar el script train_model.py:

python train_model.py

2. Inicia la aplicación Flask:
python app.py


## Ejemplo de Solicitud
Puedes enviar una solicitud POST a la API para obtener una predicción de la tarifa del taxi. Aquí hay un ejemplo usando curl:

    ```bash
    curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '[{"trip_distance": 3.5, "trip_duration": 15, "PULocationID": 1, "DOLocationID": 2}]'
    ```
La respuesta será un JSON con la predicción de la tarifa:
    ```bash
    {
    "prediction": [12.34]
    }
    ```

## Créditos
Este proyecto fue creado en el curso de Saturdays AI Quito.
