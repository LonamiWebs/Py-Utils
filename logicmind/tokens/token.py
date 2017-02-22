class Token:
    # Static variable holding all the representations for a given token
    representations = []

    # Static variable holding a possible representation making use of only 1 character
    # We need these to make it easy to tokenize a given string. For example, to separate:
    #   'p<->(q->p)', if we replaced '->' with ' -> ', it would become 'p< -> (q -> p)'
    # For this reason, by using a single character, we avoid this problem
    single_char_representation = None

    def __init__(self, operands, precedence):
        # If operands = 0, it takes no operands, method should be apply(dict: solutions)
        # If operands = 1, it takes one operand, method should be apply(bool: rightExpr)
        # If operands = 2, it takes two operands, method should be apply(bool: leftExpr, bool: rightExpr)
        self.operands = operands

        # The precendence (order) in which operators are applied
        # The lower this number is, the sooner it will be applied
        self.precedence = precedence
