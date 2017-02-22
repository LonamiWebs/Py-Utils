from tokens.token import Token


class ConstantTrue(Token):
    representations = ['1']

    single_char_representation = '1'

    def __init__(self):
        super().__init__(operands=0, precedence=0)

    def apply(self, solutions):
        return True

    def __repr__(self):
        return '1'
