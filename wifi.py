'''
wifi.py - Establish a connection to the network.

This module will attempt to connect to the wifi network.
If an SSID has not been configured or when unable to connect
to the wifi network, an access point is setup to allow
for device configuration. 
'''
import time
from phew import server, connect_to_wifi, access_point, logging, dns
from mylogging import safe_print
from pico_config import WifiConf, APConf, PicoConf

DOMAIN = "pico.wireless"  # This is the address that is shown on the Captive Portal

class Wifi:
    
    @classmethod
    def try_wifi( cls ):
        print( "wifi:" )
        print( WifiConf.ssid() )
        print( WifiConf.password() )
        
        # for now just try one network but later there will be a list
        ip = connect_to_wifi( WifiConf.ssid(), WifiConf.password() )
        
        if (ip == None):
            print( "no wifi" )
            print( APConf.ssid() )
            wlan = access_point( APConf.ssid() )
            if (wlan == None):
                print( "no AP" )
            else:
                print( "AP" )
                ip = wlan.ifconfig()[0]
                dns.run_catchall(ip)
            return False
        
        #print( ip )
        return True

def apmode():


    ap = access_point( "Pixel Web" )
    # Set to Accesspoint mode
    ip = ap.ifconfig()[0]
    logging.info(f"starting DNS server on {ip}")
    dns.run_catchall(ip)
    
    
    
if __name__ == "__main__":
    safe_print( "wifi testing..." )

    PicoConf.read_file()

    Wifi.try_wifi()
    
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

    #PicoConf.read_file()

    #worked = Wifi.try_wifi()
    #print( worked )

else:
    safe_print( __name__ + " imported" )



    
