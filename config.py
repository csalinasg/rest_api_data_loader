import os

connection_params = {
    'user': os.getenv('SF_USER'),
    'password': os.getenv('SF_PASSWORD'),
    'account': os.getenv('SF_ACCOUNT'),
    'warehouse': os.getenv('SF_WAREHOUSE'),
    'database': os.getenv('SF_DATABASE'),
    'schema': os.getenv('SF_SCHEMA'),
    'role': os.getenv('SF_ROLE')
}

allowed_file_types = ['.csv'] 

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
