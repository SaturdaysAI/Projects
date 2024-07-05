# 🍏 SmartBite

[Don't understand Spanish? Read it in English instead](README-en.md)

SmartBite es una herramienta de IA que identifica platos de comida en fotos, proporcionando detalles sobre ingredientes, alérgenos, macronutrientes y calorías. Mejora tu salud y bienestar con una alimentación consciente y equilibrada. 🍽️🌿

<div align="center">
    <img src="https://github.com/sergiolms/smartbite/assets/86774052/897885e8-efca-400e-a679-73b6ab3f828b" alt="SmartBite Showcase gif" />
    <br/>
    <i>Si lo prefieres, <a href="https://github.com/sergiolms/smartbite/assets/86774052/36561ee5-0d07-437d-bf9c-9ebc00980083" target="_blank">aquí</a> lo tienes en vídeo</i>
</div>

## ✨ Demo en directo ✨

Pruébalo en acción en las [GitHub Pages del repositorio][5] o en la [web de Hugging Face][6].

<!-- TODO: añadir el artículo de Medium aquí una vez se publique -->

## 🚀 El proyecto

Nace como resultado de un proyecto de fin de curso de [AI Saturdays 🤖 ALICANTE][1], con la idea de realizar una herramienta basada en inteligencia artificial que reconociera un plato de comida en una fotografía e identificara sus ingredientes, alérgenos, macronutrientes y calorías (aproximación en porción/gramos) para ese plato.

### 👥 Impacto social
Podría contribuir a mejorar la salud y el bienestar de las personas. Al ayudarles a ser conscientes de lo que comen, puede ayudar a prevenir enfermedades relacionadas con la obesidad y la diabetes. Además, se busca promover una alimentación equilibrada y sostenible, informando sobre la importancia de una nutrición adecuada.


### 🧑🏻‍🍳 Autores

<table align="center" style="font-size:14px">
    <tbody>
        <tr>
            <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
                <a href="https://github.com/sergiolms">
                    <img src="https://avatars.githubusercontent.com/u/86774052?v=4" width="100" height="auto" alt="Sergio L. Maciá Sempere"/>
                    <br />
                    <sub><b>Sergio Maciá</b></sub>
                </a>
            </td>
            <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
                <a href="https://github.com/Javier-Macia">
                    <img src="https://avatars.githubusercontent.com/u/72144607?v=4" width="100" height="auto" alt="Javier Maciá Sempere"/>
                    <br />
                    <sub><b>Javier Maciá</b></sub>
                </a>
            </td>
            <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
                <a href="https://github.com/adl23-ua">
                    <img src="https://avatars.githubusercontent.com/u/123936715?v=4" width="100" height="auto" alt="Antonio Díaz-Parreño Lajara"/>
                    <br />
                    <sub><b>Antonio Díaz-Parreño</b></sub>
                </a>
            </td>
        </tr>
    </tbody>
</table>

## 🧠 Sobre el modelo

- Ha sido entrenado utilizando de base el modelo InceptionV3 de la librería de Keras de Tensorflow.
- Actualmente, el modelo tiene un ratio aproximado de acierto del 84%, y una pérdida de 0.9252.
- Dentro de la carpeta `model` se puede encontrar un [documento más detallado](model/README.md) sobre la evaluación del modelo (scoring).
- Ha sido entrenado con 101 platos que pueden verse [aquí](datasource/meta/labels.txt).

## 🌿 Cómo empezar

En la carpeta [`gogle-collab`](google-collab) puedes encontrar un par de Notebooks para entrenar y utilizar el modelo para hacer predicciones. En los cuadernos, encontrarás el código dividido en bloques y explicado paso a paso.

Si por el contrario prefieres ejecutarlo en tu máquina, sigue las instrucciones del apartado [Requerimientos](#️-requerimientos).

### ⚙️ Requerimientos

Si ejecutas los cuadernos de Google Collab, no es necesario que hagas ninguna instalación en tu máquina. 
Tienes instrucciones sobre las dependencias del proyecto en el propio cuaderno.

Si decides descargarte el proyecto y ejecutarlo en tu máquina, necesitarás:
- Python, para ejecutar los scripts. 
    - Para el desarrollo fue utilizado Python v3.12.3. Puedes instalarlo [aquí][2]
- Tensorflow v2.16.1, para ejecutar el modelo.
- [Gradio][3], para generar una interfaz web desde donde cargar las imágenes.
- [Git LFS][4], dado que el modelo pesa más de 100MB, es necesario para manejar archivos grandes en git.

## 🏋🏻‍♂️ Entrena el modelo

Si deseas entrenar o afinar el modelo utilizando la misma configuración del proyecto, en la carpeta [`scripts`](scripts) tienes los scripts de Python que han sido utilizados tanto para entrenar el modelo como para usarlo para hacer predicciones.

## ☝️🤓 Dataset

El dataset que se ha utilizado se llama Food101. Tienes más información en [`datasource/images`](datasource/images/README.md)

[1]:https://saturdays.ai/alicante/
[2]:https://www.python.org/downloads/release/python-3123/
[3]:https://github.com/gradio-app/gradio
[4]:https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage
[5]:https://sergiolms.github.io/smartbite/
[6]:https://huggingface.co/spaces/sergiolms/smartbite
