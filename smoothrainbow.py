import time
from neopixel import Neopixel
from mylogging import safe_print

ITERATIONS_LIMIT = None

def rainbow_role():
    num_pixels = 50
    strip = Neopixel(num_pixels, 0, 28, "GRB")
    hue = 0
    iterations = 0

    while True:
        color = strip.colorHSV(hue, 255, 100)
        strip.fill(color)
        strip.show()
        time.sleep(0.01)
        hue += 150

        # Increment the iterations and break the loop if the limit is reached
        if ITERATIONS_LIMIT is not None:
            iterations += 1
            if iterations >= ITERATIONS_LIMIT:
                break
    
if __name__ == "__main__":
    safe_print("smooth rainbow testing...")

    rainbow_role()

else:
    safe_print( __name__ + " imported")
