'''
pico_config.py = configuration of the device 
'''
import _thread
import machine
import os
import json
from roles import Roles

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
        role_map = Roles.primary_map()
        role_map[cls.primary_role]()

    @classmethod
    def start_secondary( cls ):
        role_map = Roles.secondary_map()
        role_map[cls.secondary_role]()

    @classmethod
    def get_roles( cls ):
        return { "Primary Role": cls.primary_role ,
                 "Secondary Role": cls.secondary_role } 

    @classmethod
    def save_roles( cls, roles ):
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
    def config2html( cls, config ):
        
        html = ""
        #html = "<div>\n"
        for section_label in config.keys():
            html += "<h2>" + section_label + "</h2>\n"
            section = config[section_label]
            
            html += "<ul>\n"
            for item_label in section.keys():
                
                html += "<li> " + "{:<25}".format(item_label + ":") 
                item = section[item_label]
                html += str(item) + "</li>\n"
            
            html += "</ul>\n"
        #html += "</div>\n"

        return html
    
    @classmethod
    def read_file(cls):
        
        if ( False == file_exists(cls.filename) ):
            PicoConf.create_defaults()

        config = PicoConf.load_config()
        
        PicoConf.save_config(config)
            
    @classmethod    
    def pico_conf_read():

        # a Python object (dict):
        x = {
          "name": "John",
          "age": 30,
          "city": "New York"
        }

        # convert into JSON:
        y = json.dumps(x)

        # the result is a JSON string:
        print(y)

        os.listdir()

        os.mkdir('testdir')

        f = open('testdir/data.txt', 'w')
        f.write(y)
        f.close()

        f = open('testdir/data.txt')
        z = json.loads(f.read())
        print (z)
        f.close()

        #os.remove('testdir/data.txt')
        #os.remove('testdir')
        
    @classmethod
    def pico_conf_write():
        pass
        

if __name__ == "__main__":
    
    PicoConf.read_file()
    
    print( "Configuration:" )
    print( "SSID: " + WifiConf.ssid() )
    print( "Password: " + WifiConf.password() )

    print( "AP SSID: " + APConf.ssid() )
    print( "AP Password: " + APConf.password() )

    print( "Roles" )
    print( ThreadConf.get_roles() )
    
    config = PicoConf.get_config()
    print( "Config" )
    print( config )

    print( "HTML" )
    html = PicoConf.config2html( config )
    
    print( html ) 
    #thread_one = _thread.start_new_thread(ThreadConf.start_secondary, ())
    #ThreadConf.start_primary()

else:
    safe_print( __name__ + " imported")


