import unittest
from controls import Flag

class TestControls(unittest.TestCase):
    
    def test_run_flag(self):
        # Test initial value
        self.assertFalse(Flag.get_run_flag())

        # Test set run flag
        Flag.set_run_flag()
        self.assertTrue(Flag.get_run_flag())

        # Test clear run flag
        Flag.clear_run_flag()
        self.assertFalse(Flag.get_run_flag())

if __name__ == '__main__':
    unittest.main()
