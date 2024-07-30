/*
Number of employees hired for each job and department in 2021 divided by quarter. The
table must be ordered alphabetically by department and job.
*/

WITH temp_query as (
SELECT "departament","job", count(*) as "employees",
EXTRACT(QUARTER FROM TO_TIMESTAMP("datetime", 'YYYY-MM-DD"T"HH24:MI:SS"Z"')) as "quarter"
FROM "hired_employees" as "he"
INNER JOIN "departaments" as "d" on "d"."id" = "he"."departament_id"
INNER JOIN "jobs" AS "j" on "j"."id" = "he"."job_id"
where EXTRACT(YEAR FROM TO_TIMESTAMP("datetime", 'YYYY-MM-DD"T"HH24:MI:SS"Z"')) = 2021
group by "departament","job", EXTRACT(QUARTER FROM TO_TIMESTAMP("datetime", 'YYYY-MM-DD"T"HH24:MI:SS"Z"'))
)


SELECT *
  FROM temp_query
 PIVOT(SUM("employees") FOR "quarter" IN (ANY ORDER BY "quarter"))
  ORDER BY "departament";