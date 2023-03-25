import unittest
from indicator import Flash
from machine import Timer
from time import sleep

class TestIndicator(unittest.TestCase):

    def test_led_on_off(self):
        Flash.led_on()
        self.assertTrue(Flash.intled.value())

        Flash.led_off()
        self.assertFalse(Flash.intled.value())

    def test_start_stop_flash(self):
        Flash.start_flash()
        self.assertTrue(isinstance(Flash.tim, Timer))

        Flash.stop_flash()
        self.assertFalse(Flash.intled.value())

    def test_add_flash(self):
        initial_flashes = Flash.get_flash()
        Flash.add_flash()
        self.assertEqual(Flash.get_flash(), initial_flashes + 1)

    def test_tick(self):
        Flash.start_flash()
        initial_count = Flash.count
        Flash.tick(None)
        self.assertEqual(Flash.count, initial_count - 1)

if __name__ == '__main__':
    unittest.main()
