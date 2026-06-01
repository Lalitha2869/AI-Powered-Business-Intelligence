from backend.database import get_connection


class AnalyticsManager:

    def get_summary(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM audit_logs
        """)
        total_queries = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM audit_logs
            WHERE status = 'SUCCESS'
        """)
        successful_queries = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM audit_logs
            WHERE status = 'FAILED'
        """)
        failed_queries = cursor.fetchone()[0]

        cursor.execute("""
            SELECT AVG(execution_time_ms)
            FROM audit_logs
        """)
        avg_execution_time = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return {
            "total_queries": total_queries,
            "successful_queries": successful_queries,
            "failed_queries": failed_queries,
            "avg_execution_time_ms": round(
                float(avg_execution_time or 0),
                2
            )
        }

    def get_advanced_summary(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                user_query,
                COUNT(*) AS frequency
            FROM audit_logs
            GROUP BY user_query
            ORDER BY frequency DESC
            LIMIT 5
        """)

        top_questions = []

        for row in cursor.fetchall():
            top_questions.append({
                "question": row[0],
                "count": row[1]
            })

        cursor.execute("""
            SELECT MIN(execution_time_ms)
            FROM audit_logs
        """)
        fastest_query = cursor.fetchone()[0]

        cursor.execute("""
            SELECT MAX(execution_time_ms)
            FROM audit_logs
        """)
        slowest_query = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return {
            "top_questions": top_questions,
            "fastest_query_ms": fastest_query,
            "slowest_query_ms": slowest_query
        }