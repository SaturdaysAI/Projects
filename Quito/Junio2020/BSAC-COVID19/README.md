El presente proyecto está diseñado para trabajar en el entorno de Google Colaboratory, utilizando un GPU (graphics processing unit) y valiéndose de Google Drive tanto para lectura como escritura de datos. El trabajo está dividido en 3 notebooks:

1. **BSAC_Covid_19-Parte_1-Interactive_Abstract_and_Expert_Finder.ipynb** basado en el trabajo de John David Parson “Interactive Search using BioBERT and CorEx Topic Modeling” [4] en el contexto del reto de Kaggle “[COVID-19 Open Research Dataset Challenge (CORD-19)](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)”. El objetivo de este notebook es:
    * Leer los títulos y resúmenes (en adelante denominados "documentos"), de los artículos científicos del set de datos provisto en el reto Kaggle.
    * Limpiar los datos, procesándolos con tareas tradicionales de NLP (Natural Language Processing) tales como: remover stop-words, generar matriz de documentos vs los términos y la frecuencia con la que estos aparecen  (TF-IDF), generar n-gramas, entre otras.
    * Utilizar el algoritmo de entrenamiento no-supervisado [CorEx  (Correlation Explained)](https://pypi.org/project/corextopic/
) para agrupar los documentos por tópicos o temas.
    * Como producto final, se generarán dos archivos:
        * `df_final_covid_clean_topics.pkl` con el dataframe final de los documentos, su clasificación en tópicos y una columna con los términos de los documentos, ordenados según la frecuencia en la que aparecen en los mismos.
        * `corex_topic_model.pkl` un archivo en el formato CorEx que contendrá los tópicos determinados para el conjunto de documentos provisto, así como la lista de palabras que conforma cada tópico (ordenada según su relevancia relativa).

2. **BSAC_Covid_19-Parte_2-BERT_Fine_Tuning.ipynb** toma como materia prima los documentos y la clasificación en tópicos realizada en el anterior notebook (de los archivos previamente mencionados) y se procede con la tarea de Afinamiento (Fine-Tuning) del modelo pre-entrenado de BERT, en este caso [BioBERT-Base v1.1 (+ PubMed 1M)](https://github.com/dmis-lab/biobert), compuesto de los siguietnes archivos:  

        biobert_v1.1_pubmed/
            bert_config.json
            model.ckpt-1000000.data-00000-of-00001
            model.ckpt-1000000.index
            model.ckpt-1000000.meta
            vocab.txt

    Para esta tarea, nos basamos principalmente en el artículo “[Building a Multi-label Text Classifier using BERT and TensorFlow](https://towardsdatascience.com/building-a-multi-label-text-classifier-using-bert-and-tensorflow-f188e0ecdc5d)”  del autor Javaid Nabi, producto de lo cual se obtuvieron los siguientes archivos, correspondientes al modelo afinado para una tarea de [clasificación de texto en múltiples etiquetas](https://en.wikipedia.org/wiki/Multi-label_classification). Producto del afinamiento, se obtuvieron los siguientes archivos:  
    
        fine-tuned/model/
          eval/
          checkpoint
          events.out.tfevents.1592530631.e29c1ab3f26a
          graph.pbtxt
          model.ckpt-1023.data-00000-of-00001
          model.ckpt-1023.index
          model.ckpt-1023.meta    

3. **BSAC_Covid_19-Parte_3-BioBERT+CorEx_Topic_Search.ipynb** este notebook extiende el trabajo de John David Parsons “[BioBERT+CorEx Topic Search](https://www.kaggle.com/jdparsons/biobert-corex-topic-search)” , en el que se utiliza y/o implementa:
    * El archivo df_final_covid_clean_topics.pkl como fuente de información (documentos y tópicos CorEx).
    * [Bert as a Service](https://bert-as-service.readthedocs.io/en/latest/) que es un servidor que, basado en un modelo pre-entrenado (BioBERT-Base v1.1) y opcionalmente en un modelo afinado (el obtenido en el paso anterior, tensorflow checkpoint `ckpt-1023`), permite codificar texto al formato BERT para poder realizar tareas de NLP con el modelo.
    * Widget de Búsqueda: herramienta construida con la librería [Jupyter Widgets](https://ipywidgets.readthedocs.io/en/latest/user_guide.html) que permite la búsqueda semántica de artículos en la base de datos, de acuerdo a la pregunta planteada en la caja de texto y al resto de parámetros que permite configurar el widget. 
