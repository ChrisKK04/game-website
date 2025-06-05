import random
import sqlite3

# the script doesn't include images for users or games
# database.db and the tables in it have to exist before running the script
    # if database.db doesn't exist:
        # $ database.db < schema.sql
# logging in to the generated users isn't possible
    # (because the passwords aren't saved as hashes and the app checks for hashes)
        # (generating the hashes takes too long for testing)

db = sqlite3.connect("database.db")

db.execute("DELETE FROM Users")
db.execute("DELETE FROM Games")
db.execute("DELETE FROM Reviews")

user_count = 1000 # 1/2 developers 1/2 reviews (1 - 500 developers 501 - 1000 reviewers)
game_count = 10**5
review_count = 10**6

for i in range(1, user_count + 1): # insert users
    developer = 1 if i < 501 else 0
    db.execute("""INSERT INTO Users (username, password_hash, developer)
                  VALUES (?, ?, ?)""",
               ["user" + str(i), "user" + str(i), developer])
    
for i in range(1, game_count + 1): # insert games
    user_id = random.randint(1, user_count // 2)
    db.execute("""INSERT INTO Games (title, description, uploaded_at, user_id)
                  VALUES (?, ?, datetime('now'), ?)""",
               ["game" + str(i), "game" + str(i), user_id])

for i in range(1, review_count): # insert reviews
    user_id = random.randint(501, user_count)
    game_id = random.randint(1, game_count)
    score = random.choice([1, 2, 3, 4, 5])
    db.execute("""INSERT INTO Reviews (content, sent_at, user_id, game_id, score)
                  VALUES (?, datetime('now'), ?, ?, ?)""",
                  ["message" + str(i), user_id, game_id, score])
    
db.commit()
db.close()