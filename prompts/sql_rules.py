SQL_RULES = """
SQL Generation Rules

Revenue Requests:
→ SUM(revenue)

Sales Trends:
→ GROUP BY sale_date

Regional Analysis:
→ JOIN regions

Employee Analysis:
→ JOIN departments

Attendance Reports:
→ Use attendance table

Budget Analysis:
→ Compare budgets and expenses

Inventory Reports:
→ inventory table

Supplier Analysis:
→ suppliers and shipments

Ranking Requests:
→ ORDER BY DESC

Top N Requests:
→ LIMIT N

Bottom N Requests:
→ ORDER BY ASC LIMIT N
"""