# module for fetching and editing data
import db

def get_user(user_id):
    sql = "SELECT username, developer FROM Users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else []

def get_reviews(user_id):
    sql = """SELECT R.id, R.game_id, G.title AS game_title, R.sent_at, R.content
            FROM Reviews R, Games G
            WHERE G.id = R.game_id AND R.user_id = ?
            ORDER BY R.sent_at DESC"""
    return db.query(sql, [user_id])

def get_games(user_id):
    sql = """SELECT id, title, uploaded_at, description
            FROM Games
            WHERE user_id = ?
            ORDER BY uploaded_at DESC"""
    return db.query(sql, [user_id])