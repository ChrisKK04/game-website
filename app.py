import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db, forum

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    games = forum.get_games()
    return render_template("index.html", games=games)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "ERROR: The passwords do not match"
    
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO Users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "ERROR: The username is taken"
    
    session["username"] = username # The user will be logged in automatically when an account is made
    session["user_id"] = db.last_insert_id() # fetch the id
    
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash, id FROM Users WHERE username = ?"
    query = db.query(sql, [username])
    password_hash = query[0][0]
    user_id = query[0][1]

    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = user_id
        return redirect("/")
    else:
        return "ERROR: Wrong password or username"
    
@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/new_game", methods=["POST"])
def new_game():
    title = request.form["title"]
    description = request.form["description"]
    user_id = session["user_id"]

    print(title, description, user_id)

    thread_id = forum.add_game(title, description, user_id)
    return redirect("/game/" + str(thread_id))

@app.route("/game/<int:game_id>")
def show_game(game_id):
    game = forum.get_game(game_id)
    reviews = forum.get_reviews(game_id)
    return render_template("game.html", game=game, reviews=reviews)

@app.route("/new_review", methods=["POST"])
def new_review():
    content = request.form["content"]
    user_id = session["user_id"]
    game_id = request.form["game_id"]

    forum.new_review(content, user_id, game_id)
    return redirect("/game/" + str(game_id))

@app.route("/edit/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    review = forum.get_review(review_id)

    if request.method == "GET":
        return render_template("edit_review.html", review=review)

    if request.method == "POST":
        content = request.form["content"]
        forum.update_review(review["id"], content)
        return redirect("/game/" + str(review["game_id"]))

@app.route("/delete/<int:review_id>", methods=["GET", "POST"])
def delete_review(review_id):
    review = forum.get_review(review_id)

    if request.method == "GET":
        return render_template("delete_review.html", review=review)
    
    if request.method == "POST":
        if "delete" in request.form:
            forum.remove_review(review["id"])
        return redirect("/game/" + str(review["game_id"]))