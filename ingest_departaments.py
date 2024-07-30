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

data=pd.read_csv("data\departments.csv", header=None, names=["id", "departament"])

cur=conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS "departaments" ("id" Integer, "departament" String)')
cur.execute('CREATE OR REPLACE TEMPORARY TABLE "temp_departaments" ("id" Integer, "departament" String)')
write_pandas(conn, data, table_name="temp_departaments")

merge_query = """
MERGE INTO "departaments" AS target
USING "temp_departaments" AS source
ON target."id" = source."id"
WHEN MATCHED THEN
    UPDATE SET
        target."departament" = source."departament"
WHEN NOT MATCHED THEN
    INSERT ("id", "departament")
    VALUES (source."id", source."departament")
"""

cur.execute(merge_query)

cur.execute('DROP TABLE "temp_departaments"')


