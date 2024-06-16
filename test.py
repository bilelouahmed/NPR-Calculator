from main import calculator
import unittest
import math


class TestCalculator(unittest.TestCase):
    def test_addition(self):
        result, classic_expression = calculator("3 4 +")
        self.assertEqual(result, 7)
        self.assertEqual(classic_expression, "(3 + 4)")

    def test_complex_expression(self):
        result, classic_expression = calculator("10 2 8 * + 3 -")
        self.assertEqual(result, 23)
        self.assertEqual(classic_expression, "((10 + (2 * 8)) - 3)")

    def test_trigonometric_sin(self):
        result, classic_expression = calculator("9 sin")
        self.assertAlmostEqual(result, math.sin(9))
        self.assertEqual(classic_expression, "sin(9)")

    def test_exponentiation(self):
        result, classic_expression = calculator("3 2 ^")
        self.assertEqual(result, 9)
        self.assertEqual(classic_expression, "(3 ^ 2)")

    def test_multiple_operations(self):
        result, classic_expression = calculator("4 2 ^ 3 + 2 *")
        self.assertEqual(result, 38)
        self.assertEqual(classic_expression, "(((4 ^ 2) + 3) * 2)")

    def test_exponentiation_addition(self):
        result, classic_expression = calculator("2 3 ^ 2 3 ^ +")
        self.assertEqual(result, 16)
        self.assertEqual(classic_expression, "((2 ^ 3) + (2 ^ 3))")

    def test_exponential_function(self):
        result, classic_expression = calculator("4 exp")
        self.assertAlmostEqual(result, math.exp(4))
        self.assertEqual(classic_expression, "exp(4)")

    def test_invalid_expression(self):
        with self.assertRaises(ValueError):
            calculator("4 2 + +")

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculator("4 0 /")


if __name__ == "__main__":
    unittest.main()
