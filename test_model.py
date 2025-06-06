
import unittest
from model import Resource

class TestResource(unittest.TestCase):
    def test_valid_resource(self):
        r = Resource("Нефть", "2025.06.01", 123.45, "ежемесячно", True)
        self.assertEqual(r.name, "Нефть")
        self.assertEqual(r.date.year, 2025)
        self.assertTrue(r.status)

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            Resource("Нефть", "2025.13.01", 123.45, "ежемесячно", True)

    def test_invalid_frequency(self):
        with self.assertRaises(ValueError):
            Resource("Нефть", "2025.06.01", 123.45, "непонятно", True)

    def test_invalid_status(self):
        with self.assertRaises(ValueError):
            Resource("Нефть", "2025.06.01", 123.45, "ежемесячно", "да")

if __name__ == "__main__":
    unittest.main()
