from phew import access_point, connect_to_wifi, is_connected_to_wifi, dns, server
from phew.template import render_template
import json
import machine
import os
import utime
import _thread
from picoconfig import PicoConf, WifiConf, APConf
from picostatus import PicoStatus
from mylogging import safe_print


AP_NAME = "Pico Pixel Web"
AP_DOMAIN = "picopixel.net"
AP_TEMPLATE_PATH = "wifi"
APP_TEMPLATE_PATH = "controls"
WIFI_FILE = "wifi.json"

def machine_reset():
    utime.sleep(10)
    print("Resetting...")
    machine.reset()

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


def application_mode():
    print("Entering application mode.")
    onboard_led = machine.Pin("LED", machine.Pin.OUT)

    def app_controls(request):
        return render_template(f"website/controls.html")

    def app_main(request):
        return render_template(f"website/index.html"), 200

    def app_toggle_led(request):
        onboard_led.toggle()
        return "OK"

    def app_reset(request):
        machine_reset()
        return "OK"

    def app_catch_all(request):
        return "Not found.", 404
    
    def app_wifi(request):
        ssid = WifiConf.ssid()
        print( "ssid:" + ssid )
        password = WifiConf.password()
        return render_template( f"website/wifi.html", ssid=ssid, password=password ), 200
        
    def app_ap(request):
        ssid = APConf.ssid()
        password = APConf.password()
        return render_template( f"website/ap.html", ssid=ssid, password=password ), 200
        
    def app_threads(request):
        #ssid = ThreadConf.ssid()
        #password = APConf.password()
        return render_template( f"website/threads.html" ), 200
    
    def app_pico_status(request):
        temp = PicoStatus.temperature()
        mem = PicoStatus.memory()
        return render_template( f"website/pico_status.html", temp=temp, mem=mem ), 200
        
    server.add_route( "/status/pico", handler = app_pico_status, methods = ["GET"] )
    server.add_route( "/", handler = app_main, methods = ["GET"] )
    server.add_route( "/config/ap", handler = app_ap, methods = ["GET"] )
    server.add_route( "/config/wifi", handler = app_wifi, methods = ["GET"] )
    server.add_route( "/config/threads", handler = app_threads, methods = ["GET"] )
    server.add_route( "/controls", handler = app_controls, methods = ["GET"] )
    server.add_route( "/reset", handler = app_reset, methods = ["GET"] )
    server.add_route( "/toggle", handler = app_toggle_led, methods = ["GET"] )
    # Add other routes for your application...
    server.set_callback(app_catch_all)

def start_wifi():
    # Figure out which mode to start up in...
    try:
        os.stat(WIFI_FILE)

        # File was found, attempt to connect to wifi...
        with open(WIFI_FILE) as f:
            wifi_credentials = json.load(f)
            ip_address = connect_to_wifi(wifi_credentials["ssid"], wifi_credentials["password"])

            if not is_connected_to_wifi():
                # Bad configuration, delete the credentials file, reboot
                # into setup mode to get new credentials from the user.
                print("Bad wifi connection!")
                print(wifi_credentials)
                os.remove(WIFI_FILE)
                machine_reset()

            print(f"Connected to wifi, IP address {ip_address}")
            application_mode()

    except Exception:
        # Either no wifi configuration file found, or something went wrong, 
        # so go into setup mode.
        setup_mode()

def start_net(ssid, password):
    
    ip_address = connect_to_wifi(ssid, password)
    if not is_connected_to_wifi():
        print("Bad wifi connection!")
        return False
    
    print(f"Connected to wifi, IP address {ip_address}")
    application_mode()
    return True

# Start the web server...
if __name__ == "__main__":
# this may help with memory errors. 
    import gc
    gc.threshold( 50000 ) # setup garbage collection

    PicoConf.read_file()
    start_net( WifiConf.ssid(), WifiConf.password() )
    server.run()
    
        DOMAIN = "pico.wireless"  # This is the address that is shown on the Captive Portal

    safe_print( "wifi testing..." )

    PicoConf.read_file()
    safe_print(f"AP enabled: {APConf.is_enabled()}")
    safe_print(f"ssid: {WifiConf.ssid()}")
    safe_print(f"password: {WifiConf.password()}")

    Wifi.start_wifi()
    
    @server.route("/", methods=['GET'])
    def index(request):
        """ Render the Index page"""
        if request.method == 'GET':
            logging.debug("Get request")
            return render_template("index.html")

    # microsoft windows redirects
    @server.route("/ncsi.txt", methods=["GET"])
    def hotspot(request):
        print(request)
        print("ncsi.txt")
        return "", 200


    @server.route("/connecttest.txt", methods=["GET"])
    def hotspot(request):
        print(request)
        print("connecttest.txt")
        return "", 200


    @server.route("/redirect", methods=["GET"])
    def hotspot(request):
        print(request)
        print("****************ms redir*********************")
        return redirect(f"http://{DOMAIN}/", 302)

    # android redirects
    @server.route("/generate_204", methods=["GET"])
    def hotspot(request):
        print(request)
        print("******generate_204********")
        return redirect(f"http://{DOMAIN}/", 302)

    # apple redir
    @server.route("/hotspot-detect.html", methods=["GET"])
    def hotspot(request):
        print(request)
        """ Redirect to the Index Page """
        return render_template("index.html")


    @server.catchall()
    def catch_all(request):
        print("***************CATCHALL***********************\n" + str(request))
        return redirect("http://" + DOMAIN + "/")

    server.run()
    logging.info("Webserver Started")
    
    while True:
        print(".", end="")
        time.sleep(10)
        pass


else:
    safe_print( __name__ + " imported")



