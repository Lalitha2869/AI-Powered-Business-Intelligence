from backend.pii_tokenizer import PIITokenizer
from backend.pii_resolver import PIIResolver


class SecurityManager:

    def __init__(self):

        self.tokenizer = PIITokenizer()
        self.resolver = PIIResolver()

    def tokenize(self, rows):

        return self.tokenizer.tokenize_results(rows)

    def resolve(self, rows):

        return self.resolver.resolve_results(rows)