# Sabropedia

Aplicación web para buscar recetas a partir de sus ingredientes o por nombre de receta.

## Características
* Filtrar recetas por ingredientes que se desea incluir.
* Excluir según ingredientes no deseados.
* Opción de restringir ingredientes a aquellos que son ingresados, sin incluir otro adicional.
* Filtrar por nombre de receta
* Los ingredientes se pueden escribir con cualquier nombre. Ejemplo: *frijoles*, *porotos* y *alubias* generan los mismos resultados.

## Instalación

### Requisitos
* `Python3`
* `PostgreSQL`
* `Sass` con `Node-Sass`

### Pasos a seguir

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
reemplazando `nombre_base_de_datos` con el nombre deseado para
la base de datos.


6. Crear el archivo `config.env` con el siguiente contenido:
```
SECRET_KEY=randomkey
DB_NAME=nombre_base_de_datos
DB_USER=usuario_postgresql
DB_PASSWORD=contraseña_postgresql
```
reemplazando `nombre_base_de_datos`, `usuario_postgresql`
y `contraseña_postgresql` con sus valores correspondientes.


7. Migrar base de datos:
```
python manage.py migrate
```


8. Compilar archivos CSS a partir de SCSS:
```
node-sass assets/scss -o static/css
```


9. Iniciar servidor:
```
python manage.py runserver
```

Se puede acceder a la aplicación a través de un navegador web,
utilizando la dirección `http://localhost:8000`.

## Inicializar base de datos

1. `python manage.py getsources`
2. `python manage.py getrecipes`
3. `python manage.py detectingredients`