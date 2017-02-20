from tokens.token import Token


class Then(Token):
    representations = ['->', '→']

    def __init__(self):
        super().__init__(operands=2)

    def apply(self, left, right):
        return not left or right

    def __repr__(self):
        return '->'
