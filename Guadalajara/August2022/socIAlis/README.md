Equipo rosa

Despliegue local

Instalar python 3.* ejecutable o comando

Instalar pipenv: pip install pipenv

Clonar el repositorio con: git clone https://github.com/FelixAscWii/socIAlis.git

Ejecutar: pipenv shell Para crear un ambiente virtual 

Pegar el archivo secret.json en la raíz del repositorio

Instalar todos los paquetes y librerías con: pipenv install --ignore-pipfile    
o para instalar una librería nueva: pipenv install {{ nombre }}

Migraciones(    
Crear migraciones: python manage.py makemigrations    
Ejecutar migraciones: python manage.py migrate)

Para correr el servidor: python manage.py runserver    
si sale un cohete, significa que vamos por buen camino

Para crear un usuario admin: python manage.py createsuperuser    
acceder al panel de administración en: /admin

