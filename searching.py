import db

# all database queries relating to searching

def games():
    pass

def reviews(content, review_score_type, review_score):
    sql = """SELECT U.id user_id, U.username, G.id game_id, G.title game_title, R.id review_id, R.sent_at, R.content, R.score
             FROM Reviews R
             LEFT JOIN Games G ON R.game_id = G.id
             LEFT JOIN Users U ON R.user_id = U.id
             WHERE R.content LIKE ?"""
    if review_score_type == 0: # any score
        sql += " ORDER BY R.sent_at"
        return db.query(sql, ["%" + content + "%"])
    elif review_score_type == 1: # above the given score
        sql += " AND R.score >= ? ORDER BY R.sent_at"
        return db.query(sql, ["%" + content + "%", review_score])
    elif review_score_type == 2: # below the given score
        sql += " AND R.score <= ? ORDER BY R.sent_at"
        return db.query(sql, ["%" + content + "%", review_score])
    
def users(username, user_type):
    if user_type == 2: # any
        sql = """SELECT id, username, developer, image
                 FROM Users
                 WHERE username LIKE ?
                 ORDER BY developer DESC, username"""
        return db.query(sql, ["%" + username + "%"])

    if user_type == 0: # reviewer
        sql = """SELECT id, username, developer, image
                 FROM Users
                 WHERE developer = 0 AND username LIKE ?
                 ORDER BY username"""
        return db.query(sql, ["%" + username + "%"])
    
    if user_type == 1: # developer
        sql = """SELECT id, username, developer, image
                 FROM Users
                 WHERE developer = 1 AND username LIKE ?
                 ORDER BY username"""
        return db.query(sql, ["%" + username + "%"])