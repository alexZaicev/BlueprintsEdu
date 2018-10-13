import unittest
from context import *

class TestMain(unittest.TestCase):
    def test_func(self):
        sum = fun(5, 2)
        self.assertEqual(7, sum)

if __name__ == "__main__":
    unittest.main()
