# cutebot_pattern.py
from cutebot import *

# Speed and duration settings
speed = 50  # motor speed
delay_time = 0.5  # seconds

def main():
    print("[Cutebot] Starting full movement pattern")

    # Move forward
    for _ in range(4):
        forward(speed)
        wait(delay_time)
        right(speed)
        wait(delay_time)

    # Stop
    stop()
    print("[Cutebot] Movement complete")

if __name__ == "__main__":
    main()