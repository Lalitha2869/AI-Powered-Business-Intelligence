from backend.database import get_connection


class AuthManager:

    def authenticate(
        self,
        username,
        password
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT role
            FROM users
            WHERE username = %s
            AND password = %s
            """,
            (
                username,
                password
            )
        )

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:

            raise Exception(
                "Invalid username or password"
            )

        return {
            "username": username,
            "role": row[0]
        }