from tokens.token import Token


class ConstantFalse(Token):
    representations = ['0']

    single_char_representation = '0'

    def __init__(self):
        super().__init__(operands=0, precedence=0)

    def apply(self, solutions):
        return False

    def __repr__(self):
        return '0'
