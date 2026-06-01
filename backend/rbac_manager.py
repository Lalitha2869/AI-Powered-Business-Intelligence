from security.role_permissions import ROLE_PERMISSIONS


class RBACManager:

    def validate_tables(
        self,
        sql,
        role
    ):

        sql_lower = sql.lower()

        allowed_tables = ROLE_PERMISSIONS.get(
            role,
            []
        )

        if "*" in allowed_tables:
            return True

        tables_found = []

        for table in [
            "sales",
            "customers",
            "products",
            "regions",
            "employees",
            "attendance",
            "departments",
            "expenses",
            "budgets",
            "payroll",
            "invoices"
        ]:

            if table in sql_lower:
                tables_found.append(table)

        for table in tables_found:

            if table not in allowed_tables:

                raise Exception(
                    f"Access denied: {role} cannot access table {table}"
                )

        return True