"""A python script to insert pre-made data into the database."""

import sqlite3
from werkzeug.security import generate_password_hash

import config

# This is a python script that inserts custom data into database.db for testing.
# the script doesn't include images for users or games
# database.db and the tables in it have to exist before running the script
    # if database.db doesn't exist:
        # $ sqlite3 database.db < schema.sql
        # $ sqlite3 database.db < init.sql

# this global variable changes the default sql time zone from UTC 0 to UTC +3
# it can be freely changed
TIME = config.TIME

db = sqlite3.connect("database.db")

db.execute("DELETE FROM Users")
db.execute("DELETE FROM Games")
db.execute("DELETE FROM Reviews")
db.execute("DELETE FROM Game_classes")
db.execute("DELETE FROM Images")

users = [["RampageGames", "rampagegames", 1],
         ["Pipe", "pipe", 1],
         ["HeroicGames", "heroicgames", 1],
         ["Jason", "jason", 0],
         ["Emily", "emily", 0]]

games = [["Falorant", """Falorant is a team-based first-person tactical hero shooter set in the near future.
          Players play as one of a set of Agents, characters based on several countries and cultures
          around the world. In the main game mode, players are assigned to either the attacking or
          defending team with each team having five players on it.""", 1],
          ["League of Ripoffs", """League of Ripoffs is a team-based strategy game where two teams of
           five powerful champions face off to destroy the other's base. Choose from over 140
           champions to make epic plays, secure kills, and take down towers as you battle
           your way to victory.""", 1],
          ["Counter the DMCA 2", """Welcome to Counter the DMCA 2, the next evolution of the world's
           most legendary competitive shooter. Built on the powerful Closing 2 engine, CDMCA2 brings
           breathtaking visuals, hyper-responsive gameplay, and reimagined classics to life — all
           for free.""", 2],
           ["Fortress Fight", """Join the worldwide sensation that blends high-speed combat with
            creative construction. In FortressFight Battle Royale, 100 players fight to be the last
            one standing — scavenging weapons, building defenses, and outlasting the competition
            in a constantly evolving world.""", 3]]

reviews = [["I love the new lighting and gun feel!", 4, 3, 5],
           ["Similar to CDMCA 2 but with abilities.", 4, 1, 3],
           ["wayyyyyyy better than CDMCA 2", 5, 1, 5],
           ["The game has way too many characters.", 5, 2, 2]]

classes = [[1, "Category", "action"],
           [1, "Category", "competitive"],
           [2, "Category", "action"],
           [2, "Category", "competitive"],
           [3, "Category", "action"],
           [3, "Category", "competitive"],
           [4, "Category", "action"],
           [4, "Category", "competitive"],]

for username, password, developer in users: # inserts the users
    password_hash = generate_password_hash(password)
    sql = """INSERT INTO Users (username, password_hash, developer)
              VALUES (?, ?, ?)"""
    db.execute(sql, [username, password_hash, developer])

for title, description, user_id in games: # inserts the games
    sql = f"""INSERT INTO Games (title, description, uploaded_at, user_id)
              VALUES (?, ?, datetime('now', '{TIME}'), ?)"""
    db.execute(sql, [title, description, user_id])

for content, user_id, game_id, score in reviews: # inserts the reviews
    sql = f"""INSERT INTO Reviews (content, sent_at, user_id, game_id, score)
              VALUES (?, datetime('now', '{TIME}'), ?, ?, ?)"""
    db.execute(sql, [content, user_id, game_id, score])

for game_id, title, value in classes: # inserts the categories for games
    sql = """INSERT INTO Game_classes (game_id, title, value)
               VALUES (?, ?, ?)"""
    db.execute(sql, [game_id, title, value])

db.commit()
db.close()
