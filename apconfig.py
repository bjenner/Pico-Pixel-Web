'''
apconfig - Access Point Configuration
'''

class APConf:
    ap_enabled = True
    ap_ssid = ""
    ap_password = ""

    @classmethod
    def enable(cls):
        cls.ap_enabled = True

    @classmethod
    def disable(cls):
        cls.ap_enabled = False

    @classmethod
    def set_ssid(cls, ssid):
        cls.ap_ssid = ssid

    @classmethod
    def set_password(cls, password):
        cls.ap_password = password

    @classmethod
    def is_enabled(cls):
        return cls.ap_enabled

    @classmethod
    def ssid(cls):
        return cls.ap_ssid

    @classmethod
    def password(cls):
        return cls.ap_password

    @classmethod
    def get_ap_conf(cls):
        return {"Access Point Enabled": cls.ap_enabled,
                "Access Point SSID": cls.ap_ssid,
                "Access Point Password": cls.ap_password}

    @classmethod
    def save_ap(cls, ap):
        if ap["Access Point Enabled"]:
            cls.enable()
        else:
            cls.disable()
        cls.set_ssid(ap["Access Point SSID"])
        cls.set_password(ap["Access Point Password"])

    @classmethod
    def get_ap_defaults(cls):
        return {"Access Point Enabled": True,
                "Access Point SSID": "Pico Pixel Web",
                "Access Point Password": ""}

if __name__ == "__main__":

    safe_print("AP SSID: " + APConf.ssid())
    safe_print("AP Password: " + APConf.password())

else:
    safe_print(__name__ + " imported")

