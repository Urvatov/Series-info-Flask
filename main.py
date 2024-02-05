from flask import Flask, render_template, request, g, flash, abort, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3

from data import Data
from UserLogin import UserLogin

DATABASE = "database.db"
DEBUG = True
SECRET_KEY = "abc"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "database.db")))

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    print("load user")
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    connect = sqlite3.connect(app.config['DATABASE'])
    connect.row_factory = sqlite3.Row
    return connect

def create_db():
    db = connect_db()
    with app.open_resource('database.sql', mode= 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
        print("БАЗА ДАННЫХ ПОЛУЧЕНА")
    return g.link_db

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = Data(db)
   

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


#------------------------------------------------------------------------------------------------------------------


@app.route("/")
def index():
    db = get_db()
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/all_series", methods=["POST", "GET"])
def all_series():
    db = get_db()
    dbase = Data(db)
    return render_template("all_series.html", posts = dbase.get_posts())


@app.route("/series/<int:id_series>", methods=["POST", "GET"])
def series(id_series):
    title, seasons, finished, release = dbase.get_series(id_series)
    series_genres = dbase.get_genre_from_series(id_series)
    series_actors = dbase.get_actors_from_series(id_series)
    series_directors = dbase.get_directors_from_series(id_series)
    series_writers = dbase.get_writers_from_series(id_series)
    series_seasons = dbase.get_season(id_series)

    print(series_genres)

    if request.method == "POST":
        
        if "rating" in request.form:
            user_id = current_user.get_id()
            dbase.add_rating(user_id, id_series, request.form["rating"])
        
        if "genre" in request.form:
            dbase.add_genre_to_series(id_series, request.form["genre"])
        
        if "actor" in request.form:
            dbase.add_actor_to_series(id_series, request.form["actor"])
        
        if "director" in request.form:
            dbase.add_director_to_series(id_series, request.form["director"])
        
        if "writer" in request.form:
            dbase.add_writer_to_series(id_series, request.form["writer"])
        
        if "create_season" in request.form:
            print("add_season")
            dbase.add_season(request.form["season_title"], id_series, request.form["order_number"], request.form["episodes_number"])
        
    return render_template("series.html", id_series = id_series, posts = dbase.get_posts(), title = title, seasons = seasons,
                            finished = finished, release = release, rating = dbase.get_rating(id_series), series_genres = series_genres,
                            series_actors = series_actors, series_directors = series_directors, series_writers = series_writers, series_seasons = series_seasons,
                            genres = dbase.get_genres(),
                            actors = dbase.get_actors(), directors = dbase.get_directors(), writers = dbase.get_writers())


@app.route("/add_series", methods=["POST", "GET"])
@login_required
def add_series():
    
    if request.method == "POST":
       res = dbase.add(request.form['title'], request.form['seasons'], request.form['finished'], request.form['release'])
       flash("Сериал успешно добавлен")
    return render_template("add_series.html", genres = dbase.get_genres(), actors = dbase.get_actors(), directors = dbase.get_directors(), writers = dbase.get_writers())


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = dbase.get_user_by_nickname(request.form['nickname'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect("/")
    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form["nickname"]) > 4 and len(request.form["psw"]) > 4:
            hash = generate_password_hash(request.form["psw"])
            res = dbase.add_user(request.form['nickname'], hash)
            print("HASH", hash)
            if res: return redirect("/login")
            else:
                print("ОШИБКА РЕГИСТРАЦИИ")

    return render_template("register.html")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", nickname = current_user.get_nickname(), id = current_user.get_id())

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/config")
@login_required
def config():
    return render_template("config.html")

@app.route("/config/add_genre", methods = ["POST", "GET"])
def add_genre():
    if request.method == "POST":
       res = dbase.add_genre(request.form['title'])
      
    return render_template("add_genre.html")

@app.route("/config/add_human", methods = ["POST", "GET"])
def add_human():
    if request.method == "POST":
        dbase.add_human(request.form["fullname"], request.form["birthday"], request.form["select"])
    return render_template("add_human.html")

create_db()
if __name__ == "__main__":
    app.run(debug = True)

