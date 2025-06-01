# module for fetching and editing data
import db

# all database queries relating to searching

def title(title): # game title
    sql = """SELECT G.id, G.title, G.uploaded_at, G.user_id, U.username
            FROM Games G, Users U
            WHERE G.user_id = U.id AND G.title LIKE ?
            ORDER BY G.uploaded_at DESC"""
    return db.query(sql, ["%" + title + "%"])

def review_content(review_content): # review content
    sql = """SELECT R.id, R.game_id, G.title AS game_title, R.sent_at, R.content, R.score
            FROM Reviews R, Games G
            WHERE G.id = R.game_id AND R.content LIKE ?
            ORDER BY R.sent_at DESC"""
    return db.query(sql, ["%" + review_content + "%"])

# description - game description
# tags - multiple
# average score - above a score for a game
# developer - name
# user - name