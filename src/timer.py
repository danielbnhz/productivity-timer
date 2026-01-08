import time
import threading
import os



def Timer(minutes):
    start = time.monotonic()
    seconds = minutes * 60
    while True:
        elapsed = time.monotonic() - start
        remaining = max(seconds - elapsed, 0)
        mins, secs = divmod(remaining, 60)
        print(f"Time left: {int(mins)}:{int(secs):02d}", end="\r")
        if remaining <= 0:
            break
        time.sleep(1)
