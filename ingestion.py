import snowflake.connector
import pandas as pd
from config import *
from snowflake.connector.pandas_tools import write_pandas
from datetime import datetime

def merge_data(config_name, file_name):

    config = files_configuration.get(config_name)

    file = file_name
    table = config["table"]
    columns = config["columns"]
    primary_key = config["primary_key"]
    connection = config["connection"]

    conn = snowflake.connector.connect(
        user=connection['user'],
        password=connection['password'],
        account=connection['account'],
        warehouse=connection['warehouse'],
        database=connection['database'],
        schema=connection['schema'],
        role=connection['role']
    )
    
    data = pd.read_csv(file, header=None, names=columns.keys(), nrows=1000)
    
    cur = conn.cursor()
    
    columns_definitions = ', '.join(f'"{column}" {type}' for column, type in columns.items())
    create_table_query = f'CREATE TABLE IF NOT EXISTS "{table}" ({columns_definitions})'
    cur.execute(create_table_query)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f') 
    temp_table_name = f"temp_{table}_{timestamp}" #creare una tabla temporal con timestamp en el caso que lleguen dos peticiones al mismo tiempo
    create_temp_table_query = f'CREATE OR REPLACE TEMPORARY TABLE "{temp_table_name}" ({columns_definitions})'
    cur.execute(create_temp_table_query)
    
    write_pandas(conn, data, table_name=temp_table_name)
    
    columns_list = ', '.join(f'"{column}"' for column in columns.keys())
    values_list = ', '.join(f'source."{column}"' for column in columns.keys())
    update_set = ', '.join(f'target."{column}" = source."{column}"' for column in columns.keys() if column != primary_key) #sacamos la llave primary key
    
    merge_query = f"""
    MERGE INTO "{table}" AS target
    USING "{temp_table_name}" AS source
    ON target."{primary_key}" = source."{primary_key}"
    WHEN MATCHED THEN
        UPDATE SET
            {update_set}
    WHEN NOT MATCHED THEN
        INSERT ({columns_list})
        VALUES ({values_list})
    """
    cur.execute(merge_query)
    
    cur.execute(f'DROP TABLE "{temp_table_name}"')
    
    cur.close()
    conn.close()


