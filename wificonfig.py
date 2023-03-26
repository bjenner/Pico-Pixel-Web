'''
Wifi configuration
'''

class WifiConf:
    wf_ssid = ""
    wf_password = ""

    @classmethod
    def set_ssid(cls, ssid):
        cls.wf_ssid = ssid

    @classmethod
    def set_password(cls, password):
        cls.wf_password = password

    @classmethod
    def ssid(cls):
        return cls.wf_ssid

    @classmethod
    def password(cls):
        return cls.wf_password

    @classmethod
    def get_wifi_conf(cls):
        return {"Wifi SSID": cls.wf_ssid,
                "Wifi Password": cls.wf_password}

    @classmethod
    def save_wifi(cls, wifi):
        WifiConf.set_ssid(wifi["Wifi SSID"])
        WifiConf.set_password(wifi["Wifi Password"])

    @classmethod
    def get_wifi_defaults(cls):
        return {"Wifi SSID": "",
                "Wifi Password": ""}