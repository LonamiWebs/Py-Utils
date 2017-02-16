from tokens.token import Token
from tokens.variable import Variable


class Expression(Token):
    """Expressions should be grouped (more can be combined by combining expressions, e.g. (token -> expr)).
       Order of tokens is not taken into account, and results are undefined if relied upon."""

    def __init__(self):
        super().__init__(operands=0)
        self.tokens = []

    def add_token(self, token):
        self.tokens.append(token)

    def get_variables(self):
        variables = set()

        for t in self.tokens:
            if isinstance(t, Expression):
                variables |= t.get_variables()
            elif isinstance(t, Variable):
                variables.add(t.representation)

        return variables

    def apply(self, solutions):
        # Solutions is a dict containing variable: True/False
        for i in range(len(self.tokens)):
            ct = self.tokens[i]
            if ct.operands == 1:
                # Assume next token takes no operands or it would not be well formed…
                nt = self.tokens[i+1]
                return ct.apply(nt.apply(solutions))

            elif ct.operands == 2:
                # Assume previous and next tokens take no operands or it would not be well formed…
                pt = self.tokens[i-1]
                nt = self.tokens[i+1]
                return ct.apply(pt.apply(solutions), nt.apply(solutions))

        # This expression should only have 1 token or it would not be well-formed…
        return self.tokens[0].apply(solutions)

    @staticmethod
    def _binary_digit(decimal, index_from_right):
        # index_from_right is 0 based
        return (decimal >> index_from_right) & 1

    def find_solutions(self):
        variables = list(self.get_variables())
        variables.sort()

        solutions = []

        for i in range(2**len(variables)):
            solution = {}
            for j in range(len(variables)):
                # To follow the order of powers of two, one should start with the
                # highest (len(variables) - j - 1) and then go down, but since
                # order doesn't really matter, just use j as the index_from_right
                solution[variables[j]] = self._binary_digit(i, j)

            if self.apply(solution):
                solutions.append(solution)

        return solutions

    def __repr__(self):
        return '(' + ' '.join(repr(t) for t in self.tokens) + ')'
