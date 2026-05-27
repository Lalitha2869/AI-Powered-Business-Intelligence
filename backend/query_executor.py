import pandas as pd

from sqlalchemy import text

from backend.database import engine


def execute_query(sql: str):

    with engine.connect() as connection:

        result = connection.execute(
            text(sql)
        )

        rows = result.fetchall()

        columns = result.keys()

        dataframe = pd.DataFrame(
            rows,
            columns=columns
        )

        return dataframe