from tokens.token import Token


class And(Token):
    def __init__(self):
        super().__init__(operands=2)

    def apply(self, left, right):
        return left and right

    def __repr__(self):
        return '^'
