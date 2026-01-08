import time
import threading
import os



def Timer(minutes):
    start = time.monotonic()
    seconds = minutes * 60
    while seconds >= 0:
        seconds -= 1
        print(f"Time left: {seconds:.2f} seconds")
        time.sleep(1)