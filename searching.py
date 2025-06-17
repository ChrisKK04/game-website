import db

# all database queries relating to searching

def games():
    pass

def reviews():
    pass
    
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