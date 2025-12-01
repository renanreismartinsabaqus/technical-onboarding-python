import unittest


from math_utils import add, factorial

class TestMathUtils(unittest.TestCase):

    def test_add(self):
        """Test addition function."""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(1, 0), 0)
        self.assertEqual(add(1.5, 2.5), 4.0)


    def test_factorial_negative(self):
        """Test that factorial of negative number raises ValueError."""
        with self.assertRaises(ValueError):
            factorial(-1)

