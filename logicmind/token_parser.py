from tokens.andd import And
from tokens.expression import Expression
from tokens.iff import Iff
from tokens.nop import Not
from tokens.orr import Or
from tokens.then import Then
from tokens.variable import Variable


class TokenParser:
    """This parser only works with atomic expressions,
       so parenthesis are needed everywhere to group items"""

    @staticmethod
    def parse_expression(string):
        # Separate parenthesis so they're new tokens
        # Also convert [ or { to the same parenthesis (
        for s in '([{':
            string = string.replace(s, ' ( ')

        for s in ')]}':
            string = string.replace(s, ' ) ')

        # Get all the tokens
        words = string.split()

        expressions_stack = [Expression()]

        for w in words:
            if w == '(':
                expressions_stack.append(Expression())
            elif w == ')':
                e = expressions_stack.pop()
                expressions_stack[-1].add_token(e)

            elif w == '¬':
                expressions_stack[-1].add_token(Not())
            elif w == '->':
                expressions_stack[-1].add_token(Then())
            elif w == '<->':
                expressions_stack[-1].add_token(Iff())
            elif w == 'v':
                expressions_stack[-1].add_token(Or())
            elif w == '^':
                expressions_stack[-1].add_token(And())

            else:
                expressions_stack[-1].add_token(Variable(w))

        return expressions_stack[0]
