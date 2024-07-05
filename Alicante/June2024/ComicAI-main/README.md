# ComicAI
Sistema de Narración de Cómics para Personas con Discapacidad Visual.
El presente proyecto pretende ayudar a las personas con discapacidad visual a disfrutar del mundo del comic a través de la narración de las historias gráficas.
## Estructura y funcionalidad de los módulos
La pipeline del proyecto se realiza a través diferenes operaciones para llegar al resultado final a través de módulos inviduales en cascada:

- **1_divide_page**

Divide el archivo original .pdf (el cual puede ser un comic completo o capítulos individuales) en páginas en formato .jpeg.

En este código se utilizan varias librerías para diferentes propósitos: fitz (de PyMuPDF) se emplea para abrir y manipular documentos PDF, específicamente para extraer las imágenes de cada página; os se usa para interactuar con el sistema operativo, permitiendo la manipulación de directorios y archivos, como la creación, eliminación y listado de contenidos; shutil se utiliza para operaciones de alto nivel en archivos y colecciones de archivos, en este caso para eliminar subdirectorios; y csv se utiliza para escribir en archivos CSV, en este caso, para crear un archivo que contiene las rutas de las imágenes extraídas del PDF.

- **2_identify_panels**

Identifica cada viñeta de las páginas del paso anterior y la guarda el formato .jpeg.

En este código se utilizan varias librerías para diferentes propósitos: cv2 (OpenCV) se usa para la manipulación y procesamiento de imágenes, incluyendo la lectura, conversión a escala de grises, aplicación de desenfoque, detección de bordes y dibujo de contornos; os se emplea para interactuar con el sistema operativo, permitiendo la manipulación de directorios y archivos, como la creación, eliminación y listado de contenidos; shutil se utiliza para operaciones de alto nivel en archivos y colecciones de archivos, en este caso, para eliminar directorios y su contenido; y matplotlib.pyplot se utiliza para la visualización de imágenes con los rectángulos de las viñetas dibujados, ajustando el tamaño de la figura y mostrando la imagen procesada.

- **3_bubbles_to_text**

Indetifica el diálogo entre los personajes y el texto que aparece en la viñeta como onomatopeyas o descripciones. *Esta descripción es en español*

En este código se utilizan varias librerías para diferentes propósitos: torch (PyTorch) se usa para verificar la disponibilidad de CUDA y para manejar el dispositivo (CPU o GPU) en el que se ejecutarán los modelos de procesamiento de texto e imagen; transformers de Hugging Face se emplea para cargar los modelos preentrenados de TrOCR y su procesador, permitiendo realizar el reconocimiento óptico de caracteres en las imágenes; easyocr se utiliza para detectar y leer texto en imágenes sin necesidad de CUDA. En este caso se utiliza para el reconocimiento de las zonas donde hay texto, ya que el reconocimiento del propio texto se hace con el modelo finetuned de trOCR; cv2 (OpenCV) se usa para cargar y manipular imágenes, incluyendo el recorte y dibujo de cajas delimitadoras alrededor de las áreas de texto detectado; os se utiliza para interactuar con el sistema operativo, permitiendo la navegación por los directorios de entrada y salida, así como la creación de nuevas carpetas; matplotlib.pyplot se usa para visualizar las imágenes con las cajas delimitadoras dibujadas; y PIL (Pillow) se emplea para convertir imágenes de formato OpenCV a formato PIL para su procesamiento por los modelos de Hugging Face.

- **4_img_to_nlp**

Realiza la descripción de de lo que ocurre en la viñeta, ya sea la descripción del entorno o de los propios peronajes. *Esta descripción es en inglés*

En este código se utilizan varias librerías para diferentes propósitos: torch (PyTorch) se emplea para verificar la disponibilidad de CUDA y manejar el dispositivo (CPU o GPU) donde se ejecutarán los modelos, así como para cargar y mover el modelo afinado al dispositivo; transformers de Hugging Face se utiliza para cargar los modelos preentrenados BLIP para la generación de descripciones de imágenes y sus procesadores correspondientes, permitiendo realizar el captioning de las imágenes; os se usa para interactuar con el sistema operativo, permitiendo la navegación por los directorios de entrada y salida, así como la creación de nuevas carpetas; PIL (Pillow) se utiliza para cargar y convertir imágenes a formato RGB para su procesamiento; y matplotlib.pyplot se emplea para visualizar las imágenes junto con las descripciones generadas por los modelos.

- **5_translate**

