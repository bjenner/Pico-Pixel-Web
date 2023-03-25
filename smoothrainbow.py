import time
from neopixel import Neopixel
from mylogging import safe_print

def rainbow_role():
    numpix = 50
    strip = Neopixel(numpix, 0, 28, "GRB")

    hue = 0
    while(True):
        color = strip.colorHSV(hue, 255, 100)
        strip.fill(color)
        strip.show()
        time.sleep(0.01)
        hue += 150
    
if __name__ == "__main__":
    safe_print("smooth rainbow testing...")

    rainbow_role()

else:
    safe_print( __name__ + " imported")


