#----------------------------------------
#              Helpers
#----------------------------------------

def unsupported(operator, a, b):
    """
    Raises a standard TypeError of operation @operation
    between variables @a and @b.
    """
    raise TypeError("unsupported operand type(s) for {}: '{}' and '{}'".format(
        operator,
        type(a),
        type(b)))