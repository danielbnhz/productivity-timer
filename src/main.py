from timer import Timer
from storage import init_db, log_session
import uuid
import time


init_db()


def main():
    print("Running program \n")
    while input("Initiate task counter? (answer y or n) \n") == "y":
        session_id = str(uuid.uuid4())
        start = int(time.time())
        minutes = int(input("Enter the minutes you want to be productive for \n"))
        Timer(minutes)
        end = int(time.time())
        log_session(session_id, start, end)



if __name__ == "__main__":
    main()
