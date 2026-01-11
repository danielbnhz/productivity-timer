import time

class Timer:
    def __init__(self, minutes: float):
        self.remaining = minutes * 60
        self.paused = False
        self._last_tick = None
        self.finished = False

    def start(self):
        self._last_tick = time.monotonic()
        while not self.finished:
            self._tick()
            time.sleep(1)

    def _tick(self):
        now = time.monotonic()
        delta = now - self._last_tick
        self._last_tick = now

        if not self.paused:
            self.remaining -= delta

        if self.remaining <= 0:
            self.remaining = 0
            self.finished = True

        mins, secs = divmod(int(self.remaining), 60)
        print(f"Time left: {mins}:{secs:02d}", end="\r")

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
