from microbit import *
import time

interval = 100  # milliseconds
sequence = [
    (0, 5),  # steady 5 sec
    (1, 5),  # shake 5 sec
    (0, 5),  # steady 5 sec
    (1, 5)   # shake 5 sec
]

start_time = time.ticks_ms()
print("timestamp,x,y,z,label")  # CSV header

for label, sec in sequence:
    steps = int(sec * 1000 / interval)
    for _ in range(steps):
        t = (time.ticks_ms() - start_time) / 1000
        x = accelerometer.get_x()
        y = accelerometer.get_y()
        z = accelerometer.get_z()
        print("{:.2f},{},{},{},{}".format(t, x, y, z, label))
        sleep(interval)
