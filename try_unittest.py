import unittest

def add(a, b):
    return a+b

def minus(a, b):
    return a-b

class TestDemo(unittest.TestCase):
    """Test mathfuc.py"""

    @classmethod
    def setUpClass(cls):
        print ("this setupclass() method only called once.\n")

    @classmethod
    def tearDownClass(cls):
        print ("this teardownclass() method only called once too.\n")

    def setUp(self):
        print ("do something before test : prepare environment.\n")

    def tearDown(self):
        print ("do something after test : clean up.\n")

    def test_add(self):
        """Test method add(a, b)"""
        print("test add 1+2=3")
        self.assertEqual(3, add(1, 2))
        print("test add 2+2!=3")
        self.assertNotEqual(3, add(2, 2))

    def test_minus(self):
        """Test method minus(a, b)"""
        print("test add 3-2=1")
        self.assertEqual(1, minus(3, 2))
        print("test add 3-2 != 1")
        self.assertNotEqual(1, minus(3, 2))

    @unittest.skip("do't run as not ready")
    def test_minus_with_skip(self):
        """Test method minus(a, b)"""
        self.assertEqual(1, minus(3, 2))
        self.assertNotEqual(1, minus(3, 2))

#test also can be launched by cmd: python -m  unittest try_unittest.TestDemo.test_add
if __name__ == '__main__':
    # verbosity=*：默认是1；设为0，则不输出每一个用例的执行结果；2-输出详细的执行结果
    unittest.main(verbosity=1)