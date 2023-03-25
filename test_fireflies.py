import unittest
from fireflies import firefly_step
import time
from neopixel import Neopixel

class TestFireflies(unittest.TestCase):

    def setUp(self):
        global time
        global Neopixel
        
        self.original_time_sleep = time.sleep
        self.original_neopixel = Neopixel

        # Mock time.sleep to avoid waiting during testing
        time.sleep = lambda x: None

        # Mock the Neopixel class to avoid hardware interactions
        class MockNeopixel:
            def __init__(self, *args, **kwargs):
                pass

            def fill(self, color):
                pass

            def show(self):
                pass

            def set_pixel(self, index, color):
                pass

        Neopixel = MockNeopixel

    def tearDown(self):
        global time
        global Neopixel

        time.sleep = self.original_time_sleep
        Neopixel = self.original_neopixel

    def test_firefly_step(self):
        try:
            firefly_step()
        except Exception as e:
            self.fail(f"Exception occurred during test: {e}")

if __name__ == '__main__':
    unittest.main()
