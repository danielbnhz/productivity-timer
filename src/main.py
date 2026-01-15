from timer import Timer
from storage import init_db, log_session
from logger import logger
import utils
import config
import threading
import msvcrt
import time
import sys

# Initialize database
init_db()


def keyboard_listener(timer):
    """Listen for keyboard input to pause, resume, or stop the timer."""
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


def get_minutes_input():
    while True:
        try:
            minutes = int(input("Minutes: "))
            if minutes <= 0:
                raise ValueError
            return minutes
        except ValueError:
            print("Please enter a positive number")


def get_category_input():
    while True:
        category = input("Please input task category: ").strip()
        if category in config.CATEGORIES:
            return category
        print(f"Please enter a valid category from: {config.CATEGORIES}")


def start_productivity_session():
    """Handles a single timer session from start to finish."""
    session_id = utils.generate_session_id()
    start = utils.now_utc_ts()
    logger.info(f"Session started: {session_id}")

    minutes = get_minutes_input()
    category = get_category_input()

    # Create and start timer
    timer = Timer(minutes)
    timer.finished = False

    timer_thread = threading.Thread(target=timer.start)
    k_thread = threading.Thread(target=keyboard_listener, args=(timer,))

    timer_thread.start()
    k_thread.start()

    # Monitor keypresses in main thread for user feedback
    while not timer.finished:
        if msvcrt.kbhit():
            cmd = msvcrt.getwch().lower()
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
        time.sleep(0.1)

    timer_thread.join()
    k_thread.join()
    end = utils.now_utc_ts()

    # Log session
    log_session(session_id, start, end, category)
    duration = end - start
    logger.info(f"Session saved: {session_id} ({duration}s) in category: {category}")
    print(f"Session saved: {session_id} for ({duration}s) in category: {category}\n")
    sys.stdout.flush()


def menu_loop():
    """Main interactive menu for running multiple sessions."""
    print("Running program\n")
    run_sessions = True
    while run_sessions:
        start_task = input("Start task? (y/n): ").strip().lower()
        if start_task != "y":
            run_sessions = False
            continue
        start_productivity_session()


def main():
    logger.info("App started")
    menu_loop()


if __name__ == "__main__":
    main()
