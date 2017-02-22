from tokens.andd import And
from tokens.expression import Expression
from tokens.iff import Iff
from tokens.kfalse import ConstantFalse
from tokens.ktrue import ConstantTrue
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
        #
        # Note that the order here is important. We first need to replace long
        # expressions, such as '<->' with their single character representations.
        #
        # If we didn't do this, after we tried to separate the tokens from other
        # expressions by adding spaces on both sides of the operator, '->' would
        # break '<->' turning it into '< ->', which would not be recognised.
        #
        # We add spaces between the tokens so it's easy to split them and identify them.
        # Another way would be to iterate over the string and finding the tokens. Once
        # identified, they'd be put, in order, on a different list. However, this is
        # not as simple as the currently used approach.
        operators = [Iff, Then, Not, Or, And, ConstantTrue, ConstantFalse]

        # Find all the representations on the string and add surrounding spaces,
        # this will allow us to call 'string.split()' to separate variable names
        # from the operators so the user doesn't need to enter them separated
        for operator in operators:
            for representation in operator.representations:
                string = string.replace(representation, ' '+operator.single_char_representation+' ')

        # Get all the tokens
        words = string.split()

        # Store the found nested expressions on the stack
        expressions_stack = [Expression()]
        for w in words:
            done = False
            for operator in operators:
                # We replaced all the operator with their single character representations. We
                # don't need to check whether the current word (representation) is any of the
                # available representations for this operator, since it's the single-character one.
                if w == operator.single_char_representation:
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
