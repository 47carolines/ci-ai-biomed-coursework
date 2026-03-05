from microbit import *

def flicker(frequency):
    if frequency <= 0:
        return
    
    period = 1000 / frequency
    half_period = period / 2

    while True:
        display.set_pixel(2, 2, 9)
        sleep(int(half_period))
        display.set_pixel(2, 2, 0)
        sleep(int(half_period))

frequency = 3.917727717925015
flicker(frequency)