# module for fetching and editing data
import db

def get_user(user_id): # users username and developer status
    sql = """SELECT id, username, developer, image IS NOT NULL has_image
            FROM Users
            WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_reviews(user_id): # users given reviews
    sql = """SELECT R.id, R.game_id, G.title AS game_title, R.sent_at, R.content
            FROM Reviews R, Games G
            WHERE G.id = R.game_id AND R.user_id = ?
            ORDER BY R.sent_at DESC"""
    return db.query(sql, [user_id])

def get_games(user_id): # developers published games
    sql = """SELECT id, title, uploaded_at, description
            FROM Games
            WHERE user_id = ?
            ORDER BY uploaded_at DESC"""
    return db.query(sql, [user_id])

def update_profile_picture(user_id, image): # updates the users profile picture
    sql = "UPDATE Users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id])

def get_profile_picture(user_id): # fetches the users profile picture
    sql = "SELECT image FROM Users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else None