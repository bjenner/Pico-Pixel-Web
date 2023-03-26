import unittest
from picoconfig import PicoConf, WifiConf, APConf, ThreadConf, file_exists

class TestPicoConfig(unittest.TestCase):

    def test_file_exists(self):
        # Ensure the config file is created
        PicoConf.read_file()
        self.assertTrue(file_exists(PicoConf.filename))

    def test_wifi_conf(self):
        # Test WifiConf
        WifiConf.set_ssid("TestSSID")
        WifiConf.set_password("TestPassword")

        self.assertEqual(WifiConf.ssid(), "TestSSID")
        self.assertEqual(WifiConf.password(), "TestPassword")

    def test_ap_conf(self):
        # Test APConf
        APConf.enable()
        APConf.set_ssid("TestAPSSID")
        APConf.set_password("TestAPPassword")

        self.assertTrue(APConf.is_enabled())
        self.assertEqual(APConf.ssid(), "TestAPSSID")
        self.assertEqual(APConf.password(), "TestAPPassword")

    def test_thread_conf(self):
        # Test ThreadConf
        ThreadConf.set_primary("test_primary")
        ThreadConf.set_secondary("test_secondary")

        self.assertEqual(ThreadConf.get_roles()["Primary Role"], "test_primary")
        self.assertEqual(ThreadConf.get_roles()["Secondary Role"], "test_secondary")

    def test_config_html(self):
        config = PicoConf.get_config()
        html = PicoConf.config2html(config)
        self.assertIn("<h2>", html)
        self.assertIn("<ul>", html)
        self.assertIn("<li>", html)

if __name__ == '__main__':
    unittest.main()
