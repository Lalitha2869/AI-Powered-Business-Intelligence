from sqlalchemy import inspect
from backend.database import engine


def get_schema_context():

    inspector = inspect(engine)

    schema_text = ""

    tables = inspector.get_table_names()

    for table in tables:

        schema_text += f"\nTable: {table}\n"

        columns = inspector.get_columns(table)

        for column in columns:

            schema_text += f"- {column['name']}\n"

    return schema_text