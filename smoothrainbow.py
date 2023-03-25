import time
from neopixel import Neopixel
from mylogging import safe_print

# Add a variable to limit the number of iterations
iterations_limit = None

def rainbow_role():
    numpix = 50
    strip = Neopixel(numpix, 0, 28, "GRB")

    hue = 0
    iterations = 0
    while(True):
        color = strip.colorHSV(hue, 255, 100)
        strip.fill(color)
        strip.show()
        time.sleep(0.01)
        hue += 150

        # Increment the iterations and break the loop if the limit is reached
        if iterations_limit is not None:
            iterations += 1
            if iterations >= iterations_limit:
                break
    
if __name__ == "__main__":
    safe_print("smooth rainbow testing...")

    rainbow_role()

else:
    safe_print( __name__ + " imported")
