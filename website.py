from phew import access_point, connect_to_wifi, is_connected_to_wifi, dns, server
from phew.template import render_template
import json
import machine
import os
import utime
import _thread
from roles import Roles
from pico_config import PicoConf, WifiConf, APConf, ThreadConf
from pico_status import PicoStatus
from mylogging import safe_print

def setup_mode():
    print("Entering setup mode...")
    
    def ap_index(request):
        if request.headers.get("host") != AP_DOMAIN:
            return render_template(f"website/config/{AP_TEMPLATE_PATH}/redirect.html", domain = AP_DOMAIN)

        return render_template(f"website/config/{AP_TEMPLATE_PATH}/index.html")

    def ap_configure(request):
        print("Saving wifi credentials...")

        with open(WIFI_FILE, "w") as f:
            json.dump(request.form, f)
            f.close()

        # Reboot from new thread after we have responded to the user.
        _thread.start_new_thread(machine_reset, ())
        return render_template(f"website/config/{AP_TEMPLATE_PATH}/configured.html", ssid = request.form["ssid"])
        
    def ap_catch_all(request):
        if request.headers.get("host") != AP_DOMAIN:
            return render_template(f"website/config/{AP_TEMPLATE_PATH}/redirect.html", domain = AP_DOMAIN)

        return "Not found.", 404

    server.add_route("/", handler = ap_index, methods = ["GET"])
    server.add_route("/", handler = ap_configure, methods = ["POST"])
    server.set_callback(ap_catch_all)

    ap = access_point(AP_NAME)
    ip = ap.ifconfig()[0]
    print (ip)
    dns.run_catchall(ip)

def setup_website():
    safe_print( "Setting up website." )
    onboard_led = machine.Pin( "LED", machine.Pin.OUT )

    def app_controls_led(request):
        return render_template( f"website/controls.html" )

    def app_main(request):
        return render_template( f"website/index.html" ), 200

    def app_toggle_led( request ):
        onboard_led.toggle()
        return "OK"

    def app_reset( request ):
        machine_reset()
        return "OK"

    def app_catch_all( request ):
        return "Not found.", 404
    
    def app_wifi( request ):
        ssid = WifiConf.ssid()
        password = WifiConf.password()
        return render_template( f"website/wifi.html", ssid=ssid, password=password ), 200
        
    def app_ap(request):
        ssid = APConf.ssid()
        password = APConf.password()
        return render_template( f"website/ap.html", ssid=ssid, password=password ), 200
        
    def app_threads(request):
        roles = ThreadConf.get_roles()
        primary = roles["Primary Role"]
        secondary = roles["Secondary Role"]
        checked = ["", "checked"]
        webmap = Roles.get_webmap()
        return render_template( f"website/threads.html", prim="test", second=2, checked=checked, webmap=webmap ), 200
    
    def app_pico_status(request):
        temp = PicoStatus.temperature()
        mem = PicoStatus.memory()
        return render_template( f"website/pico_status.html", temp=temp, mem=mem ), 200
        
    server.add_route( "/status/pico", handler = app_pico_status, methods = ["GET"] )
    server.add_route( "/", handler = app_main, methods = ["GET"] )
    server.add_route( "/config/ap", handler = app_ap, methods = ["GET"] )
    server.add_route( "/config/wifi", handler = app_wifi, methods = ["GET"] )
    server.add_route( "/config/threads", handler = app_threads, methods = ["GET"] )
    server.add_route( "/controls/led", handler = app_controls_led, methods = ["GET"] )
    server.add_route( "/reset", handler = app_reset, methods = ["GET"] )
    server.add_route( "/toggle", handler = app_toggle_led, methods = ["GET"] )
    # Add other routes for your application...
    server.set_callback( app_catch_all )

# Start the web server...
if __name__ == "__main__":
    import gc
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

    PicoConf.read_file()
    #start_net( WifiConf.ssid(), WifiConf.password() )
    ip_address = connect_to_wifi( WifiConf.ssid(), WifiConf.password() )
    safe_print( f"IP: {ip_address}"  )
    setup_website()
    server.run()

else:
    safe_print( __name__ + " imported" )
