import argparse


class ValuesInBetweenAction(object):
    a = None
    b = None

    def __init__(self, a=0, b=100):
        self.a = a
        self.b = b

    def __call__(self, value):
        forced_int_value = int(value)
        if forced_int_value < self.a or forced_int_value > self.b:
            raise argparse.ArgumentTypeError('{} is not a value between {} and {}'.format(value, self.a, self.b))

        return forced_int_value
