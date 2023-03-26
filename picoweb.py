'''
picoweb.py - Website for the devices 
'''

from phew import access_point, connect_to_wifi, is_connected_to_wifi, dns, server
from phew.template import render_template
import json
import machine
import os
import utime
import gc
from wificonfig import WifiConf
from apconfig import APConf
from threadconfig import ThreadConf
from picoconfig import PicoConf
from picostatus import PicoStatus
from mylogging import safe_print
from roles import Roles
from wifi import Wifi

class PicoWeb:
    
    @classmethod
    def setup_website( cls ):
        safe_print( "Setting up website." )
        onboard_led = machine.Pin( "LED", machine.Pin.OUT )

        def app_main(request):
            return render_template( f"website/index.html" ), 200

        server.add_route( "/", handler = app_main, methods = ["GET"] )

        def app_controls_led(request):
            return render_template( f"website/controls.html" )

        def app_toggle_led( request ):
            onboard_led.toggle()
            return "OK"

        def app_reset( request ):
            machine.reset()
            return "OK"

        server.add_route( "/controls/led", handler = app_controls_led, methods = ["GET"] )
        server.add_route( "/reset", handler = app_reset, methods = ["GET"] )
        server.add_route( "/toggle", handler = app_toggle_led, methods = ["GET"] )

        def app_save( request ):
            PicoConf.pico_conf_write()
            return "OK"
        
        def app_config( request ):
            return render_template( f"website/config.html" ), 200
        
        server.add_route( "/config", handler = app_config, methods = ["GET"] )
        server.add_route( "/save", handler = app_save, methods = ["GET"] )
        server.add_route( "/reboot", handler = app_reset, methods = ["GET"] )

        def app_wifi( request ):
            ssid = WifiConf.ssid()
            password = WifiConf.password()
            return render_template( f"website/wifi.html", ssid=ssid, password=password ), 200

        def app_wifi_configure(request):
            safe_print("Saving wifi credentials...")
            WifiConf.set_ssid( request.form['ssid'] )
            WifiConf.set_password( request.form['password'] )
            return render_template(f"website/config.html")
        
        server.add_route( "/config/wifi", handler = app_wifi, methods = ["GET"] )
        server.add_route( "/config/wifi", handler = app_wifi_configure, methods = ["POST"])

        def app_ap(request):
            ssid = APConf.ssid()
            password = APConf.password()
            return render_template( f"website/ap.html", ssid=ssid, password=password ), 200

        def app_ap_configure(request):
            safe_print("Saving AP credentials...")
            safe_print( request )
            APConf.set_ssid( request.form['ssid'] )
            APConf.set_password( request.form['password'] )
            #safe_print( request.form['enable_ap'] )
            #APConf.enable( request.form['enabled'] )
            return render_template(f"website/config.html")

        server.add_route( "/config/ap", handler = app_ap, methods = ["GET"] )
        server.add_route( "/config/ap", handler = app_ap_configure, methods = ["POST"] )        
            
        def app_threads(request):
            roles = ThreadConf.get_roles()
            Roles.set_checked(roles["Primary Role"], roles["Secondary Role"])
            webmap = Roles.get_webmap()
            return render_template( f"website/threads.html", primmap=webmap['primary'], secmap=webmap['secondary']  ), 200

        def app_threads_configure(request):
            safe_print("Saving thread credentials...")
            ThreadConf.set_primary( request.form['primary'] )
            ThreadConf.set_secondary( request.form['secondary'] )
            return render_template(f"website/config.html" )

        server.add_route( "/config/threads", handler = app_threads, methods = ["GET"] )
        server.add_route( "/config/threads", handler = app_threads_configure, methods = ["POST"] )

        def app_pico_status(request):
            temp = PicoStatus.temperature()
            mem = PicoStatus.memory()
            return render_template( f"website/pico_status.html", temp=temp, mem=mem ), 200
            
        server.add_route( "/status/pico", handler = app_pico_status, methods = ["GET"] )

        # Add other routes for your application...
        def app_catch_all( request ):
            return "Not found.", 404
        
        server.set_callback( app_catch_all )

    @classmethod
    def website_role( cls ):
        gc.threshold( 50000 ) # setup garbage collection
        cls.setup_website()
        server.run()

    @classmethod
    def init( cls ):
        Wifi.start()
        return

Roles.set_role( 'primary', 'web', PicoWeb.website_role )
    

# Start the web server...
if __name__ == "__main__":
    import gc
    import _thread
    from roles import Roles

    gc.threshold( 50000 ) # setup garbage collection
    
    safe_print( "Testing website" )
    # this may help with memory errors. 
    def start_wifi():
        # Figure out which mode to start up in...
        try:
            os.stat( WIFI_FILE )

            # File was found, attempt to connect to wifi...
            with open( WIFI_FILE ) as f:
                wifi_credentials = json.load( f )
                ip_address = connect_to_wifi( wifi_credentials["ssid"], wifi_credentials["password"] )

                if not is_connected_to_wifi():
                    # Bad configuration, delete the credentials file, reboot
                    # into setup mode to get new credentials from the user.
                    print( "Bad wifi connection!" )
                    print( wifi_credentials )
                    os.remove( WIFI_FILE )
                    machine_reset()

                print( f"Connected to wifi, IP address {ip_address}" )
                application_mode()

        except Exception:
            # Either no wifi configuration file found, or something went wrong, 
            # so go into setup mode.
            setup_mode()

    def start_net( ssid, password ):
    
        ip_address = connect_to_wifi( ssid, password )
        if not is_connected_to_wifi():
            print( "Bad wifi connection!" )
            return False
    
        print( f"Connected to wifi, IP address {ip_address}" )
        application_mode()
        return True

    PicoConf.init()
    PicoWeb.init()
    #start_net( WifiConf.ssid(), WifiConf.password() )
    ip_address = connect_to_wifi( WifiConf.ssid(), WifiConf.password() )
    safe_print( f"IP: {ip_address}"  )
    PicoWeb.setup_website()
    server.run()

else:
    safe_print( __name__ + " imported" )
