from tokens.token import Token


class Variable(Token):
    def __init__(self, representation):
        super().__init__(operands=0, precedence=0)
        self.representation = representation

    def apply(self, solutions):
        return solutions[self.representation]

    def __repr__(self):
        return self.representation
