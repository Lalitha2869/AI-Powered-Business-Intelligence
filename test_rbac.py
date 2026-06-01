from backend.rbac_manager import RBACManager

rbac = RBACManager()

sql = """
SELECT * FROM sales
"""

rbac.validate_tables(
    sql,
    "sales_manager"
)

print("Allowed")