from time import sleep
from neopixel import Neopixel
from mylogging import safe_print
from random import randint

numpix = 50  # Number of NeoPixels
# Pin where NeoPixels are connected
strip = Neopixel(numpix, 0, 28, "GRB")

colors_rgb = [
    (232, 100, 255),  # Purple
    (200, 200, 20),  # Yellow
    (30, 200, 200),  # Blue
    (150,50,10),
    (50,200,10),
]

# same colors as normaln rgb, just 0 added at the end
colors_rgbw = [color+tuple([0]) for color in colors_rgb]
colors_rgbw.append((0, 0, 0, 255))

# uncomment colors_rgbw if you have RGBW strip
colors = colors_rgb
# colors = colors_rgbw

max_len=20
min_len = 5
#pixelnum, posn in flash, flash_len, direction
flashing = []

num_flashes = 10

for i in range(num_flashes):
    pix = randint(0, numpix - 1)
    col = randint(1, len(colors) - 1)
    flash_len = randint(min_len, max_len)
    flashing.append([pix, colors[col], flash_len, 0, 1])
    
strip.fill((0,0,0))

def firefly_step():
    strip.show()
    for i in range(num_flashes):

        pix = flashing[i][0]
        brightness = (flashing[i][3]/flashing[i][2])
        colr = (int(flashing[i][1][0]*brightness), 
                int(flashing[i][1][1]*brightness), 
                int(flashing[i][1][2]*brightness))
        strip.set_pixel(pix, colr)

        if flashing[i][2] == flashing[i][3]:
            flashing[i][4] = -1
        if flashing[i][3] == 0 and flashing[i][4] == -1:
            pix = randint(0, numpix - 1)
            col = randint(0, len(colors) - 1)
            flash_len = randint(min_len, max_len)
            flashing[i] = [pix, colors[col], flash_len, 0, 1]
        flashing[i][3] = flashing[i][3] + flashing[i][4]
        sleep(0.005)
 

def firefly_role():

    while True:
        firefly_step()
 
if __name__ == "__main__":
    safe_print("firefly testing...")

    firefly_role()

else:
    safe_print( __name__ + " imported")

