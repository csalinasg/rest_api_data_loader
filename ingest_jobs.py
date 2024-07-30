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

data=pd.read_csv("data\jobs.csv", header=None, names=["id", "job"])

cur=conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS "jobs" ("id" Integer, "job" String)')
cur.execute('CREATE OR REPLACE TEMPORARY TABLE "temp_jobs" ("id" Integer, "job" String)')
write_pandas(conn, data, table_name="temp_jobs")

merge_query = """
MERGE INTO "jobs" AS target
USING "temp_jobs" AS source
ON target."id" = source."id"
WHEN MATCHED THEN
    UPDATE SET
        target."job" = source."job"
WHEN NOT MATCHED THEN
    INSERT ("id", "job")
    VALUES (source."id", source."job")
"""

cur.execute(merge_query)

cur.execute('DROP TABLE "temp_jobs"')

