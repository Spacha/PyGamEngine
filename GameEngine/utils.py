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

#----------------------------------------
#            Utility classes
#----------------------------------------

class PerfTimer:
    def __init__(self):
        self.started_at = 0.0
    def reset(self):
        self.started_at = time.time()
    def get_time(self):
        return time.time() - self.started_at
    def get_time_string(self):
        dt = get_time()
        # TODO

class Colors:
    BLACK   = ( 0 , 0 , 0 )
    WHITE   = (255,255,255)
    GREY    = (100,100,100)
    RED     = (255, 0 , 0 )
    GREEN   = ( 0 ,255, 0 )
    BLUE    = ( 0 , 0 ,255)
    YELLOW  = (255,255, 0 )
    SANDY   = (255,221, 93)
