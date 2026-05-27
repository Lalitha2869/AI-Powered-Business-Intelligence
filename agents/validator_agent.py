import sqlglot

from sqlglot.expressions import Select

from security.allowed_tables import ALLOWED_TABLES
from security.blocked_keywords import BLOCKED_KEYWORDS
from security.blocked_columns import BLOCKED_COLUMNS

def validate_keywords(sql: str):

    sql_upper = sql.upper()

    for keyword in BLOCKED_KEYWORDS:

        if keyword in sql_upper:

            raise Exception(
                f"Blocked SQL keyword detected: {keyword}"
            )

    return True

def validate_sql_syntax(sql: str):

    try:

        parsed = sqlglot.parse_one(sql)

        return parsed

    except Exception as e:

        raise Exception(
            f"Invalid SQL: {str(e)}"
        )
    

def validate_select_only(parsed):

    if not isinstance(parsed, Select):

        raise Exception(
            "Only SELECT queries are allowed"
        )

    return True

def validate_tables(parsed):

    tables = []

    for table in parsed.find_all(
        sqlglot.expressions.Table
    ):

        tables.append(table.name)

    for table in tables:

        if table not in ALLOWED_TABLES:

            raise Exception(
                f"Unauthorized table detected: {table}"
            )

    return True

def validate_columns(parsed):

    for column in parsed.find_all(
        sqlglot.expressions.Column
    ):

        if column.name in BLOCKED_COLUMNS:

            raise Exception(
                f"Restricted column accessed: {column.name}"
            )

    return True

def enforce_limit(sql: str):

    sql = sql.strip()

    if sql.endswith(";"):
        sql = sql[:-1]

    if "LIMIT" not in sql.upper():
        sql += " LIMIT 100"

    return sql

def validate_sql(sql: str):

    validate_keywords(sql)

    parsed = validate_sql_syntax(sql)

    validate_select_only(parsed)

    validate_tables(parsed)

    validate_columns(parsed)

    validated_sql = enforce_limit(sql)

    return validated_sql