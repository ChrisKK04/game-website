# A website for posting games and reviews

## Current features

* Creating an account and logging in
* Adding posts describing games
* Leaving reviews on games alongside a score
* Editing and deleting reviews and games
* Seeing and searching (game title or review content) the posts of other users
* Account pages which list a given accounts posts and certain statistics about the account
* Only developers can post games and only users can post reviews

## Upcoming features

* Game photos and categories
* More search parameters (game description, average score, tags, developers, etc.)
* Support for usage with large amounts of data
* A seed.py file for testing with large amounts of data
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
```

The files include a database.db file with pre-made data for testing.

Login to accounts:
```
Username: Jason, RampageGames            # uppercase starts
Password: jason, rampagegames            # all lowercase
```

You can also use an empty database by renaming or deleting database.db and entering the following commands into the terminal whilst being in the website's folder:
```
$ sqlite3 database.db < schema.sql       # create database.db and add tables
$ sqlite3 database.db < init.sql         # insert categories  (future feature)
```

You can now use the website in the terminal with:
```
$ flask run                              # runs the website
$ ctrl + c                               # closes the website
```