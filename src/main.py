from timer import Timer
from storage import init_db, log_session
from logger import logger
import uuid
import time


init_db()


def main():
    logger.info("App started")

    print("Running program \n")
    while input("Initiate task counter? (answer y or n) \n") == "y":
        session_id = str(uuid.uuid4())
        logger.info(f"Session started: {session_id}")

        start = int(time.time())
        minutes = int(input("Enter the minutes you want to be productive for \n"))
        Timer(minutes)
        end = int(time.time())
        log_session(session_id, start, end)
        duration = end - start 
        logger.info(f"Session saved: {session_id} ({duration}s)")



if __name__ == "__main__":
    main()
