# A website for posting games and reviews

## Functions

* Creating an account and logging in
* Adding posts describing games with photos and categories (action, racing, simulator, etc.)
* Editing and deleting reviews and games
* Seeing and searching the posts of other users
* Account pages which list a given accounts posts and certain statistics about the account
* Leaving reviews on games alongside a score
* Only developers can post games and only users can post reviews

## Using the website (Linux)

Start by creating a folder for the website.

Then run the following commands in the terminal whilst being in the created folder:
```
$ python3 -m venv venv                # creates a virtual environment to download packages into
$ source venv/bin/activate            # activates the virtual environment
$ pip install flask                   # downloads and installs flask
```

The files include a database file with pre-made data for testing.

You can also use an empty database by renaming or deleting database.db and entering the following commands into the terminal whilst being in the website's folder:
```
$ sqlite3 database.db < schema.sql     # add tables
$ sqlite3 database.db < init.sql       # insert categories
```

You can now use website in the terminal with:
```
flask run                              # runs the website
ctrl + c                               # closes the website
```