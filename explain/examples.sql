-- простой запрос с соединением и фильтром
-- планировщик использует два вложенных цикла поиска Nested Loop
EXPLAIN ANALYZE
SELECT check_lists.*
FROM check_lists JOIN check_list_criteria_control_params ON check_lists.id = check_list_criteria_control_params.check_list_id
JOIN template_criteria_control_params ON check_list_criteria_control_params.template_control_param_id = template_criteria_control_params.id
WHERE template_criteria_control_params.remote_source_id = 3

-- Nested Loop  (cost=0.55..134.39 rows=5 width=103) (actual time=0.142..0.685 rows=153 loops=1)
--   ->  Nested Loop  (cost=0.28..132.69 rows=5 width=4) (actual time=0.135..0.373 rows=153 loops=1)
--         ->  Seq Scan on template_criteria_control_params  (cost=0.00..51.17 rows=2 width=4) (actual time=0.115..0.188 rows=2 loops=1)
--               Filter: (remote_source_id = 3)
--               Rows Removed by Filter: 733
--         ->  Index Only Scan using uq_check_list_criteria_control_params_check_list_id on check_list_criteria_control_params  (cost=0.28..40.71 rows=5 width=8) (actual time=0.019..0.081 rows=76 loops=2)
--               Index Cond: (template_control_param_id = template_criteria_control_params.id)
--               Heap Fetches: 128
--   ->  Index Scan using pk_check_lists on check_lists  (cost=0.28..0.34 rows=1 width=103) (actual time=0.002..0.002 rows=1 loops=153)
--         Index Cond: (id = check_list_criteria_control_params.check_list_id)
-- Planning Time: 20.661 ms
-- Execution Time: 0.728 ms

-- Seq Scan
-- последовательное сканирование дешевле, т.к. выбираем все строки

EXPLAIN ANALYZE
SELECT id FROM check_lists ORDER BY id desc

-- Index Only Scan Backward
-- выбираем часть индексных значений
-- нет узла сортировки т.к. индекс уже отсортирован

EXPLAIN ANALYZE
SELECT id, estimate FROM check_lists where id IN (895, 150) ORDER BY id asc

-- Bitmap, Sort
-- к индексу добавили неиндексируемое поле

EXPLAIN ANALYZE
SELECT id, estimate FROM check_lists where id IN (895, 150) ORDER BY id asc

-- Bitmap, Sort
-- план не изменился т.к. вложенный запрос раскрылся в родительский
EXPLAIN ANALYZE
SELECT id, estimate FROM (SELECT * from check_lists where id IN (895, 150)) t1

-- Hash Join
-- планировщик готовит хэш для t2,
-- далее последовательным сканированием ищет ключи t1 в хэше t2

EXPLAIN ANALYZE
SELECT * FROM
(SELECT id from check_lists) t1 JOIN
(SELECT id from check_lists) t2 ON t1.id=t2.id

-- Merge Join
-- Максимально упростили задачу планировщику, т.к. выбираем только индексные
-- поля и ограничили их условием.
-- Сортировка добавлена для демонстрации того, что она не добавляет узлов Sort,
-- т.к. индекс уже отсортирован
-- Если не ограничивать условием IN (895, 150), то будет использован последовательный поиск.
-- При добавлении полей не в индексе, план запроса добавит Bitmap Heap Scan.
-- Если добавить разную сортировку asc, desc - Merge Join земанится на Nested Loop.

EXPLAIN ANALYZE
SELECT t2.id FROM
(SELECT id  from check_lists where check_lists.id IN (895, 150) ORDER by id) t1 JOIN
(SELECT id from check_lists where check_lists.id IN (895, 150) ORDER by id) t2 ON t1.id=t2.id