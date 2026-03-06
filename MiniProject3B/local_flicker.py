from microbit import *

frequency = 2   # default frequency if argument fails

def flicker(freq):
    wait_time = 1000 / (2 * freq)

    while True:
        display.set_pixel(2, 2, 9)
        sleep(wait_time)

        display.set_pixel(2, 2, 0)
        sleep(wait_time)

# Try reading runtime frequency if possible
try:
    import sys
    frequency = float(sys.argv[1])
except:
    pass

flicker(frequency)