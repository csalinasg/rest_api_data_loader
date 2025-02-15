# CVS a Snowflake API LOADER

## Descripción
Rest API para carga de archivos csv a Snowflake por defecto viene configurado para cargar archivos departaments.csv, hired_employees.csv y jobs.csv, pero esta construido con un framework de ingesta que permite añadir a traves de un csv y la configuracion de un diccionario para añadir nuevas tablas al datawarehouse en snowflakes.


## Características

- Permite la carga de archivos a traves de un endpoint o a traves de una interfaz web
- Permite la carga de datos en formato csv por defecto para departaments.csv, hired_employees.csv, jobs.csv.
- Permite consultar empleados contratados por trimestre
- Permite consultar empleados contratados por departamento que sea mayor al promedio de contrataciones del 2021
- Permite la carga de nuevos archivos csv delimitados por "," los cuales se deben agregar al diccionario en el archivo config.py

## Limitaciones

- Los archivos no deben contener encabezado y deben estar delimitados por ",".
- Solo acepta formato csv.
- No acepta archivos mayores a 2 MB.
- permite la carga de maximo 1000 registros por solicitud.

## Requisitos

Python:

flask
flask_wtf  
snowflake-connector-python
python-dotenv
pandas
snowflake-connector-python[secure-local-storage,pandas]
snowflake-connector-python[pandas]

Las dependencias se encuentran en el archivo requirements.txt

Base de Datos:

Datawarehouse Snowflake

## Ejecución

Para ejecutar la aplicacion localmente en el puerto 5000. 
python main.py

## Formuario WEB

Se puede acceder a un formulario web para la carga de archivos a traves de la URL:

http://127.0.0.1:5000/

## Endpoints:

Endpoint para carga de archivos:

curl --location 'http://127.0.0.1:5000/upload' \
--form 'file=@"{ruta_del_archivo}/hired_employees.csv"'

curl --location 'http://127.0.0.1:5000/upload' \
--form 'file=@"{ruta_del_archivo}/jobs.csv"'

curl --location 'http://127.0.0.1:5000/upload' \
--form 'file=@"{ruta_del_archivo}/departments.csv"'

## Endpoint para consultas sobre los datos:

1.- Número de empleados contratados para cada puesto y departamento en 2021, divididos por trimestre. La tabla debe estar ordenada alfabéticamente por departamento y puesto. 

curl --location 'http://127.0.0.1:5000/departments/quarter'

2.- Lista de IDs, nombre y número de empleados contratados de cada departamento que contrató más empleados que el promedio de empleados contratados en 2021 para todos los departamentos, ordenada por el número de empleados contratados (de forma descendente).

curl --location 'http://127.0.0.1:5000/departments/top'


## ************* Challenge creado para el cargo de Data Engineer en la empresa GLOBANT *************