import uuid


class TokenManager:

    def __init__(self):

        self.active_tokens = {}

    def generate_token(
        self,
        username,
        role
    ):

        token = str(
            uuid.uuid4()
        )

        self.active_tokens[token] = {
            "username": username,
            "role": role
        }

        return token

    def validate_token(
        self,
        token
    ):

        if token not in self.active_tokens:

            raise Exception(
                "Authentication required"
            )

        return self.active_tokens[token]