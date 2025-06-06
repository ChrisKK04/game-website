# A website for posting games and reviews

## Current features

* Creating an account and logging in
* Adding posts describing games
* Leaving reviews on games alongside a score
* Editing and deleting reviews and games
* Seeing and searching (game title or review content) the posts of other users
* Account pages which list a given accounts posts and certain statistics about the account
* Only developers can post games and only users can post reviews
* A seed.py script for testing the website with large quantities of data

## Upcoming features

* Game photos and categories
* More search parameters (game description, average score, tags, developers, etc.)
* Better accessibility
* CSS for styling
* QOL-updates
* An actual name for the website

## Using the website (Linux)

Start by creating a folder for the website.

Then run the following commands in the terminal whilst being in the created folder:
```
$ python3 -m venv venv                   # creates a virtual environment to download packages into
$ source venv/bin/activate               # activates the virtual environment
$ pip install flask                      # downloads and installs flask
$ sqlite3 database.db < schema.sql       # create database.db and add tables
$ sqlite3 database.db < init.sql         # insert categories  (future feature)
```

After running the commands, the database will be empty. You can insert some data for testing by running a python script.

pre_data.py: populates the database with some users, games and reviews

Login to accounts:
```
Username: Jason, RampageGames            # uppercase starts
Password: jason, rampagegames            # all lowercase
```

seed.py: populates the database with large amounts of data for peformance testing

You can now use the website in the terminal with:

(A fetch-to-load time measurement is also shown in the terminal).
```
$ flask run                              # runs the website
$ ctrl + c                               # closes the website
```

As of 6.6.2025 development is still in progress.