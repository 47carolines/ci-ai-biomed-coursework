# cutebot_step.py
from cutebot import *

# Speed and duration settings
speed = 50
step_time = 0.3  # short step

def main():
    print("[Cutebot] Performing small step")

    # Step forward
    forward(speed)
    wait(step_time)
    
    # Step backward
    backward(speed)
    wait(step_time)

    # Stop
    stop()
    print("[Cutebot] Step complete")

if __name__ == "__main__":
    main()