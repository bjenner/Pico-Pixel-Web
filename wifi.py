'''
wifi.py - Establish a connection to the network.

This module will attempt to connect to the wifi network.
If an SSID has not been configured or when unable to connect
to the wifi network, an access point is setup to allow
for device configuration. 
'''
from phew import connect_to_wifi, access_point, dns, is_connected_to_wifi
from mylogging import safe_print
from wificonfig import WifiConf
from apconfig import APConf
from picoconfig import PicoConf

class Wifi:
    @classmethod
    def start_access_point(cls):
        ap = access_point( APConf.ssid() )
        # Set to Accesspoint mode
        ip = ap.ifconfig()[0]
        safe_print(f"starting DNS server on {ip}")
        dns.run_catchall(ip)
    
    @classmethod
    def start(cls):
        if not APConf.is_enabled():
            try:
                ip_address = connect_to_wifi(WifiConf.ssid(), WifiConf.password())
                safe_print(f"Connected to wifi, IP address {ip_address}")

                # Wifi is not working, enable Access Point, save, reboot. 
                if not is_connected_to_wifi():
                    APConf.enable()
                    PicoConf.pico_conf_write()
                    machine.reset()

                print(f"Connected to wifi, IP address {ip_address}")
            
            except Exception as e:
                # Either no wifi configuration file found, or something went wrong,
                # so go into setup mode.
                safe_print(f"Exception: {e}")
                cls.start_access_point()
        else:
            # Force Access Point mode
            cls.start_access_point()
    
if __name__ == "__main__":
    from phew import server
    
    # TBD

else:
    safe_print( __name__ + " imported" )



    
