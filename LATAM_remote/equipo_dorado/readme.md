Selección de elementos a desarrollar
Discutimos y definimos mediante una lluvia de ideas cuáles serían los elementos apropiados para presentar a un usuario sin expertise técnico nuestros resultados. Para lograr esto, debíamos enfocarnos en dos cosas principalmente:

Facilitar el uso interactivo del usuario (que sea mínimo y sencillo en controles)
Que los indicadores fuesen suficientemente detallados y comprendieran de manera general todas las dudas o consultas que una persona pudiera hacerse (para que se incluyeran en la visualización de forma predeterminada)
A continuación presentamos los elementos que elegimos para desarrollar:

Series de tiempo y predicción.
Es el objetivo principal del proyecto: deseamos mostrar de manera fácil y entendible cómo varían los precios de ciertos productos en el tiempo (inflación). A la vez, mostrar cuál es la predicción del comportamiento de los mismos en base al modelo de AI previamente desarrollado. Para mandar el mensaje principal debemos mostrar visualmente la fluctuación de los precios de los productos en el tiempo (el precio promedio, ya que se analizan diferentes marcas para cada producto). Y si se deseara analizar a detalle a un producto, consideraríamos en ese caso la fluctuación de los precios por marca en el tiempo, lo que sería una comparativa sobre las marcas.

Cálculo de inflación de productos.
La variación de precios en el tiempo es fácilmente interpretada mediante una gráfica. Sin embargo, el conocer el número exacto que representa la variación de precios en un periodo (inflación) de cada producto requiere un cálculo ya que puede ser muy complicado y/o muy lento determinarlo en base a gráficas solamente. El cálculo de la inflación se vuelve clave ya que es el resultado final del comportamiento del precio de cada producto en el periodo analizado. Este indicador es el que nos dirá si el movimiento fue hacia arriba (subió de precio) o hacia abajo (bajó de precio). En los casos donde la inflación no sea tan notable visualmente o sea complicada de estimar, el indicador nos dirá incluso con diferencias mínimas de centavos si el movimiento fue a la alza o la baja.

Comparativa de marcas.
En el mercado nacional y global siempre existe una cantidad múltiple de marcas para un mismo producto. Tenemos algunas marcas genéricas de bajo costo y al mismo tiempo podemos encontrarnos con otras marcas premium dirigidas a consumidores con mayor poder adquisitivo. Sin embargo, todas corresponden a un mismo producto. Por ello consideramos importante tomarlas en cuenta y distinguirlas dentro del análisis de un producto a detalle.

Top 3 de variación mayor/menor.
Consideramos importante presentar cuáles fueron los productos que tuvieron mayor y menor variación en el periodo analizado de una manera directa. Así con un “top”, cualquier usuario podrá conocer cuáles fueron los artículos más afectados o beneficiados por la economía.

KPIs (indicadores clave).
Mostrar la variación de precio de los productos o cuáles fueron los productos top en variación no nos parecía suficiente. Discutimos sobre facilitar indicadores adicionales que pudieran apoyar a dar un mejor panorama de qué pasó con cada producto para permitir hacer un análisis más personalizado. Por ello consideramos incluir adicionalmente para cada producto: precio mínimo, precio promedio, mediana de precio y precio máximo. Así, apoyaríamos la visualización con indicadores básicos que soportarían con exactitud cualquier duda respecto a las gráficas.

Periodo de análisis.
Este elemento comprende la flexibilidad del periodo a utilizar para realizar cada análisis de una persona. Consideramos importante permitir que el periodo pueda ser variable para cada caso ya que de esta manera, podría revisarse únicamente la temporada de interés y al mismo tiempo permitiríamos la comprobación de variaciones en cualquier periodicidad (diaria, semanal, mensual, anual, etc.) En un segundo caso, podría darse el escenario en que, tras un análisis de periodicidad amplia, por ejemplo anual, se observe que hay algo interesante a observar durante un par de meses determinados. Entonces, ajustando el periodo a esos meses, la persona podría investigar qué pasó en ese intervalo y descubrir información útil.

Dashboard general de resultados.
Consideramos que todo lo anterior debíamos consolidarlo en un solo punto. Debería ser algo de fácil acceso que reuniera todos los elementos que definimos desarrollar y presentarlos de manera sencilla a cualquier persona. Por esto decidimos que la mejor manera de lograrlo sería con un dashboard general de resultados. Un dashboard nos permite consolidar la información y resultados, y representar a la vez un medio de autoayuda para la persona que desee hacer un análisis. Con las gráficas e indicadores definidos, un diseño sencillo y controles mínimos de operación, debería ser muy simple para cualquier persona accederlo, operarlo y realizar análisis sin mayor complicación.

Demo
main El dashboard desarrollado se encuentra disponible en la siguiente liga https://latcovmmunity.com *

la sección correspondiente a QuickSight podría no estar disponible ya que se requiere un servidor de aplicaciones para generar una URL dinámica (válida por un periodo de 5min), y el hosting actual del proyecto, S3 (AWS) es estático. Para embeberlo se usaron una serie de acondicionamientos especiales, workarounds y tareas manuales por evento como: https, caching CDN, Roles AWS, políticas AWS, generar manualmente URL dinámico expirable (para simular el app server), etc.

Algunos screenshots:

Dashboard Tableau Dashboard Tableau
Dashboard QuickSight
Público General Dashboard Tableau Dashboard Tableau Dashboard Tableau Dashboard Tableau
Público Especializado Dashboard Tableau Dashboard Tableau Dashboard Tableau
 Pages 1
Find a Page…
Home
Clone this wiki locally
https://github.com/SaturdaysAI-EquipoMorado/Visualizacion-de-Datos.wiki.git
