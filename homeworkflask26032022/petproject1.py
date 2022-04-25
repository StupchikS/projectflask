from flask import Flask, render_template


menu = [
    {"name": "Главная страница", "url": "/"},
    {"name": "Автомобили настоящего времени", "url": "/now"},
    {"name": "Автомобили прошлые", "url": "/past"},
    {"name": "О сайте", "url": "/about"}
]
auto_now = [
    {"brend": "lada niva", "owner": "папа"},
    {"brend": "nissan laef", "owner": "я"},
    {"brend": "toyota ractis", "owner": "брат"}
]
auto_past = [
    {"brend": "toyota ractis", "owner": "папа"},
    {"brend": "uaz patriot pickup", "owner": "я"},
    {"brend": "toyota corolla", "owner": "брат"}
]

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", menu=menu, title="main page")


@app.route("/now")
def now():
    return render_template("now.html", menu=menu, title="present page", auto=auto_now)


@app.route("/past")
def past():
    return render_template("past.html", menu=menu, title="past page", auto=auto_past)


@app.route("/about")
def about():
    return render_template("about.html", menu=menu, title="about")


if __name__ == "__main__":
    app.run(debug=True)
