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
PIVOT(SUM("employees") FOR "quarter" IN (ANY ORDER BY "quarter")DEFAULT ON NULL (0))
AS p ("departament", "job", "Q1", "Q2", "Q3", "Q4")
ORDER BY "departament"



/*
List of ids, name and number of employees hired of each department that hired more
employees than the mean of employees hired in 2021 for all the departments, ordered
by the number of employees hired (descending).
*/

WITH c as (
select "departament_id", count(*) as "q_employees" from "hired_employees" where EXTRACT(YEAR FROM TO_TIMESTAMP("datetime", 'YYYY-MM-DD"T"HH24:MI:SS"Z"')) = 2021
group by "departament_id"
)

--select avg("q_employees") from c  -> 129.61535

SELECT "d"."id" as "id_departament","d"."departament", count(*) as "employees"
FROM "hired_employees" as "he"
INNER JOIN "departaments" as "d" on "d"."id" = "he"."departament_id"
INNER JOIN "jobs" AS "j" on "j"."id" = "he"."job_id"
group by "d"."departament","d"."id"
having count(*) > (select avg("q_employees") from c ) 
order by count(*) desc