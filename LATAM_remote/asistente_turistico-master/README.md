# **Proyecto Saturdays.AI Equipo Tinto: SMARTOUR.AI**

**Miembros del equipo y roles:**
- Mentor: Rodrigo Herrera
- Full Stack developer: Julio Cortés Fredes         
- Project manager: José Luis Rangel Guerrero   


**Nombre detallado del proyecto:** 
- Asistente turístico virtual para turistas internacionales que buscan tener experiencias únicas durante su estancia en México.

**Nombre corto o comercial del proyecto:** SmarTour.AI

**Eje rector o impacto social principal del proyecto:** Turismo

**Alineación o impacto hacia objetivos de desarrollo sostenible:**

Nuestro proyecto se alinea con los siguientes objetivos de desarrollo sustentable: **TRABAJO DECENTE Y CRECIMIENTO ECONÓMICO**

- 8.9 De aquí a 2030, elaborar y poner en práctica políticas encaminadas a promover un turismo sostenible que cree puestos de trabajo y promueva la cultura y los productos locales.
- 8.a Aumentar el apoyo a la iniciativa de ayuda para el comercio en los países en desarrollo, en particular los países menos adelantados, incluso mediante el Marco Integrado Mejorado para la Asistencia Técnica a los Países Menos Adelantados en Materia de Comercio.

**Descripción del problema específico:**

El COVID-19 ha tenido un impacto profundo en el turismo. En México se ha
registrado una caída del 41.2% en el número de turistas internacionales
respecto de 2019. Esto representa, a septiembre de 2020, una pérdida de 10.4 mil millones de dólares en ingresos por visitantes internacionales.
Asimismo, dado que la recuperación del turismo dependerá de cómo
evolucione la propagación del virus, de las restricciones de viaje y de
que el público recupere la confianza para volver a viajar al extranjero,
es importante poner en marcha proyectos que ayuden en la aceleración de
la recuperación de este sector.

**Hipótesis:**

En este momento, es importante posicionar a México cómo un destino
seguro y de calidad para el turismo extranjero. Para ello, las
experiencias que viva el turista extranjero durante su estancia en el
destino son de suma importancia para que decida regresar y recomendar al
país como un destino valioso. Por tanto, nuestra hipótesis es:

- Si se realizan recomendaciones sobre experiencias personalizadas al turista internacional, entonces la calidad de la estancia del turista internacional se verá impactada positivamente, lo cual, aumentará la probabilidad de que el turista regrese y recomiende la zona que visitó.

Supuestos:

- Al turista extranjero le interesa tener experiencias de calidad durante su estancia.

- Al turista extranjero le es complicado acceder a experiencias de calidad en la zona que visita.

- Se pueden ofrecer experiencias personalizadas que mejoren la experiencia del turista

**Población objetivo/Unidad de análisis:**

Nuestra población objetivo son los turistas internacionales de
internación que llegan a la Ciudad de México por vía aérea. Considerando
los datos para 2019, el número de turistas que llegan a este destino
bajo dicha modalidad es de 4.9 millones.

**MVP**

1.  Se acota el proyecto a recomendaciones para visitantes de la Ciudad
    de México

2.  Se ofrecen las siguientes experiencias a los usuarios:

    a.  Gastronómica: Restaurantes de comida típica mexicana

    b.  Cultural: Museos, Teatros y Templos

    c.  Ecológica: Parques y actividades al exterior.

3.  El usuario accede mediante una aplicación web en donde recibe una
    recomendación posterior al llenado de un cuestionario interactivo

**Descripción de las fuentes de información:**

Google places API: De esta fuente se extraerá información sobre los
lugares que pueden ser visitados por los turistas internacionales. La
lista de campos es la siguiente:

- Nombre del lugar, ubicación, sitio web, horarios de servicio, nivel
    de precios, evaluación global, número de evaluaciones, detalle de
    cada evaluación (texto, fecha, idioma y foto del evaluador) y tipo
    de lugar.

Wextractor: Dado que Google places limita el número de reviews a
5 por establecimiento, se utiliza esta fuente para extraer 170 reviews
por cada lugar considerado para el MVP

**Descripción de la solución**

Nuestra solución será una aplicación web a la cual podrá acceder
cualquier usuario sin necesidad de registrarse. Para recibir la
recomendación, el usuario tendrá que llenar un cuestionario interactivo
que recabará información sobre sus intereses. Utilizando el
cuestionario, un modelo de recomendación hará match entre las respuestas
del usuario y los lugares disponibles en la plataforma, para recomendar
aquel que mejor se adecue a los intereses del turista.

**Flujo de usuario**

El siguiente diagrama describe la interacción que el usuario tendría con
la solución planteada:

Diagrama 1: Flujo de usuario

![alt text](https://github.com/SaturdaysAI-Tinto/asistente_turistico/blob/master/Picture1.png)


1.  El usuario se Registra/Ingresa en la aplicación e ingresa
    información personal.

2.  El usuario comienza el uso de la aplicación seleccionando algunos
    intereses aleatorios del día

3.  La aplicación envía los intereses al modelo mediante API y devuelve
    match con actividades o lugares.

4.  La aplicación muestra inmediatamente sugerencias de actividades en
    forma de carrusel de imágenes parecido a instagram.

**Clientes potenciales y usuarios finales**

Para esta solución, los usuarios finales pueden ser:

-   Turistas de internación que llegan a la Ciudad de México vía aérea
    sin un plan o itinerario específico.

-   Turistas de otros estados de la República Mexicana que vienen a
    conocer la Ciudad de México.

-   Residentes de la Ciudad de México que les gusta experimentar nuevas
    experiencias y que les cuesta trabajo escoger a dónde ir.


