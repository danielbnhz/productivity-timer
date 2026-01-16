import time
import threading
import sys

class Timer:
    def __init__(self, minutes: float):
        self.remaining = minutes * 60
        self.paused = False
        self.finished = False
        self._lock = threading.Lock()

    def start(self):
        last_tick = time.monotonic()

        while not self.finished:
            now = time.monotonic()
            with self._lock:
                if not self.paused:
                    # Only subtract elapsed time when running
                    delta = now - last_tick
                    self.remaining -= delta

                    if self.remaining <= 0:
                        self.remaining = 0
                        self.finished = True

                # Always update last_tick, even if paused
                last_tick = now

            # Print time above input line
            mins, secs = divmod(int(self.remaining), 60)
            sys.stdout.write(f"\rTime left: {mins}:{secs:02d}   ")
            sys.stdout.flush()

            # Short sleep to make thread responsive
            time.sleep(0.1)

    def pause(self):
        with self._lock:
            self.paused = True

    def resume(self):
        with self._lock:
            self.paused = False

    def stop(self):
        """Immediately stop the timer, safe for quitting early"""
        with self._lock:
            self.paused = True
            self.finished = True
