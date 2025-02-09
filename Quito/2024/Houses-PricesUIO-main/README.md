# House Prices UIO

¡Bienvenido al proyecto **House Prices UIO**!  
Este es un sistema de recomendación de inmuebles desarrollado con Vue.js, diseñado para ayudar a los usuarios a encontrar su hogar ideal de forma interactiva.

---

## 🚀 Características

- 🏡 **Recomendaciones Personalizadas:** Los usuarios reciben sugerencias basadas en sus preferencias (ubicación, presupuesto, número de habitaciones, etc.).
- 🌟 **Interfaz Moderna:** Incluye un diseño de chatbot interactivo para facilitar la experiencia del usuario.
- 📊 **Análisis Completo:** Presenta información detallada de cada propiedad, como precios, amenidades, áreas, y ubicación.
- ⚡ **Rendimiento Óptimo:** Usa Vue.js para garantizar una aplicación rápida y eficiente.

---

## 📂 Estructura del Proyecto

```
HousePrices/
├── public/          # Archivos estáticos (HTML, favicons)
├── src/             # Código fuente principal
│   ├── assets/      # Imágenes, estilos, y otros recursos estáticos
│   ├── components/  # Componentes reutilizables en Vue.js
│   ├── views/       # Vistas principales de la aplicación
├── .gitignore       # Archivos y carpetas ignoradas por Git
├── package.json     # Dependencias y scripts del proyecto
├── README.md        # Documentación del proyecto
└── vue.config.js    # Configuración personalizada de Vue.js
```

---

## 🛠️ Tecnologías Utilizadas

- **Vue.js:** Framework frontend principal.
- **JavaScript (ES6+):** Lenguaje de programación.
- **Node.js & npm:** Para la gestión de paquetes y scripts.
- **CSS:** Para estilos personalizados.
- **GitHub:** Control de versiones y alojamiento del repositorio.


---

## 📦 Instalación

### 1. Requisitos Previos

Asegúrate de tener instalado:

-Python 3.10 a 3.12
-uv, pip o pipx para la instalación de paquetes en Python.
-Node.js: Descargar Node.js
-npm (incluido con Node.js)

### 2. Instalación de Langflow y Configuración del Entorno Virtual

1. Crea un entorno virtual en Python:

   ```bash
   python -m venv langflow_env

2. Activa el entorno virtual con (Windows) langflow_env\Scripts\activate
3. Instala Langflow en su versión 1.1 python -m pip install langflow==1.1
4. Carga el archivo de flujo en Langflow (Anexo como LangflowRAGHouses.json) y ejecútalo.
    Aquí necesitarás ingresar tus APIS, y endpoints necesarios según el esquema de archivo de flujo te mostrará.

### 3. Clona este repositorio
   
   ```bash
   git clone https://github.com/TuUsuario/HousePrices.git
   cd HousePrices
   ```
## 🖥️ Uso del Proyecto

### Desarrollo

Para iniciar el servidor de desarrollo:
```bash
npm run serve
```

El servidor estará disponible en:  
[http://localhost:8080](http://localhost:8080)

---

## 🌟 Funcionalidades Clave

1. **Recomendaciones de Inmuebles:**
   Los usuarios pueden interactuar con un chatbot para recibir propiedades sugeridas basadas en:
   - Ubicación preferida.
   - Presupuesto.
   - Número de habitaciones, baños, y amenidades adicionales.

2. **Interfaz Visualmente Atractiva:**
   - Uso de componentes dinámicos en Vue.js.
   - Estilos modernos y responsivos.

3. **Resultados Detallados:**
   Cada propiedad incluye:
   - Precio.
   - Amenidades (jardines, parqueaderos, etc.).
   - Distancia a transporte público, escuelas, y más.

---

## 🔧 Personalización

Puedes personalizar la configuración del proyecto editando el archivo `vue.config.js` y otros archivos de configuración en la carpeta raíz.

---

## ✨ Autores

**Daniela Tupiza**

**Salomé Polanco**

**Steven Pérez**

**María Rosa Camacho**
    

Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto. ¡Gracias por visitar este repositorio!
