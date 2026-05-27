EXAMPLES = """
Question:
Show total revenue by region

SQL:
SELECT
    r.region_name,
    SUM(s.revenue) AS total_revenue
FROM sales s
JOIN regions r
ON s.region_id = r.region_id
GROUP BY r.region_name;

Question:
Show employee count by department

SQL:
SELECT
    d.department_name,
    COUNT(e.employee_id)
FROM employees e
JOIN departments d
ON e.department_id = d.department_id
GROUP BY d.department_name;

Question:
Show department expenses

SQL:
SELECT
    d.department_name,
    SUM(ex.amount)
FROM expenses ex
JOIN departments d
ON ex.department_id = d.department_id
GROUP BY d.department_name;


Question:
Show budget allocation by department

SQL:
SELECT
d.department_name,
b.allocated_budget
FROM budgets b
JOIN departments d
ON b.department_id=d.department_id;


Question:
Show products below reorder level

SQL:
SELECT
p.product_name,
i.stock_quantity,
i.reorder_level
FROM inventory i
JOIN products p
ON i.product_id=p.product_id
WHERE i.stock_quantity < i.reorder_level;
"""