CONSTRAINTS = """
Query Construction Constraints

1. Use PostgreSQL syntax only.
2. Use explicit JOIN clauses.
3. Prefer INNER JOIN when applicable.
4. Avoid CROSS JOIN.
5. Avoid SELECT *.
6. Select only required columns.
7. Use aliases for readability.
8. Use aggregation when business metrics are requested.
9. Use GROUP BY appropriately.
10. Use ORDER BY when ranking is requested.
11. Include LIMIT 100 for non-aggregated results.
12. Return performant queries.
13. Avoid unnecessary subqueries.
14. Prefer indexed columns when filtering.
"""