# module for fetching and editing data
import db

def get_games(): # fetches all of the games and their info
    sql = """SELECT G.id, G.title, G.description, COUNT(R.id) total, G.uploaded_at, G.user_id, U.username
            FROM Games G LEFT JOIN Reviews R ON G.id = R.game_id, Users U
            WHERE G.user_id = U.id
            GROUP BY G.id
            ORDER BY G.id DESC"""
    return db.query(sql)

def get_game(game_id): # fetches an id-specified game
    sql = """SELECT G.id, G.title, G.description, G.uploaded_at, G.user_id, U.username
            FROM Games G, Users U
            WHERE G.id = ? AND G.user_id = U.id"""
    result = db.query(sql, [game_id])
    return result[0] if result else None # none if no matches

def add_game(title, description, user_id): # adds a game
    sql = """INSERT INTO Games (title, description, uploaded_at, user_id)
            VALUES (?, ?, datetime('now'), ?)"""
    db.execute(sql, [title, description, user_id])
    return db.last_insert_id()

def get_reviews(game_id): # fetches all reviews for an id-specified game
    sql = """SELECT R.id, R.content, R.sent_at, R.user_id, U.username, R.score
            FROM Reviews R, Users U
            WHERE R.user_id = U.id AND R.game_id = ?"""
    return db.query(sql, [game_id])

def new_review(content, user_id, game_id, score): # adds a new review for a game
    sql = """INSERT INTO Reviews (content, sent_at, user_id, game_id, score)
            VALUES (?, datetime('now'), ?, ?, ?)"""
    db.execute(sql, [content, user_id, game_id, score])

def get_review(review_id): # returns a review's id and contents with it's id
    sql = "SELECT id, game_id, content, user_id FROM Reviews WHERE id = ?"
    result = db.query(sql, [review_id])
    return result[0] if result else None # none if no matches

def edit_review(review_id, content): # updates a review
    sql = "UPDATE Reviews SET content = ? WHERE id = ?"
    db.execute(sql, [content, review_id])

def delete_review(review_id): # deletes a review
    sql = "DELETE FROM Reviews WHERE id = ?"
    db.execute(sql, [review_id])

def edit_game(game_id, title, description): # updates a game
    sql = "UPDATE Games SET title = ?, description = ? WHERE id = ?"
    db.execute(sql, [title, description, game_id])

def delete_game(game_id): # deletes a game
    sql = "DELETE FROM Games WHERE id = ?"
    db.execute(sql, [game_id])