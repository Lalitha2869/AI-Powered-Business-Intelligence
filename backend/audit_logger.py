from backend.database import get_connection


class AuditLogger:

    def log(
        self,
        username,
        question,
        generated_sql,
        execution_time_ms,
        status="SUCCESS"
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO audit_logs
            (
                username,
                user_query,
                generated_sql,
                execution_time_ms,
                status
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                username,
                question,
                generated_sql,
                execution_time_ms,
                status
            )
        )

        conn.commit()

        cursor.close()
        conn.close()