Traduce el texto generado el paso anterior para adaptarlo al español.

En este código se utilizan varias librerías para diferentes propósitos: deep_translator se emplea para traducir texto usando la clase GoogleTranslator, permitiendo la traducción de textos de inglés a español; os se usa para interactuar con el sistema operativo, permitiendo la navegación por los directorios de entrada y salida, así como la creación de nuevas carpetas; os.path se utiliza para manipular las rutas de archivos y directorios, facilitando la construcción de rutas absolutas y relativas; y builtins se emplea para operaciones de lectura y escritura de archivos, permitiendo la manipulación del contenido de los archivos de texto que se encuentran en el directorio de entrada y la escritura de las traducciones en el directorio de salida.

- **6_tts**

Por último se narra el texto generado en los pasos 3 y 5. *En este paso también se unen ambos texto para que tengan coherencia dentro de una viñeta. Cada archivo de audio se genera individualmene para cada viñeta*

En este código se utilizan varias librerías para diferentes propósitos:
gtts: La librería gtts (Google Text-to-Speech) se usa para convertir texto a audio. Utiliza el servicio de TTS de Google para generar archivos de audio en diferentes idiomas. moviepy.editor: La librería moviepy se utiliza para manipular archivos de audio y video. En este caso, se usa para concatenar clips de audio. pathlib.Path: Proporciona una manera de trabajar con rutas de archivos y directorios de forma más intuitiva y moderna que el módulo os.path. os: La librería os se usa para interactuar con el sistema operativo, permitiendo navegar por directorios y crear carpetas si es necesario.


## Estructura de directorios
En el presente proyecto encontramos la siguiente estructura de directorios:
- data (`archivos de entrada y salida`)
    - input (`carpeta para cargar el comic`)
        - Comic_test (`carpeta donde se aloja el comic a estudiar en formato pdf. Se puede guardar cada capítulo por separado en carpetas`)
    - output (``carpetas de salida de cada proceso``)
        - divide_images_test (``imágenes derivadas de la identificación de viñetas``)
        - divide_pages_test (`imágenes derivadas separación por páginas del comic`)
            - pages_raw (`imágenes de cada página del comic`)
            - pages_routes (`archivo csv que aloja las rutas de las imágenes de la carpeta pages_raw`)
        - ouput_audio_test (`salida final de audio para cáda viñeta del comic`)
        - output_description_test (`archivos de texto donde se describe lo que aparece en cada viñeta`)
        - output_description_translate_test (`archivos de texto con la traducción de los archivos de descripción de cada viñeta`)
        - output_text_test (`archivos de texto donde se transcribe el texto que aparece en cada viñeta`)
- documentation (`documentación final del proyecto`)
    - data (`datos usados para la presentación y/o el paper`)
    - *paper.docx* (`paper del proyecto`)
    - *Presentation.pptx* (`presentación del proyecto`)
- environments (`entornos para cargar en anaconda`)
    - *SATURDAYS-2.yaml* (`entorno con todas las librerías necesarias para ejecutar el presente proyecto`)
- execution_files (`archivos de ejecución del proyecto en 2 formatos`)
    - notebooks (`notebooks de jupyter`)
        - *1_divide_page.ipynb* (`divide las páginas del comic y las guarda como imágenes`)
        - *2_identify_panels.ipynb* (`identifica cada viñeta y la guarda como imagen`)
        - *3_bubbles_to_text.ipynb* (`identifica el texto que aparece en la viñeta y lo guarda en un archivo de texto`)
        - *4_img_to_nlp.ipynb* (`identifica lo que ocurre en la imagen, hace una descripción en inglés y la guarda en un archivo de texto`)
        - *5_translate.ipynb* (`traduce los archivos del punto 4 a español y los guarda en archivos de texto`)
        - *6_tts.ipynb* (`narra los ficheros de descripción de la imagen y el texto que aparece en ella. Puntos 3 y 5`)
    - py_files (`archivos python para el pipeline`)
        - *1_divide_page.py* (`divide las páginas del comic y las guarda como imágenes`)
        - *2_identify_panels.py* (`identifica cada viñeta y la guarda como imagen`)
        - *3_bubbles_to_text.py* (`identifica el texto que aparece en la viñeta y lo guarda en un archivo de texto`)
        - *4_img_to_nlp.py* (`identifica lo que ocurre en la imagen, hace una descripción en inglés y la guarda en un archivo de texto`)
        - *5_translate.py* (`traduce los archivos del punto 4 a español y los guarda en archivos de texto`)
        - *6_tts.py* (`narra los ficheros de descripción de la imagen y el texto que aparece en ella. Puntos 3 y 5`)
        - *packages.py* (`bibliotecas necesarias`)
