from tokens.token import Token


class Not(Token):
    representations = ['¬', '!']

    single_char_representation = '¬'

    def __init__(self):
        super().__init__(operands=1, precedence=1)

    def apply(self, right):
        return not right

    def __repr__(self):
        return '¬'
