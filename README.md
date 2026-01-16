## A productivity app based on Python, currently under construction

The app is currently functional. After cloning, just run
```bash
    python main.py
```
This will be elaborated on as the program grows more developed

Current the app will write a database according to the tasks set in config.py
When you initiate the app. It will present you with a prompt to menu to for options of either
querying the database or running the timer. It currently doesn't support inputting your
own hours. 

The program will then prompt how many minutes you wish to work for. And then it
will ask for the category for the task. 

When finished, you can run sqlite3 commands on the database to gauge your productivity

the app will be elaborated to include more database query types. And also the ability to
input tasks without the task counter

the app will eventually be able to show patterns of productivity through weeks and months

the config allows you to select your own categories. 