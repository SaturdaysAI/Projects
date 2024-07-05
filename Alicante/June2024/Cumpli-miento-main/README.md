Resumen:
Este proyecto tiene como objetivo desarrollar una herramienta automática para evaluar si las políticas de privacidad de diferentes empresas cumplen 
con ciertos derechos establecidos por el Reglamento General de Protección de Datos (GDPR). Utilizando técnicas de procesamiento de lenguaje natural (NLP) 
y aprendizaje automático, se analiza el texto de las políticas de privacidad y se determina el cumplimiento de varios derechos específicos.

Objetivos:

Extraer y analizar el texto de documentos HTML que contienen políticas de privacidad.
Entrenar modelos de clasificación para determinar el cumplimiento de varios derechos de privacidad.
Evaluar nuevas políticas de privacidad mediante modelos entrenados y generar un informe de cumplimiento.
Pasos del Proyecto:

Procesamiento de Datos:

Descomprimir el archivo ZIP y extraer los documentos HTML.
Leer el archivo CSV y unificar los nombres de las empresas para garantizar la correspondencia con los documentos HTML.
Extraer el texto de los documentos HTML utilizando BeautifulSoup.
Entrenamiento del Modelo:

Preprocesar el texto extraído y preparar las etiquetas para varios derechos de privacidad.
Entrenar modelos de clasificación para cada derecho utilizando TF-IDF y regresión logística.
Evaluar la precisión de los modelos utilizando un conjunto de datos de prueba.
Evaluación de Nuevas Políticas:

Proporcionar una URL de una política de privacidad.
Extraer el texto de la URL proporcionada y evaluarlo utilizando los modelos entrenados.
Generar un informe indicando qué derechos se cumplen y cuáles no.
Tecnologías Utilizadas:

Python
Google Colab
Pandas
BeautifulSoup
Scikit-learn
Requests
Conclusión:
Este proyecto proporciona una solución automatizada para evaluar el cumplimiento de las políticas de privacidad con respecto a los derechos del GDPR.
Al aprovechar técnicas avanzadas de NLP y aprendizaje automático, la herramienta puede analizar eficientemente múltiples políticas de privacidad
y ofrecer una evaluación detallada del cumplimiento de cada derecho.
