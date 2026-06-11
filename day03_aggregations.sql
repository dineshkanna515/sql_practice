-- =====================================================================
-- Day 3 — SQL Aggregation & Subqueries
-- Week 1 · Foundations
-- Status: 10 / 15 complete. Remaining: 1661, 1934, 1158, 550, 262 (tomorrow AM)
--
-- Problems 6-15 are the deferred Day 2 join problems, now finished with
-- GROUP BY / HAVING / subquery knowledge from Day 3.
-- Dialect: PostgreSQL (LeetCode judge accepts PG).
-- =====================================================================


-- ---------------------------------------------------------------------
-- 511. Game Play Analysis I
-- Skill: GROUP BY + MIN
-- First login date per player.
-- ---------------------------------------------------------------------
select player_id, min(event_date) as first_login
from Activity
group by player_id;


-- ---------------------------------------------------------------------
-- 586. Customer Placing the Largest Number of Orders
-- Skill: GROUP BY + ORDER BY count + LIMIT
-- Customer with the most orders.
-- ---------------------------------------------------------------------
select customer_number
from Orders
group by customer_number
order by count(order_number) desc
limit 1;


-- ---------------------------------------------------------------------
-- 596. Classes With at Least 5 Students
-- Skill: HAVING
-- NOTE: "at least 5" => >= 5  (NOT > 5 — off-by-one trap)
-- ---------------------------------------------------------------------
select class
from Courses
group by class
having count(student) >= 5;


-- ---------------------------------------------------------------------
-- 619. Biggest Single Number
-- Skill: HAVING + derived table; MAX() returns NULL on empty set for free
-- Largest number appearing exactly once (NULL if none).
-- ---------------------------------------------------------------------
select MAX(num) as num
from (
    select num
    from MyNumbers
    group by num
    having count(num) < 2
) t;


-- ---------------------------------------------------------------------
-- 1075. Project Employees I
-- Skill: JOIN + AVG + ROUND
-- Average experience years per project, rounded to 2.
-- ---------------------------------------------------------------------
select p.project_id,
       ROUND(AVG(e.experience_years), 2) as average_years
from Project p
left join Employee e on p.employee_id = e.employee_id
group by p.project_id
order by project_id;


-- ---------------------------------------------------------------------
-- 1731. The Number of Employees Which Report to Each Employee
-- Skill: self-join + COUNT/AVG  (Day 2 #11)
-- m = manager, e = report. INNER join keeps only actual managers.
-- NOTE: reference solution — replace with your submitted version if it differs.
-- ---------------------------------------------------------------------
select m.employee_id,
       m.name,
       COUNT(e.employee_id) as reports_count,
       ROUND(AVG(e.age))    as average_age
from Employees m
join Employees e on e.reports_to = m.employee_id
group by m.employee_id, m.name
order by m.employee_id;


-- ---------------------------------------------------------------------
-- 1280. Students and Examinations
-- Skill: CROSS JOIN + LEFT JOIN + COUNT(col)  (Day 2 #12)
-- Every student x every subject; 0 when never sat.
-- COUNT(e.subject_name) not COUNT(*) so no-shows read 0, not 1.
-- ---------------------------------------------------------------------
select s.student_id, s.student_name, sub.subject_name,
       COUNT(e.subject_name) as attended_exams
from Students s
cross join Subjects sub
left join Examinations e
       on e.student_id   = s.student_id
      and e.subject_name = sub.subject_name
group by s.student_id, s.student_name, sub.subject_name
order by s.student_id, sub.subject_name;


-- ---------------------------------------------------------------------
-- 570. Managers with at Least 5 Direct Reports
-- Skill: self-join + HAVING  (Day 2 #13)
-- Group by m.id AND m.name (two managers could share a name).
-- NOTE: reference solution — replace with your submitted version if it differs.
-- ---------------------------------------------------------------------
select m.name
from Employee e
join Employee m on e.managerId = m.id
group by m.id, m.name
having count(*) >= 5;


-- ---------------------------------------------------------------------
-- 184. Department Highest Salary
-- Skill: JOIN + subquery per-group MAX  (Day 2 #16)
-- Row-value (departmentId, salary) IN (per-dept max) — keeps ties.
-- ---------------------------------------------------------------------
select d.name as Department, e.name as Employee, e.salary as Salary
from Employee e
left join Department d on e.departmentId = d.id
where (e.departmentId, e.salary) in (
    select departmentId, max(salary)
    from Employee
    group by departmentId
);


-- ---------------------------------------------------------------------
-- 512. Game Play Analysis II
-- Skill: JOIN to a per-player MIN derived table  (Day 2 #19)
-- Device each player first logged in with.
-- Derived table on the LEFT, Activity on the RIGHT — avoids RIGHT JOIN.
-- ---------------------------------------------------------------------
select b.player_id, a.device_id
from (
    select player_id, min(event_date) as min_date
    from Activity
    group by player_id
) b
left join Activity a
       on a.player_id  = b.player_id
      and a.event_date = b.min_date;