from tokens.token import Token


class Or(Token):
    def __init__(self):
        super().__init__(operands=2)

    def apply(self, left, right):
        return left or right

    def __repr__(self):
        return 'v'
