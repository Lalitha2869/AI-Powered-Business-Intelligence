from security.token_store import TOKEN_STORE
from security.pii_rules import PII_COLUMNS


class PIITokenizer:

    def __init__(self):

        self.customer_counter = 1
        self.email_counter = 1
        self.phone_counter = 1
        self.employee_counter = 1

    def generate_token(self, column):

        if column == "customer_name":

            token = f"CUST_{self.customer_counter:03}"
            self.customer_counter += 1

        elif column == "email":

            token = f"EMAIL_{self.email_counter:03}"
            self.email_counter += 1

        elif column == "phone":

            token = f"PHONE_{self.phone_counter:03}"
            self.phone_counter += 1

        elif column == "employee_name":

            token = f"EMP_{self.employee_counter:03}"
            self.employee_counter += 1

        else:

            token = "UNKNOWN_VALUE"

        return token

    def tokenize_results(self, rows):

        for row in rows:

            for column in row.keys():

                if column in PII_COLUMNS:

                    original_value = row[column]

                    if original_value is None:
                        continue

                    existing_token = None

                    for token, value in TOKEN_STORE.items():

                        if value == original_value:

                            existing_token = token
                            break

                    if existing_token:

                        row[column] = existing_token

                    else:

                        token = self.generate_token(column)

                        TOKEN_STORE[token] = original_value

                        row[column] = token

        return rows