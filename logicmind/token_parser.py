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

        # Get all operators so we can iterate over them
        operators = [Not, Then, Iff, Or, And]

        # Find all the representations on the string and add surrounding spaces,
        # this will allow us to call 'string.split()' to separate variable names
        # from the operators so the user doesn't need to enter them separated
        for operator in operators:
            for representation in operator.representations:
                string = string.replace(representation, ' '+representation+' ')

        # Get all the tokens
        words = string.split()

        # Store the found nested expressions on the stack
        expressions_stack = [Expression()]
        for w in words:
            done = False
            for operator in operators:
                if w in operator.representations:
                    expressions_stack[-1].add_token(operator())
                    done = True
                    break

            if done:
                pass
            elif w == '(':
                expressions_stack.append(Expression())
            elif w == ')':
                e = expressions_stack.pop()
                expressions_stack[-1].add_token(e)

            else:
                expressions_stack[-1].add_token(Variable(w))

        # Tokenize the top expression (this will also tokenize its children)
        expressions_stack[0].tokenize()

        # Return the top expression once it's completely valid
        return expressions_stack[0]
