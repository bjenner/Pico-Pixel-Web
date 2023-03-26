import unittest
from picostatus import PicoStatus

class TestPicoStatus(unittest.TestCase):

    def test_temperature(self):
        # Test temperature method
        temp_c = PicoStatus.temperature()
        self.assertIsNotNone(temp_c)
        self.assertTrue(-40 <= temp_c <= 80)

    def test_memory(self):
        # Test memory method
        mem = PicoStatus.memory()
        self.assertIsNotNone(mem)
        self.assertTrue(mem > 0)

if __name__ == '__main__':
    unittest.main()
