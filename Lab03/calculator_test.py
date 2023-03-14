import unittest
import math
from calculator import Calculator


class CalculatorTest(unittest.TestCase):

    def test_add(self):
        test_cases = [(1, 2), (0, 0), (-1, -1), (1.5, 2.5), (999999999, 1)]
        for x, y in test_cases:
            with self.subTest(x=x, y=y):
                self.assertEqual(Calculator.add(x, y), x+y)
        with self.assertRaises(TypeError):
            Calculator.add(1, '2')

    def test_divide(self):
        test_cases = [(1, 2), (0, 2), (-1, -1), (1.5, 2.5), (999999999, 1)]
        for x, y in test_cases:
            with self.subTest(x=x, y=y):
                self.assertEqual(Calculator.divide(x, y), x/y)
        with self.assertRaises(ZeroDivisionError):
            Calculator.divide(1, 0)

    def test_sqrt(self):
        test_cases = [ 0, 1, 4, 2.25, 999999999]
        for x in test_cases:
            with self.subTest(x=x):
                self.assertEqual(Calculator.sqrt(x), math.sqrt(x))
        with self.assertRaises(ValueError):
            Calculator.sqrt(-1)

    def test_exp(self):
        test_cases = [ 0, 1, 2, -1, 10]
        for x in test_cases:
            with self.subTest(x=x):
                self.assertEqual(Calculator.exp(x), math.exp(x))
        with self.assertRaises(TypeError):
            Calculator.exp('2')
if __name__ == '__main__':
    unittest.main()
