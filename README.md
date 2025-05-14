# A website for posting games and reviews

## Functions

* Creating an account and logging in
* Adding posts describing games with photos and categories (action, racing, simulator, etc.)
* Seeing and searching the posts of other users
* Account pages which list a given accounts posts and certain statistics about the account
* Leaving reviews on games alongside a score

## Downloading the website/app

Download the `flask`-library:
```
$ pip install flask
```

Create tables and initial data:
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

You can also optionally add pre-made data for testing
```
$ sqlite3 database.db < pre_data.sql
```