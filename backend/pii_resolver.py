from security.token_store import TOKEN_STORE


class PIIResolver:

    def resolve_results(self, rows):

        for row in rows:

            for column in row.keys():

                value = row[column]

                if value in TOKEN_STORE:

                    row[column] = TOKEN_STORE[value]

        return rows