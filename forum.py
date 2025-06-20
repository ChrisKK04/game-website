import db

# this global variable changes the default sql time zone from UTC+0 to UTC+3
# it can be freely changed
TIME = '+3 hours'

# all database queries relating to the forum

def get_classes(game_id): # gets all of an id-specified games classes
    sql = "SELECT title, value FROM Game_classes WHERE game_id = ? ORDER BY LOWER(value)"
    result = db.query(sql, [game_id])

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def get_all_classes(): # gets all of the classes from the database into a dictionary
    sql = "SELECT title, value FROM classes ORDER BY LOWER(value)"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def get_all_game_classes(): # gets the classes for every game into a dictionary all_game_classes[game_id] = classes
    sql = "SELECT game_id, title, value FROM Game_classes"
    result = db.query(sql)
    
    all_game_classes = {}
    for game_id, title, value in result:
        if game_id not in all_game_classes:
            all_game_classes[game_id] = {}
        if title not in all_game_classes[game_id]:
            all_game_classes[game_id][title] = []
        all_game_classes[game_id][title].append(value)

    return all_game_classes

def get_images(game_id): # gets all of the images for a game
    sql = "SELECT id from Images WHERE game_id = ?"
    return db.query(sql, [game_id])

def get_image(image_id): # gets the id-specified image
    sql = "SELECT image FROM Images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

def get_games(page, page_size): # fetches all of the games and their info
    sql = """SELECT G.id, G.title, G.description, COUNT(R.id) total, G.uploaded_at, G.user_id, U.username,
            ROUND(1.0*SUM(R.score) / COUNT(R.id), 1) AS average
            FROM Games G LEFT JOIN Reviews R ON G.id = R.game_id LEFT JOIN Users U on G.user_id = U.id
            GROUP BY G.id
            ORDER BY G.id DESC
            LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_game(game_id): # fetches an id-specified game
    sql = """SELECT G.id, G.title, G.description, G.uploaded_at, G.user_id, U.username
            FROM Games G, Users U
            WHERE G.id = ? AND G.user_id = U.id"""
    result = db.query(sql, [game_id])
    return result[0] if result else None # none if no matches

def get_average_score(game_id): # fetches an id-specified games average user-score
    sql = """SELECT ROUND(1.0*SUM(R.score) / COUNT(R.id), 1) AS average
            FROM Games G, Reviews R
            WHERE G.id = ? AND R.game_id = G.id"""
    result = db.query(sql, [game_id])
    return result[0] if result else None # none if no matches

def add_game(title, description, user_id, classes, images): # adds a game
    sql = f"""INSERT INTO Games (title, description, uploaded_at, user_id)
            VALUES (?, ?, datetime('now', '{TIME}'), ?)"""
    db.execute(sql, [title, description, user_id])

    game_id = db.last_insert_id()

    sql = "INSERT INTO Game_classes (game_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [game_id, class_title, class_value])
    
    sql = "INSERT INTO Images (game_id, image) VALUES (?, ?)"
    for image in images:
        db.execute(sql, [game_id, image])

    return game_id

def get_reviews(game_id): # fetches all reviews for an id-specified game
    sql = """SELECT R.id, R.content, R.sent_at, R.user_id, U.username, R.score
            FROM Reviews R, Users U
            WHERE R.user_id = U.id AND R.game_id = ?
            ORDER BY R.sent_at DESC"""
    return db.query(sql, [game_id])

def new_review(content, user_id, game_id, score): # adds a new review for a game
    sql = f"""INSERT INTO Reviews (content, sent_at, user_id, game_id, score)
            VALUES (?, datetime('now', '{TIME}'), ?, ?, ?)"""
    db.execute(sql, [content, user_id, game_id, score])

def get_review(review_id): # returns a review's id and contents with it's id
    sql = "SELECT id, game_id, content, user_id, score FROM Reviews WHERE id = ?"
    result = db.query(sql, [review_id])
    return result[0] if result else None # none if no matches

def edit_review(review_id, content, score): # updates a review
    sql = "UPDATE Reviews SET content = ?, score = ? WHERE id = ?"
    db.execute(sql, [content, score, review_id])

def delete_review(review_id): # deletes a review
    sql = "DELETE FROM Reviews WHERE id = ?"
    db.execute(sql, [review_id])

def edit_game(game_id, title, description, classes, delete_images, new_images): # updates a game
    sql = "UPDATE Games SET title = ?, description = ? WHERE id = ?"
    db.execute(sql, [title, description, game_id])

    sql = "DELETE FROM Game_classes WHERE game_id = ?"
    db.execute(sql, [game_id])
    sql = "INSERT INTO Game_classes (game_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [game_id, class_title, class_value])

    sql = "DELETE FROM Images WHERE id = ?"
    for image_id in delete_images:
        db.execute(sql, [image_id])

    sql = "INSERT INTO Images (game_id, image) VALUES (?, ?)"
    for image in new_images:
        db.execute(sql, [game_id, image])

def delete_game(game_id): # deletes a game
    sql = "DELETE FROM Games WHERE id = ?"
    db.execute(sql, [game_id])

def game_count(): # amount of games in the database
    sql = "SELECT COUNT(id) FROM Games"
    return db.query(sql)[0][0]