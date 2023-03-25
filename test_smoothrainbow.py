import unittest
import rainbow
from neopixel import Neopixel

class TestRainbowRole(unittest.TestCase):
    def setUp(self):
        # Save the original Neopixel class and replace it with our custom class
        self.original_neopixel = rainbow.Neopixel
        rainbow.Neopixel = self.CustomNeopixel

    def tearDown(self):
        # Restore the original Neopixel class
        rainbow.Neopixel = self.original_neopixel

    class CustomNeopixel(Neopixel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fill_calls = []
            self.show_calls = 0

        def fill(self, color):
            self.fill_calls.append(color)

        def show(self):
            self.show_calls += 1

    def test_rainbow_role(self):
        # Limit the number of iterations for the test
        rainbow.iterations_limit = 10

        # Run the rainbow_role function
        rainbow.rainbow_role()

        # Instantiate the expected Neopixel instance
        expected_neopixel = self.CustomNeopixel(50, 0, 28, "GRB")

        # Check if the fill and show methods were called the expected number of times
        self.assertEqual(len(expected_neopixel.fill_calls), rainbow.iterations_limit)
        self.assertEqual(expected_neopixel.show_calls, rainbow.iterations_limit)

        # Check if the hue value was incremented by 150 on each iteration
        hue_values = [call[0] for call in expected_neopixel.fill_calls]
        expected_hue_values = list(range(0, 150 * rainbow.iterations_limit, 150))
        self.assertEqual(hue_values, expected_hue_values)

if __name__ == '__main__':
    unittest.main()
