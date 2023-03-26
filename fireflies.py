from time import sleep
from neopixel import Neopixel
from mylogging import safe_print
from random import randint

# Constants
NUM_PIXELS = 50
NUM_FLASHES = 10
MIN_LENGTH = 5
MAX_LENGTH = 20
NEOPIXEL_PIN = 28

# Colors
COLORS = [
    (232, 100, 255),  # Purple
    (200, 200, 20),   # Yellow
    (30, 200, 200),   # Blue
    (150, 50, 10),
    (50, 200, 10),
]

# Initialize the NeoPixel strip
strip = Neopixel(NUM_PIXELS, 0, NEOPIXEL_PIN, "GRB")

# Initialize the flashing list with random values
flashing = [
    [
        randint(0, NUM_PIXELS - 1),
        COLORS[randint(1, len(COLORS) - 1)],
        randint(MIN_LENGTH, MAX_LENGTH),
        0,
        1,
    ]
    for _ in range(NUM_FLASHES)
]

# Clear the strip
strip.fill((0, 0, 0))


def firefly_step():
    strip.show()

    for i in range(NUM_FLASHES):
        pixel_index = flashing[i][0]
        color = flashing[i][1]
        flash_length = flashing[i][2]
        progress = flashing[i][3]
        direction = flashing[i][4]

        brightness = progress / flash_length
        adjusted_color = (
            int(color[0] * brightness),
            int(color[1] * brightness),
            int(color[2] * brightness),
        )
        strip.set_pixel(pixel_index, adjusted_color)

        if progress == flash_length:
            direction = -1
        elif progress == 0 and direction == -1:
            pixel_index = randint(0, NUM_PIXELS - 1)
            color = COLORS[randint(0, len(COLORS) - 1)]
            flash_length = randint(MIN_LENGTH, MAX_LENGTH)
            flashing[i] = [pixel_index, color, flash_length, 0, 1]

        flashing[i][3] = progress + direction
        sleep(0.005)

def firefly_role():

    while True:
        firefly_step()
 
if __name__ == "__main__":
    safe_print("firefly testing...")

    firefly_role()

else:
    safe_print( __name__ + " imported")

