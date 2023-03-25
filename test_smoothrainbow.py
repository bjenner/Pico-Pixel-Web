import unittest
from unittest.mock import Mock, call
from rainbow import rainbow_role

class TestRainbowRole(unittest.TestCase):

    def test_rainbow_role(self):
        # Mock the Neopixel class
        neopixel_mock = Mock()
        
        # Replace Neopixel import in rainbow module with the mock
        rainbow.Neopixel = neopixel_mock

        # Limit the number of iterations for the test
        rainbow.iterations_limit = 10

        # Run the rainbow_role function
        rainbow_role()

        # Check if the Neopixel class was instantiated
        neopixel_mock.assert_called_once_with(50, 0, 28, "GRB")

        # Check if the fill and show methods were called the expected number of times
        neopixel_instance = neopixel_mock.return_value
        self.assertEqual(neopixel_instance.fill.call_count, rainbow.iterations_limit)
        self.assertEqual(neopixel_instance.show.call_count, rainbow.iterations_limit)

        # Check if the hue value was incremented by 150 on each iteration
        hue_values = [call.args[0] for call in neopixel_instance.colorHSV.call_args_list]
        expected_hue_values = list(range(0, 150 * rainbow.iterations_limit, 150))
        self.assertEqual(hue_values, expected_hue_values)

if __name__ == '__main__':
    unittest.main()
