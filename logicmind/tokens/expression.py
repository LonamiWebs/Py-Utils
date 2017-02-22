from tokens.token import Token
from tokens.variable import Variable


class Expression(Token):
    """Expressions should be grouped (more can be combined by combining expressions, e.g. (token -> expr)).
       Order of tokens is not taken into account, and results are undefined if relied upon."""

    def __init__(self):
        super().__init__(operands=0, precedence=0)
        self.tokens = []

    def add_token(self, token):
        self.tokens.append(token)

    def tokenize(self):
        # Tokenize the expression to be valid, for example, converts:
        #   (variable operator operator variable)
        # to
        #   (variable operator (operator variable))
        #
        # Another possible solution would be to apply the operators in order
        # once we're solving the expression, however, this would provide no
        # insight to the user on the real order that it's being applied.
        #
        # First check whether it's already valid or not (count operators, there must be one)
        # Store the index and their precedence as a tuple (index, precedence)
        operators_at = []
        for i in range(len(self.tokens)):
            if self.tokens[i].operands > 0:
                operators_at.append((i, self.tokens[i].precedence))

        # There is only one operator (or none at all), there is no trouble
        if len(operators_at) < 2:
            # However, we need to make sure that the inner expressions are also valid
            for t in self.tokens:
                if isinstance(t, Expression):
                    t.tokenize()

            # Early terminate, this one is valid
            return

        # Find the one with the lowest precedence and tokenize it, one at a time
        lowest_at = min(operators_at, key=lambda t: t[1])[0]

        # Find the starting token index that will be grouped (one behind if it takes 2 operators)
        # And also how many tokens we'll be replacing (3 if it takes 2 operators, 'left op right')
        # For example:
        #   'q ^ p -> ¬p' it would choose at '¬' and take 2 tokens (end + 2)
        #   'q ^ p ->  p' it would choose at '^' and take 3 tokens (start -1, before the operator, end + 2)
        if self.tokens[lowest_at].operands == 2:
            start = lowest_at - 1
            end = start + 3
        else:
            start = lowest_at
            end = start + 2

        # Add the involved tokens to the grouped expression
        group = Expression()
        for t in self.tokens[start:end]:
            group.add_token(t)

        # Replace these with the new grouped expression
        self.tokens[start:end] = [group]

        # Repeat until the expression is valid and there is no need to tokenize more
        self.tokenize()

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
