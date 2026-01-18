from timer import Timer
from logger import logger
import utils
import config
import threading
import msvcrt
import time
import sys
import storage
# Initialize database
storage.init_db()


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
    storage.log_session(session_id, start, end, category)
    duration = end - start
    logger.info(f"Session saved: {session_id} ({duration}s) in category: {category}")
    print(f"Session saved: {session_id} for ({duration}s) in category: {category}\n")
    sys.stdout.flush()


def menu_loop():
    """Main interactive menu for running multiple sessions or querying the database."""
    print("Welcome! Choose an option:\n")

    while True:
        print("\nMain Menu:")
        print("1. Task Timer")
        print("2. Database Queries")
        print("q. Quit")

        choice = input("Select an option: ").strip().lower()

        if choice == "1":
            # Enter the existing task timer loop
            start_productivity_session()
        elif choice == "2":
            database_menu()
        elif choice == "q":
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please try again.")


def database_menu():
    """Submenu for database operations."""
    while True:
        print("\nDatabase Menu:")
        print("1. Show total time per category in the past 24 hours")
        print("2. Show total time per category in the past 7 days")
        print("b. Back to main menu")

        choice = input("Select an option: ").strip().lower()

        if choice == "1":
            period = "day"
        elif choice == "2":
            period = "week"
        elif choice == "b":
            break
        else:
            print("Invalid choice, please try again.")
            continue

        totals, label = storage.get_productive_time(period)

        if totals:
            print(f"\n{label}:")
            for category, duration in totals.items():
                print(f"  {category}: {duration}")
        else:
            print(f"No sessions logged in the {label.lower()}.")

def main():
    logger.info("App started")
    menu_loop()


if __name__ == "__main__":
    main()
