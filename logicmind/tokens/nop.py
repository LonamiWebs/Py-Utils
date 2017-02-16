from tokens.token import Token


class Not(Token):
    def __init__(self):
        super().__init__(operands=1)

    def apply(self, right):
        return not right

    def __repr__(self):
        return '¬'
