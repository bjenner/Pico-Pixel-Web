from time import sleep
from neopixel import Neopixel
from mylogging import safe_print

# Constants
NUM_PIXELS = 50
NEOPIXEL_PIN = 28
COLORS_RGB = [
    (255, 0, 0),      # Red
    (255, 50, 0),     # Orange
    (255, 100, 0),    # Yellow
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (100, 0, 90),     # Indigo
    (200, 0, 100),    # Violet
]

# Initialize the NeoPixel strip
strip = Neopixel(NUM_PIXELS, 0, NEOPIXEL_PIN, "GRB")
strip.brightness(50)

# Create gradients
step = round(NUM_PIXELS / len(COLORS_RGB))
current_pixel = 0

for color1, color2 in zip(COLORS_RGB, COLORS_RGB[1:]):
    strip.set_pixel_line_gradient(current_pixel, current_pixel + step, color1, color2)
    current_pixel += step

strip.set_pixel_line_gradient(current_pixel, NUM_PIXELS - 1, COLORS_RGB[-1], COLORS_RGB[0])

def colourwave_role():
    while True:
        strip.rotate_right(1)
        sleep(0.1)
        strip.show()

if __name__ == "__main__":
    safe_print("colourwave testing...")

    colourwave_role()

else:
    safe_print( __name__ + " imported")

