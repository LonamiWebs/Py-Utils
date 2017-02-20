from tokens.token import Token


class Or(Token):
    representations = ['v', '∨']

    def __init__(self):
        super().__init__(operands=2, precedence=3)

    def apply(self, left, right):
        return left or right

    def __repr__(self):
        return 'v'
