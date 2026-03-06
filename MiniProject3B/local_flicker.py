from microbit import *

# Frequency injected by pipeline rewrite
frequency = 2

def flicker(freq):

    # Safety guard
    if freq <= 0:
        freq = 2

    wait_time = int(1000 / (2 * freq))

    while True:
        display.set_pixel(2, 2, 9)
        sleep(wait_time)

        display.set_pixel(2, 2, 0)
        sleep(wait_time)

# Run flicker
flicker(frequency)