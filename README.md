# A website for posting games and reviews

## Functions

* The user can create an account and login
* The user can add a post describing their game
* The user can add photos to their posts
* The user can see and search the posts of other users
* The website has account pages which list a given accounts posts and certain statistics about the account
* The user can select categories for their posted games (action, racing, simulator, etc.)
* Users can leave written reviews on games posted by other users alongside giving the game a score

## Downloading the website/app

Download the `flask`-library:
```
$ pip install flask

or

$ sudo apt intstall python3-flask
```

Create the tables and initial data:
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

You can also optionally add pre-made data for testing
```
$ sqlite3 database.db < pre_data.sql
```

You can run the website/app with:
```
$ flask run
```

You can then view the website/app in the browser by inputting the given IP-address.
