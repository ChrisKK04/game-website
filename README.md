# A website for posting games and reviews

## Current features

* Creating an account and logging in
* Adding posts describing games
* Leaving reviews on games alongside a score
* Editing and deleting reviews and games
* Seeing the posts of other users
* Account pages which list a given accounts posts and certain statistics about the account
* Only developers can post games and only users can post reviews
* Two Python scripts for populating the database with data
* Games have optional categories and photos
* Game, review and user search
* CSS styling

## Upcoming features

* An actual name for the website

## Using the website (Linux/Windows with Bash)

(The website requires Python https://www.python.org/ and SQLite https://sqlite.org/ to function).

Start by creating a folder for the website.

Then run the following commands in the terminal whilst being in the created folder:
```
$ python3 -m venv venv                   # creates a virtual python environment to download packages into
$ source venv/bin/activate               # activates the virtual environment (Linux)
$ source venv/Script/activate            # activates the virtual environment (Windows with Bash)
$ pip install flask                      # downloads and installs flask
$ sqlite3 database.db < schema.sql       # creates database.db and adds tables
$ sqlite3 database.db < init.sql         # inserts classes
```

After running the commands, the database will be empty. You can insert some data for testing by running a python script.

pre_data.py: populates the database with some games, users and reviews.

Login to accounts:
```
Username: Jason, RampageGames            # uppercase starts
Password: jason, rampagegames            # all lowercase
```

seed.py: populates the database with large amounts of data for peformance testing.

Time zones:
forum.py and pre_data.py have a global time zone variable called TIME.
The variable can be edited, but it defaults to UTC+3.
```
TIME = '+3 hours'
```

You can use the website in the terminal with:

(A fetch-to-load time measurement is also displayed in the terminal).
```
$ flask run                              # runs the website
$ ctrl + c                               # closes the website
```

As of 19.6.2025 development is still in progress.