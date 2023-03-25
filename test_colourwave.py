import unittest
from colourwave import colourwave_role
from time import sleep
from neopixel import Neopixel

class TestColourWave(unittest.TestCase):

    def setUp(self):
        global sleep
        global Neopixel

        self.original_sleep = sleep
        self.original_neopixel = Neopixel

        # Mock time.sleep to avoid waiting during testing
        sleep = lambda x: None

        # Mock the Neopixel class to avoid hardware interactions
        class MockNeopixel:
            def __init__(self, *args, **kwargs):
                pass

            def brightness(self, value):
                pass

            def set_pixel_line_gradient(self, *args, **kwargs):
                pass

            def rotate_right(self, steps):
                pass

            def show(self):
                pass

        Neopixel = MockNeopixel

    def tearDown(self):
        sleep = self.original_sleep
        Neopixel = self.original_neopixel

    def test_colourwave_role(self):
        try:
            colourwave_role()
        except Exception as e:
            self.fail(f"Exception occurred during test: {e}")

if __name__ == '__main__':
    unittest.main()
