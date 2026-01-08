from timer import Timer
# from storage import Storage
# from logger import Logger

# logger = Logger()
# storage = Storage()


def main():
    print("Running program \n")
    while input("Initiate task counter? (answer y or n) \n") == "y":
        minutes = int(input("Enter the minutes you want to be productive for \n"))
        Timer(minutes)




if __name__ == "__main__":
    main()