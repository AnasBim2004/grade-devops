import unittest
from app import average, result

class TestGrades(unittest.TestCase):

    def test_average(self):
        self.assertAlmostEqual(average([10, 11, 12, 13, 14, 15, 9]), 12.0)

    def test_pass_threshold(self):
        self.assertEqual(result(10), "Passed")
        self.assertEqual(result(9.99), "Not passed")

    def test_invalid_grade(self):
        with self.assertRaises(ValueError):
            average([1, 2, 3, 4, 5, 6, 21])

    def test_exactly_seven_grades(self):
        with self.assertRaises(ValueError):
            average([10, 10])

if __name__ == "__main__":
    unittest.main()