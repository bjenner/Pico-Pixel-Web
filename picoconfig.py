'''
picoconfig.py = configuration of the device 
'''
import os
import json
from roles import Roles
from wificonfig import WifiConf
from apconfig import APConf
from threadconfig import ThreadConf
import time

from mylogging import safe_print
from switchcase import switch, case

        
def file_or_dir_exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False

import os
def dir_exists(filename):
    try:
        return (os.stat(filename)[0] & 0x4000) != 0
    except OSError:
        return False
        
def file_exists(filename):
    try:
        return (os.stat(filename)[0] & 0x4000) == 0
    except OSError:
        return False

class PicoConf:
    filename = "pico_config.json"
    
    def create_defaults():
        defaults = {}
        defaults["Roles"] = ThreadConf.get_role_defaults()
        defaults["Wifi"] = WifiConf.get_wifi_defaults()
        defaults["Access Point"] = APConf.get_ap_defaults()

        # convert into JSON:
        conf_json = json.dumps(defaults)

        f = open(PicoConf.filename, 'w')
        f.write(conf_json)
        f.close()

    def load_config():
        f = open(PicoConf.filename)
        config = json.loads(f.read())
        f.close()
        
        return config
    
    def save_config(config):
        ThreadConf.save_roles( config["Roles"] )
        WifiConf.save_wifi( config["Wifi"] )
        APConf.save_ap( config["Access Point"] )

    @classmethod
    def get_config( cls ):
        config = {}
        config["Roles"] = ThreadConf.get_roles()
        config["Wifi"] = WifiConf.get_wifi_conf()
        config["Access Point"] = APConf.get_ap_conf()
        
        return config
        
    @classmethod
    def read_file(cls):
        
        if ( False == file_exists(cls.filename) ):
            cls.create_defaults()

        config = cls.load_config()
        
        cls.save_config(config)
                  
    @classmethod
    def pico_conf_write(cls):
        safe_print( f"writing to {PicoConf.filename}" )
        f = open(PicoConf.filename, 'w')
        f.write(json.dumps(cls.get_config()))
        f.close()
        
    @classmethod
    def init( cls ):
        cls.read_file()
        
if __name__ == "__main__":
    import _thread
    import machine

    PicoConf.init()
    
    safe_print( "Configuration:" )
    safe_print( "SSID: " + WifiConf.ssid() )
    safe_print( "Password: " + WifiConf.password() )

    safe_print( "AP SSID: " + APConf.ssid() )
    safe_print( "AP Password: " + APConf.password() )

    safe_print( "Roles" )
    safe_print( ThreadConf.get_roles() )
    
    config = PicoConf.get_config()
    safe_print( "Config" )
    safe_print( config )

    #safe_print( f"Primary fn {ThreadConf.start_primary}" )
    safe_print( f"Secondary fn {ThreadConf.secondary}" )
    #ThreadConf.start_secondary()()
    thread_one = _thread.start_new_thread(ThreadConf.start_secondary, ())
    #ThreadConf.start_primary()
    safe_print( "Here" )

else:
    safe_print( __name__ + " imported")


