"""Module with searching related SQL-queries."""

import db

# all database queries relating to searching

def games(title_sql, description, game_score_type, game_score, publisher, classes):
    sql = """SELECT G.id game_id, G.title, G.description, U.id publisher_id,
                    U.username publisher, G.uploaded_at, COUNT(R.id) total,
                    ROUND(1.0*SUM(R.score) / COUNT(R.id), 1) average
             FROM Games G
             LEFT JOIN Users U ON G.user_id = U.id
             LEFT JOIN Reviews R ON G.id = R.game_id
             WHERE G.title LIKE ? AND G.description LIKE ? AND U.username LIKE ?
             GROUP BY G.id"""
    parameters = ["%" + title_sql + "%", "%" + description + "%", "%" + publisher + "%"]
    if game_score_type == 1:
        sql += " HAVING ROUND(1.0*SUM(R.score) / COUNT(R.id), 1) >= ?"
        parameters.append(game_score)
    elif game_score_type == 2:
        sql += " HAVING ROUND(1.0*SUM(R.score) / COUNT(R.id), 1) <= ?"
        parameters.append(game_score)

    sql += " ORDER BY G.id DESC"
    games_list = db.query(sql, parameters) # get the matching games (no classes)

    game_ids = [game['game_id'] for game in games_list] # get the ids of the matching games
    set_classes = set(classes) # make a set of the classes in the search
    valid_game_ids = [] # list of game ids for which the games have the classes in the search

    result_classes = {} # classes for games - result_classes[game_id] = [<list of classes>]
    for game_id in game_ids:
        set_classes_check = set() # make a set for class comparing
        sql = "SELECT title, value FROM Game_classes WHERE game_id = ? ORDER BY LOWER(value)"
        result = db.query(sql, [game_id])
        for title, value in result:
            if game_id not in result_classes:
                result_classes[game_id] = {}
            if title not in result_classes[game_id]:
                result_classes[game_id][title] = []
            if value not in result_classes[game_id][title]:
                result_classes[game_id][title].append(value)
            set_classes_check.add((title, value)) # add the classes title and value
        if game_id not in result_classes: # if the game doesn't have any classes
            result_classes[game_id] = "no_classes"
        # if the game's classes are a superset of the classes in the search = matches search
        if set_classes <= set_classes_check:
            valid_game_ids.append(game_id)

    # games = games that match the search (no classes)
    # result_classes = the classes for every game in games
    # valid_game_ids = the ids of games that include the classes of the search
    return (games_list, result_classes, valid_game_ids)

def reviews(content, review_score_type, review_score):
    sql = """SELECT U.id user_id, U.username, G.id game_id, G.title game_title,
                    R.id review_id, R.sent_at, R.content, R.score
             FROM Reviews R
             LEFT JOIN Games G ON R.game_id = G.id
             LEFT JOIN Users U ON R.user_id = U.id
             WHERE R.content LIKE ?"""
    if review_score_type == 0: # any score
        sql += " ORDER BY R.sent_at"
        return db.query(sql, ["%" + content + "%"])
    if review_score_type == 1: # above the given score
        sql += " AND R.score >= ? ORDER BY R.sent_at"
        return db.query(sql, ["%" + content + "%", review_score])
    if review_score_type == 2: # below the given score
        sql += " AND R.score <= ? ORDER BY R.sent_at"
        return db.query(sql, ["%" + content + "%", review_score])

    return []

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

    return []
