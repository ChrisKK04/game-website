# module for fetching and editing data
import db

# all database queries relating to searching

def title(title): # game title
    sql = """SELECT G.id, G.title, G.uploaded_at, G.user_id, U.username
            FROM Games G, Users U
            WHERE G.user_id = U.id AND G.title LIKE ?
            ORDER BY G.uploaded_at DESC"""
    return db.query(sql, ["%" + title + "%"])

# description - game description
# tags - multiple
# review - content
# average score - above a score for a game
# developer - name
# user - name