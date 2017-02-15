class Token:
    def __init__(self, operands):
        # If operands = 0, it takes no operands, method should be apply(dict: solutions)
        # If operands = 1, it takes one operand, method should be apply(bool: rightExpr)
        # If operands = 2, it takes two operands, method should be apply(bool: leftExpr, bool: rightExpr)
        self.operands = operands
