'''
picoconfig.py = configuration of the device 
'''
import os
import json
from roles import Roles
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

class WifiConf:
    
    wf_ssid = ""
    wf_password = ""
    
    @classmethod
    def set_ssid( cls, ssid ):
        cls.wf_ssid = ssid
    
    @classmethod
    def set_password( cls, password ):
        cls.wf_password = password

    @classmethod
    def ssid( cls ):
        return cls.wf_ssid
    
    @classmethod
    def password( cls ):
        return cls.wf_password
    
    @classmethod
    def get_wifi_conf( cls ):
        return { "Wifi SSID": cls.wf_ssid ,
                 "Wifi Password": cls.wf_password } 

    @classmethod
    def save_wifi( cls, wifi ):
        WifiConf.set_ssid( wifi["Wifi SSID"] )
        WifiConf.set_password( wifi["Wifi Password"] )
        
    @classmethod
    def get_wifi_defaults( cls ):
        return { "Wifi SSID": "",
                 "Wifi Password": "" }

class APConf:
    ap_enabled = True
    ap_ssid = ""
    ap_password = ""

    @classmethod
    def enable( cls ):
        cls.ap_ssid = True
    
    @classmethod
    def disable( cls ):
        cls.ap_ssid = False
    
    @classmethod
    def set_ssid( cls, ssid ):
        cls.ap_ssid = ssid
    
    @classmethod
    def set_password( cls, password ):
        cls.ap_password = password

    @classmethod
    def is_enabled( cls ):
        return cls.ap_enabled
    
    @classmethod
    def ssid( cls ):
        return cls.ap_ssid
    
    @classmethod
    def password( cls ):
        return cls.ap_password
    
    @classmethod
    def get_ap_conf( cls ):
        return { "Access Point Enabled": cls.ap_enabled, 
                 "Access Point SSID": cls.ap_ssid,
                 "Access Point Password": cls.ap_password } 

    @classmethod
    def save_ap( cls, ap ):
        print( ap )
        if (ap["Access Point Enabled"] == True):
            cls.enable()
        else:
            cls.disable()
        cls.set_ssid( ap["Access Point SSID"] )
        cls.set_password( ap["Access Point Password"] )
       
    @classmethod
    def get_ap_defaults( cls ):
        return { "Access Point Enabled": True,
                 "Access Point SSID": "Pico Pixel Web",
                 "Access Point Password": ""}


class ThreadConf:
    primary_role = None
    secondary_role = None

    @classmethod
    def set_primary( cls, role ):
        cls.primary_role = role

    @classmethod
    def set_secondary( cls, role ):
        cls.secondary_role = role

    @classmethod
    def start_primary( cls ):
        print("hello")
        time.sleep(2)
        role_map = Roles.primary_map()
        safe_print( f"role map: {role_map}" )
        safe_print( f"primary: {cls.primary_role}" )
        role_map[cls.primary_role]()

    @classmethod
    def start_secondary( cls ):
        safe_print( "Start Secondary" )
        role_map = Roles.secondary_map()
        safe_print( f"role map: {role_map}" )
        safe_print( f"second: {cls.secondary_role}" )
        role_map[cls.secondary_role]()

    @classmethod
    def secondary( cls ):
        safe_print( "Secondary" )
        role_map = Roles.secondary_map()
        safe_print( f"role map: {role_map}" )
        safe_print( f"second: {cls.secondary_role}" )
        role_map[cls.secondary_role]()

    @classmethod
    def get_roles( cls ):
        return { "Primary Role": cls.primary_role ,
                 "Secondary Role": cls.secondary_role } 

    @classmethod
    def save_roles( cls, roles ):
        safe_print( f"save_roles: {roles}" )
        ThreadConf.set_primary( roles["Primary Role"] )
        ThreadConf.set_secondary( roles["Secondary Role"] )
                
    @classmethod
    def get_role_defaults( cls ):
        return { "Primary Role": "test",
                 "Secondary Role": 'none' }

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


