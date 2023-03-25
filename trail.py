import time
from neopixel import Neopixel
from mylogging import safe_print
import random

numpix = 50  # Number of NeoPixels
# Pin where NeoPixels are connected
strip = Neopixel(numpix, 0, 28, "RGB")


max_len=20
min_len = 5
#pixelnum, posn in flash, flash_len, direction

num_trail = 4
rp = 0

def trail_step():
    
    global rp
    global numpix
    
    r = 255
    b = 100
    for p in range(rp, rp-25, -1):        
        strip.set_pixel((p)%numpix, (r, 0, 0), b)
        b -= 4
    
    rp = (rp+1)%numpix
    
    strip.show()
    time.sleep(0.05)
    strip.clear()

def trail_role():

    while True:
        trail_step()

if __name__ == "__main__":
    safe_print("trail testing...")

    trail_role()

else:
    safe_print( __name__ + " imported")