- train (`archivos para el entramiento del proceso de finetuning de los modelos de descripción de la imagen y texto en la imagen`)
    - data (`archivos de entrada y salida`)
        - input (`archivos de entrada en raw`)
            - Comic_train (`imágenes de cada página`)
            - imagenes_prueba (`imágenes aleatorias`)
        - output (`archivos procesados del comic`)
            - divide_images_train (`imágenes de cada viñeta de la páginas de input/Comic_train`)
    - models (`modelo finetuneados de trOCR`)
        - modelo_finetuneado_trOCR
        - procesador_finetuneado_trOCR
    - results (`modelo finetuneados de BLIP`)
    - *1_identify_padels_for_finetuning.ipynb* (`proceso para dividir las páginas del training en viñetas`)
    - *2_bubbles_to_text_finetuning.ipynb* (`proceso para realizar el finetuning de trOCR`)
    - *3_img_to_nlp_finetuning.ipynb* (`proceso para realizar el finetuning de BLIP`)
- *.gitignore* (`gitignore`)
- *comic_AI.py* (`pipeline para la ejecución de los archivos de exeution_files/py_files en cadena`)
- *README.md* (`el presente archivo`)


## Ejecución del proceso completo
En este apartado se describe cómo ejecutar el proceso completo para pasar de un cómic en .pdf a los archivos finales de audio que describen cada viñeta:

**1. Carga de ficheros**

El proceso funciona desde la carga de un cómic en el directorio ``/data/input/Comic_test``. Dentro de esta carpeta se puede cargar un fichero individual en .pdf o crear un subdirectorio de carpeta en el que cada carpeta sea un capítulo y dentro de esta cargar cada capítulo en formato .pdf.

*En el caso de cargar un único fichero el sistema no es capaz de reconocer la división por capítulo para crear los subdirectorios oportunos.*

**2. Ejecución de la pipeline**

La ejecución del proceso completo se hace ejecutando el archivo comic_AI.py del directorio raiz. Este no necesita la introducción de parámetros. *Previo a este paso será necesario instalar todas las librerías necearias o cargar el entorno de anaconda que se encuentra en el directorio ``/environments``. El terminal de ejecución debe ejecutarse en ese entorno proporcionado. También será necesario decargar los modelo de la siguiente ruta (<https://drive.google.com/drive/folders/1oBLlCRzSQtV-mYpyaOOrT3YkxbWxSkVU?usp=drive_link>) y cargarlos en el directorio `/train`*

Será necesario abrir un terminal el del directorio raíz de ComicAI y ejecutar uno de estos 2 comandos:

`python comic_AI.py`

`python3 comic_AI.py`

**3. Salida de resultados**

El proceso se ejecutará al completo, imprimiendo el log perteniciente de cada módulo, y finalmente devolverá el tiempo de ejecución de todo el proceso y la frase: *ENHORABUENA, YA SE PUEDE ESCUCHAR ESTE COMIC !!*

Los archivos de audio de cada viñeta se pueden encontrar en el directorio ``data/output/output_audio_test/combined.``

Por otro lado en cada una de los siguientes directorios encontramos los archivos de salida de cada módulo o proceso:

- data/output
    - divide_images_test (``imágenes derivadas de la identificación de viñetas``)
    - divide_pages_test (`imágenes derivadas separación por páginas del comic`)
        - pages_raw (`imágenes de cada página del comic`)
        - pages_routes (`archivo csv que aloja las rutas de las imágenes de la carpeta pages_raw`)
    - ouput_audio_test (`salida final de audio para cáda viñeta del comic`)
    - output_description_test (`archivos de texto donde se describe lo que aparece en cada viñeta`)
    - output_description_translate_test (`archivos de texto con la traducción de los archivos de descripción de cada viñeta`)
    - output_text_test (`archivos de texto donde se transcribe el texto que aparece en cada viñeta`)

## Enlaces de interés

Enlace al paper de Medium.com:
<https://medium.com/sistema-de-narración-de-cómics-para-personas-con/sistema-de-narración-de-cómics-para-personas-con-discapacidad-visual-f0bd9c86f14f>


## Autores del proyecto

`@JackDM`

`@CharlosLR`

`@RogerBritoAI`