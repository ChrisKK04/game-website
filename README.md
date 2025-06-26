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
$ source venv/Scripts/activate           # activates the virtual environment (Windows with Bash)
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

Secret key:
the secret key (session key) of the website can be set in config.py (it has a default value).
```
secret_key = ...
```

You can use the website in the terminal with:

(A fetch-to-load time measurement is also displayed in the terminal).
```
$ flask run                              # runs the website
$ ctrl + c                               # closes the website
```

# Website performance with large datasets

A large dataset was generated with the script in seed.py. The script populates the website's database with test data for performance testing.

## Performance without optimizations

**Parameters:**
* `user_count = 1000`
* `game_count = 10⁵`
* `review_count = 10⁶`
* `game_classes = 10⁵`

**Result:**
The homepage loading time averaged around **14 s**.

## Optimizations done
* Added pagination to the homepage
* Added indexes to the database

## Performance after optimizations

**Parameters:**
* `user_count = 1000`
* `game_count = 10⁵`
* `review_count = 10⁶`
* `game_classes = 10⁵`

**Result:**
The homepage's (/1) loading time averaged around **0.5s** and page 10000's (/10000) loading time averaged around **3-4s**. Loading pages with higher indexes takes longer due to pagination being based off using limit/offset in the SQL queries, which with high page values has to skip over lots of rows.