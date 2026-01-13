from timer import Timer
from storage import init_db, log_session
from logger import logger
import utils
import config
import threading
import msvcrt
import time
import sys

init_db()

def keyboard_listener(timer):
    while not timer.finished:
        if msvcrt.kbhit():
            cmd = msvcrt.getwch().lower()
            if cmd == "p":
                timer.pause()
            elif cmd == "r":
                timer.resume()
            elif cmd == "q":
                timer.stop()
        time.sleep(0.05)

def main():
    logger.info("App started")
    print("Running program\n")

    run_sessions = True
    while run_sessions:
        start_task = input("Start task? (y/n): ").strip().lower()
        if start_task != "y":
            run_sessions = False
            continue
        session_id = utils.generate_session_id()
        logger.info(f"Session started: {session_id}")
        start = utils.now_utc_ts()

        # Get minutes
        while True:
            try:
                minutes = int(input("Minutes: "))
                if minutes <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Please enter a positive number")

        # Get category
        while True:
            category = input("Please input task category: ").strip()
            if category in config.CATEGORIES:
                break
            print(f"Please enter a valid category from: {config.CATEGORIES}")

        # Create and start timer in background thread
        timer = Timer(minutes)
        timer.finished = False

        timer_thread = threading.Thread(target=timer.start)
        k_thread = threading.Thread(target=keyboard_listener, args=(timer,))
    
        timer_thread.start()
        k_thread.start()
        print("\n")

        while not timer.finished:
            if msvcrt.kbhit():  # check if a key was pressed
                cmd = msvcrt.getwch().lower()  # get the character
                if cmd == "p":
                    timer.pause()
                    print("\nTimer paused")
                elif cmd == "r":
                    timer.resume()
                    print("\nTimer resumed")
                elif cmd == "q":
                    timer.pause()
                    timer.finished = True
                    print("\nTimer stopped early")
                    break
            time.sleep(0.1)  # avoid CPU spinning
        # if self.finished:
        #     mins, secs = divmod(0, 60)
        #     sys.stdout.write(f"\033[FTime left: {mins}:{secs:02d}  \n")
        #     sys.stdout.flush()
        #     break

        timer_thread.join()  # Wait for timer to finish
        k_thread.join()
        end = utils.now_utc_ts()

        # Log session
        log_session(session_id, start, end, category)
        duration = end - start
        logger.info(f"Session saved: {session_id} ({duration}s) in category: {category}")
        print(f"Session saved: {session_id} for ({duration}s) in category: {category}\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
