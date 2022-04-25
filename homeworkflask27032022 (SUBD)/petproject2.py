from flask import Flask, render_template, request, g, flash, redirect
import os
import sqlite3
from FDataBase import FDataBase

DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'ghmbjjyki'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "flsite.db")))

dbase = None


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route("/")
def index():
    return render_template("index.html", menu=dbase.get_menu(), title="main page")


@app.route("/now")
def now():
    auto_now = dbase.get_now_auto()
    print(auto_now)
    return render_template("now.html", menu=dbase.get_menu(), title="present page", auto=auto_now)


@app.route("/past")
def past():
    auto_past = dbase.get_past_auto()
    return render_template("past.html", menu=dbase.get_menu(), title="past page", auto=auto_past)


@app.route("/next_home_work", methods=["POST", "GET"])
def next_home_work():
    return render_template("next_home_work.html", menu=dbase.get_menu2(), title="next home work, car base",
                           base=dbase.get_auto())


@app.route("/add_auto", methods=["POST", "GET"])
def add_auto():
    if request.method == "POST":
        res = dbase.add_auto(request.form["marka"], request.form["model"], request.form["information"],
                             request.form["year"], request.form["price"])
        if not res:
            flash("Ошибка добавления записи в базу данных", category="error")
        else:
            flash("Добавление записи в базу данных прошло успешно", category='success')

    return render_template("add_auto.html", menu=dbase.get_menu2(), title="add auto", base=[])


@app.route("/about")
def about():
    return render_template("about.html", menu=dbase.get_menu(), title="about")


@app.route("/info", methods=["POST", "GET"])
def info():

    if request.method == "POST":
        res = dbase.get_auto_id(int(request.form['select_id']))
    return render_template("info.html", menu=dbase.get_menu2(), title="information", base=res)


if __name__ == "__main__":
    app.run(debug=True)
