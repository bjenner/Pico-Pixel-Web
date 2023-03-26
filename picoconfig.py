'''
picoconfig.py = configuration of the device
'''
import os
import json
from roles import Roles
from wificonfig import WifiConf
from apconfig import APConf
from threadconfig import ThreadConf
from mylogging import safe_print


def file_exists(filename):
    try:
        return (os.stat(filename)[0] & 0x4000) == 0
    except OSError:
        return False


class PicoConf:
    filename = "pico_config.json"

    @staticmethod
    def create_defaults():
        defaults = {
            "Roles": ThreadConf.get_role_defaults(),
            "Wifi": WifiConf.get_wifi_defaults(),
            "Access Point": APConf.get_ap_defaults()
        }
        conf_json = json.dumps(defaults)

        with open(PicoConf.filename, 'w') as f:
            f.write(conf_json)

    @staticmethod
    def load_config():
        with open(PicoConf.filename) as f:
            config = json.loads(f.read())
        return config

    @staticmethod
    def save_config(config):
        ThreadConf.save_roles(config["Roles"])
        WifiConf.save_wifi(config["Wifi"])
        APConf.save_ap(config["Access Point"])

    @classmethod
    def get_config(cls):
        config = {
            "Roles": ThreadConf.get_roles(),
            "Wifi": WifiConf.get_wifi_conf(),
            "Access Point": APConf.get_ap_conf()
        }
        return config

    @classmethod
    def read_file(cls):
        if not file_exists(cls.filename):
            cls.create_defaults()

        config = cls.load_config()
        cls.save_config(config)

    @classmethod
    def pico_conf_write(cls):
        safe_print(f"writing to {PicoConf.filename}")
        with open(PicoConf.filename, 'w') as f:
            f.write(json.dumps(cls.get_config()))

    @classmethod
    def init(cls):
        cls.read_file()


if __name__ == "__main__":
    import _thread
    import machine

    PicoConf.init()

    safe_print("Configuration:")
    safe_print("SSID: " + WifiConf.ssid())
    safe_print("Password: " + WifiConf.password())

    safe_print("AP SSID: " + APConf.ssid())
    safe_print("AP Password: " + APConf.password())

    safe_print("Roles")
    safe_print(ThreadConf.get_roles())

    config = PicoConf.get_config()
    safe_print("Config")
    safe_print(config)

    safe_print(f"Secondary fn {ThreadConf.secondary}")
    thread_one = _thread.start_new_thread(ThreadConf.start_secondary, ())
    safe_print("Here")

else:
    safe_print(__name__ + " imported")


