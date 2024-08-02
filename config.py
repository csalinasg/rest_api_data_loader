import os
import snowflake.connector

connection_params = {
    'user': os.getenv('SF_USER'),
    'password': os.getenv('SF_PASSWORD'),
    'account': os.getenv('SF_ACCOUNT'),
    'warehouse': os.getenv('SF_WAREHOUSE'),
    'database': os.getenv('SF_DATABASE'),
    'schema': os.getenv('SF_SCHEMA'),
    'role': os.getenv('SF_ROLE')
}

def get_connection():
    
    conn = snowflake.connector.connect(
        user=connection_params['user'],
        password=connection_params['password'],
        account=connection_params['account'],
        warehouse=connection_params['warehouse'],
        database=connection_params['database'],
        schema=connection_params['schema'],
        role=connection_params['role']
    )
    return conn

allowed_file_types = ['.csv'] 

#diccionario de configuracion para archivos .csv nuevos, los archivos deben ser sin encabezado 
files_configuration = {
    "hired_employees": {
        "table": "hired_employees",
        "columns": {
            "id": "Integer",
            "name": "String",
            "datetime": "String",
            "departament_id": "Integer",
            "job_id": "Integer"
        },
        "primary_key": "id",
        "connection": connection_params
    },
    "departments": {
        "table": "departaments",
        "columns": {
            "id": "Integer",
            "departament": "String"
        },
        "primary_key": "id",
        "connection": connection_params
    },
    "jobs": {
        "table": "jobs",
        "columns": {
            "id": "Integer",
            "job": "String"
        },
        "primary_key": "id",
        "connection": connection_params
    }
}
