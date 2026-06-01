class MemoryManager:

    def __init__(self):
        self.last_question = None
        self.last_sql = None
        self.last_rows = None

    def save_context(
        self,
        question,
        sql,
        rows
    ):
        self.last_question = question
        self.last_sql = sql
        self.last_rows = rows

    def get_context(self):

        return {
            "last_question": self.last_question,
            "last_sql": self.last_sql,
            "last_rows": self.last_rows
        }