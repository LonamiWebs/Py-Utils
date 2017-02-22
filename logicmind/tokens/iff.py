from tokens.token import Token


class Iff(Token):
    representations = ['<->', '↔', '⇔', '≡']

    single_char_representation = '↔'

    def __init__(self):
        super().__init__(operands=2, precedence=5)

    def apply(self, left, right):
        return left == right

    def __repr__(self):
        return '<->'
