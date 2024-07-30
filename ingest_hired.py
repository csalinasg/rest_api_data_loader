from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
import pandas as pd
import os 

conn = snowflake.connector.connect(
    user=os.getenv('SF_USER'),
    password=os.getenv('SF_PASSWORD'),
    account=os.getenv('SF_ACCOUNT'),
    warehouse=os.getenv('SF_WAREHOUSE'),
    database=os.getenv('SF_DATABASE'),
    schema=os.getenv('SF_SCHEMA'),
    role=os.getenv('SF_ROLE')
)

data=pd.read_csv("data\hired_employees.csv", header=None, names=["id", "name", "datetime", "departament_id", "job_id"])

cur=conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS "hired_employees" ("id" Integer, "name" String, "datetime" String, "departament_id" Integer, "job_id" Integer)')
cur.execute('CREATE OR REPLACE TEMPORARY TABLE "temp_hired_employees" ("id" Integer, "name" String, "datetime" String, "departament_id" Integer, "job_id" Integer)')
write_pandas(conn, data, table_name="temp_hired_employees")

merge_query = """
MERGE INTO "hired_employees" AS target
USING "temp_hired_employees" AS source
ON target."id" = source."id"
WHEN MATCHED THEN
    UPDATE SET
        target."name" = source."name"
WHEN NOT MATCHED THEN
    INSERT ("id", "name", "datetime", "departament_id", "job_id")
    VALUES (source."id", source."name", source."datetime", source."departament_id", source."job_id")
"""

cur.execute(merge_query)

cur.execute('DROP TABLE "temp_hired_employees"')

