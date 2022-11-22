import os

def plus(a, b):
    return a + b

def minus(a, b):
    return a - b


def testplus():
    assert plus(1, 2) == 3, "ERRORED"



class TestMinus(object):

    def minus_test():
        assert minus(3, 1) == 2, "ERRORED"

class Test_Minus(object):

    def test_minus():
        assert minus(3, 1) == 2, "ERRORED"



class TestPlus(object):

    def __init__(self):
        pass

    def test_plus(self):
        assert plus(1, 2) == 3, "ERRORED"



class Math(object):

    def test_plus():
        assert plus(1, 2) == 3, "ERRORED"

