# Buscador de recetas

Aplicación web para buscar recetas a partir de sus ingredientes.

## Requisitos
* Python3
* PostgreSQL

## Instalación

1. Clonar el repositorio:
```
git clone https://github.com/espinoza/sabropedia
```

2. Crear entorno virtual y activar:
```
python3 -m venv .venv
source .venv/bin/activate
```

3. Instalar paquetes de Python necesarios:
```
pip install -r requirements.txt
```

4. Entrar a PostgreSQL:
```
sudo -u usuario_postgresql psql
```
reemplazando `usuario_postgresql` con el nombre de usuario de PostgreSQL.
Generalmente, el nombre de usuario por defecto es `postgres`.


5. Crear base de datos y salir de PostgreSQL:
```
CREATE DATABASE nombre_base_de_datos;
\q
```
reemplazando `nombre_base_de_datos` con el nombre deseado para la base de datos.


6. Crear el archivo `config.env` con el siguiente contenido:
```
SECRET_KEY=randomkey
DB_NAME=nombre_base_de_datos
DB_USER=usuario_postgresql
DB_PASSWORD=contraseña_postgresql
```
reemplazando `nombre_base_de_datos`, `usuario_postgresql` y `contraseña_postgresql`
con sus valores correspondientes.


7. Migrar base de datos:
```
python manage.py migrate
```

8. Iniciar servidor:
```
python manage.py runserver
```

Se puede acceder a la aplicación a través de un navegador web, utilizando la
dirección `http://localhost:8000`.
