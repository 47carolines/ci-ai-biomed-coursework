from microbit import *

frequency = 2  # simple test frequency

wait_time = 1000 / (2 * frequency)

while True:
    display.set_pixel(2, 2, 9)
    sleep(wait_time)

    display.set_pixel(2, 2, 0)
    sleep(wait_time)