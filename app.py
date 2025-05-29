import sqlite3
from flask import Flask
from flask import redirect, render_template, abort, make_response, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db, forum, users, searching

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login(): # checks login
    if "user_id" not in session:
        abort(403)

def valid_game(title, description): # checks game title and description size requirements
    if not title or not description or len(title) > 100 or len(description) > 5000:
        return True
    
def valid_review(content, score): # checks review content size requirements
    if not content or len(content) > 5000 or score not in ["1", "2", "3", "4", "5"]:
        return True

@app.route("/") # homepage
def index():
    games = forum.get_games()
    return render_template("index.html", games=games)

@app.route("/register") # register page
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"]) # register page handler
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    developer = request.form["developer"]

    if not username or not password1 or not developer or len(username) > 50 or len(password1) > 50:
        abort(403)

    if password1 != password2:
        return "ERROR: The passwords do not match"
    
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO Users (username, password_hash, developer) VALUES (?, ?, ?)"
        db.execute(sql, [username, password_hash, developer])
    except sqlite3.IntegrityError:
        return "ERROR: The username is taken"
    
    session["username"] = username # The user will be logged in automatically when an account is made
    session["developer"] = int(developer) # stores whether or not the user is a developer
    session["user_id"] = db.last_insert_id() # fetch the id
    
    return redirect("/")

@app.route("/login", methods=["POST"]) # login handler
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash, id, developer FROM Users WHERE username = ?"
    query = db.query(sql, [username])
    password_hash = query[0][0]
    user_id = query[0][1]
    developer = query[0][2]

    if check_password_hash(password_hash, password):
        session["username"] = username
        session["developer"] = developer
        session["user_id"] = user_id
        return redirect("/")
    else:
        return "ERROR: Wrong password or username"
    
@app.route("/logout") # logout handler
def logout():
    del session["username"]
    del session["developer"]
    del session["user_id"]
    return redirect("/")

@app.route("/new_game", methods=["POST"])
def new_game():
    require_login()

    title = request.form["title"]
    description = request.form["description"]
    if valid_game(title, description):
        abort(403)

    user_id = session["user_id"]

    thread_id = forum.add_game(title, description, user_id)
    return redirect("/game/" + str(thread_id))

@app.route("/game/<int:game_id>") # game page
def show_game(game_id):
    game = forum.get_game(game_id)
    if not game:
        abort(404)
    average = forum.get_average_score(game_id)
    reviews = forum.get_reviews(game_id)
    return render_template("game.html", game=game, average=average, reviews=reviews)

@app.route("/new_review", methods=["POST"]) # new review handler
def new_review():
    require_login()

    content = request.form["content"]
    score = request.form["score"]
    user_id = session["user_id"]
    if valid_review(content, score):
        abort(403)

    game_id = request.form["game_id"]

    try:
        forum.new_review(content, user_id, game_id, score)
    except sqlite3.IntegrityError:
        abort(403)
        
    return redirect("/game/" + str(game_id))

@app.route("/edit_review/<int:review_id>", methods=["GET", "POST"]) # edit review
def edit_review(review_id):
    require_login()

    review = forum.get_review(review_id)
    if not review:
        abort(404)

    if review["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit_review.html", review=review)

    if request.method == "POST":
        content = request.form["content"]
        score = request.form["score"]
        if valid_review(content, score):
            abort(403)

        forum.edit_review(review["id"], content, score)
        return redirect("/game/" + str(review["game_id"]))

@app.route("/delete_review/<int:review_id>", methods=["GET", "POST"]) # delete review
def delete_review(review_id):
    require_login()

    review = forum.get_review(review_id)
    if not review:
        abort(404)

    if review["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete_review.html", review=review)
    
    if request.method == "POST":
        if "delete" in request.form:
            forum.delete_review(review["id"])
        return redirect("/game/" + str(review["game_id"]))

@app.route("/edit_game/<int:game_id>", methods=["GET", "POST"]) # edit game
def edit_game(game_id):
    require_login()

    game = forum.get_game(game_id)
    if not game:
        abort(404)

    if game["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit_game.html", game=game)
    
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        if valid_game(title, description):
            abort(403)

        forum.edit_game(game["id"], title, description)
        return redirect("/game/" + str(game["id"]))

@app.route("/delete_game/<int:game_id>", methods=["GET", "POST"]) # delete game
def delete_game(game_id):
    require_login()
    
    game = forum.get_game(game_id)
    if not game:
        abort(404)

    if game["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete_game.html", game=game)
    
    if request.method == "POST":
        if "delete" in request.form:
            forum.delete_game(game["id"])
        return redirect("/")
    
@app.route("/user/<int:user_id>") # user page
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(403)
    if user["developer"] == 0: # user
        reviews = users.get_reviews(user_id)
        return render_template("user.html", user=user, reviews=reviews)
    if user["developer"] == 1: # developer
        games = users.get_games(user_id)
        return render_template("user.html", user=user, games=games)
    
@app.route("/update_profile_picture", methods=["GET", "POST"]) # profile picture updating
def add_profile_picture():
    require_login()

    if request.method == "GET":
        return render_template("update_profile_picture.html")
    
    if request.method == "POST":
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            return "ERROR: wrong filetype"
        
        image = file.read()
        if len(image) > 100 * 1024:
            return "ERROR: the image is too big"
        
        user_id = session["user_id"]
        users.update_profile_picture(user_id, image)
        return redirect("/user/" + str(user_id))
    
@app.route("/profile_picture/<int:user_id>") # view a profile picture
def show_profile_picture(user_id):
    image = users.get_profile_picture(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/search") # search page:
def search():
    parameter = request.args.get("parameter") # get the search parameter

    # different parameters will render different results
    if parameter == "title":
        title_value = request.args.get("title_value") # parameter value
        title_results = searching.title(title_value)
        return render_template("search.html", title_results=title_results, title_value=title_value)
    
    if parameter == "description": # etc...
        pass
    
    return render_template("search.html") # if no parameters are given