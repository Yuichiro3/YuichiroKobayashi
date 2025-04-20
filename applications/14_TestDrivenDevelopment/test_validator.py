import unittest
from validator import validate_input

class TestInputValidation(unittest.TestCase):

    def test_valid_input(self):
        # Test a correctly-sized list
        data = [0.1, 0.2, 0.7]
        result = validate_input(data, 3)
        self.assertTrue(result)

    def test_wrong_length(self):
        # Test list with wrong length
        data = [0.1, 0.2]
        with self.assertRaises(ValueError):
            validate_input(data, 3)

    def test_wrong_type(self):
        # Test when input is not a list
        data = "not a list"
        with self.assertRaises(TypeError):
            validate_input(data, 3)

    def test_exact_output(self):
        # Ensure return value is exactly True
        self.assertEqual(validate_input([1, 2, 3], 3), True)

if __name__ == "__main__":
    unittest.main()
