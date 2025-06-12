import sqlite3
import math
import time
import secrets
from flask import Flask
from flask import redirect, render_template, abort, flash, make_response, request, session, g
import config
import db
import forum
import users
import searching
import markupsafe

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login(): # checks login
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

def valid_game(title, description): # checks game title and description size requirements
    if not title or not description or len(title) > 100 or len(description) > 5000:
        return True
    return False

def valid_review(content, score): # checks review content size requirements
    if not content or len(content) > 5000 or score not in ["1", "2", "3", "4", "5"]:
        return True
    return False

@app.before_request # time tester (begin)
def before_request():
    g.start_time = time.time()

@app.after_request # time tester (end)
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

@app.template_filter() # a template filter to show line breaks
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/") # homepage
@app.route("/<int:page>")
def index(page=1):
    page_size = 10 # amount of games per page
    game_count = forum.game_count()
    page_count = math.ceil(game_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))
    
    classes = forum.get_all_classes()
    games = forum.get_games(page, page_size)
    return render_template("index.html", page=page, page_count=page_count, games=games, classes=classes)

@app.route("/register", methods=["GET", "POST"]) # register page
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        developer = request.form["developer"]

        if not username or not password1 or not developer or len(username) > 50 or len(password1) > 50:
            abort(403)

        if password1 != password2:
            flash("ERROR: The passwords do not match")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        if users.create_user(username, password1, developer):
            session["username"] = username # The user will be logged in automatically when an account is made
            session["developer"] = int(developer) # stores whether or not the user is a developer
            session["user_id"] = db.last_insert_id() # fetch the id
            session["csrf_token"] = secrets.token_hex(16) # generates a hidden csrf-session-token
            return redirect("/")
        else:
            flash("ERROR: The username is taken")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

@app.route("/login", methods=["GET", "POST"]) # login page
def login():
    if request.method == "GET":
        return render_template("login.html", next_page=request.referrer, filled={})

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form["next_page"]

        info = users.check_login(username, password)
        if info:
            session["username"] = username
            session["developer"] = info["developer"]
            session["user_id"] = info["user_id"]
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(next_page)
        else:
            flash("ERROR: Wrong username or password")
            filled = {"username": username}
            return render_template("login.html", next_page=next_page, filled=filled)

@app.route("/logout") # logout handler
def logout():
    session.clear()
    return redirect("/")

@app.route("/new_game", methods=["POST"])
def new_game():
    require_login()
    check_csrf()

    title = request.form["title"]
    description = request.form["description"]
    if valid_game(title, description):
        abort(403)

    all_classes = forum.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    user_id = session["user_id"]

    thread_id = forum.add_game(title, description, user_id, classes)
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
    check_csrf()

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
        check_csrf()
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
        check_csrf()
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
        check_csrf()
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
        check_csrf()
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
def update_profile_picture():
    require_login()

    if request.method == "GET":
        return render_template("update_profile_picture.html")

    if request.method == "POST":
        check_csrf()
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            flash("ERROR: The file is not a .jpg-file")
            return redirect("/update_profile_picture")

        image = file.read()
        if len(image) > 100 * 1024:
            flash("ERROR: The image is too big")
            return redirect("/update_profile_picture")

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
        return render_template("search.html", title_value=title_value, title_results=title_results)

    if parameter == "review_content":
        review_content_value = request.args.get("review_content_value")
        review_content_results = searching.review_content(review_content_value)
        return render_template("search.html", review_content_value=review_content_value, review_content_results=review_content_results)

    return render_template("search.html", nothing=1) # if no parameters are given
