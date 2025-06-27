"""Module with user related SQL-queries."""

import sqlite3
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

import db

# all database queries relating to users

def get_all_dev_game_classes(user_id): # gets the classes for every game for a single developer
    sql = """SELECT A.game_id AS game_id, A.title AS title, A.value AS value
             FROM Game_classes A LEFT JOIN Games B ON A.game_id = B.id
             WHERE B.user_id = ?"""
    result = db.query(sql, [user_id])

    all_dev_game_classes = {}
    for game_id, title, value in result:
        if game_id not in all_dev_game_classes:
            all_dev_game_classes[game_id] = {}
        if title not in all_dev_game_classes[game_id]:
            all_dev_game_classes[game_id][title] = []
        all_dev_game_classes[game_id][title].append(value)

    return all_dev_game_classes

def create_user(username, password, developer): # adding a user to the database
    password_hash = generate_password_hash(password)
    try:
        sql = "INSERT INTO Users (username, password_hash, developer) VALUES (?, ?, ?)"
        db.execute(sql, [username, password_hash, developer])
        return True
    except sqlite3.IntegrityError:
        return False

def check_login(username, password): # checks the login of a user
    sql = "SELECT password_hash, id AS user_id, developer FROM Users WHERE username = ?"
    result = db.query(sql, [username])
    if result:
        return result[0] if check_password_hash(result[0]["password_hash"], password) else None
    return None


def get_user(user_id): # users username and developer status
    sql = """SELECT id, username, developer, image IS NOT NULL has_image
            FROM Users
            WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_reviews(user_id): # users given reviews
    sql = """SELECT R.id, R.game_id, G.title AS game_title, R.sent_at, R.content, R.score
            FROM Reviews R, Games G
            WHERE G.id = R.game_id AND R.user_id = ?
            ORDER BY R.sent_at DESC"""
    return db.query(sql, [user_id])

def get_games(user_id): # developers published games
    sql = """SELECT G.id, G.title, G.description, COUNT(R.id) total,
                    G.uploaded_at, G.user_id, U.username,
                    ROUND(1.0*SUM(R.score) / COUNT(R.id), 1) AS average
            FROM Games G LEFT JOIN Reviews R ON G.id = R.game_id, Users U
            WHERE G.user_id = U.id AND G.user_id = ?
            GROUP BY G.id
            ORDER BY G.id DESC"""
    return db.query(sql, [user_id])

def update_profile_picture(user_id, image): # updates the users profile picture
    sql = "UPDATE Users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id])

def get_profile_picture(user_id): # fetches the users profile picture
    sql = "SELECT image FROM Users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else None
