from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
import os
import _sqlite3
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from admin.admin import admin


DATABASE = '/tmp/fl.db'
DEBUG = True
os.urandom(20).hex()
SECRET_KEY = 'tgfhnmioiytyhfgjkhl'
app = Flask(__name__)
# app.config['SECRET_KEY'] = '32554yyjjhki8ok'
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fl.db')))
app.register_blueprint(admin, url_prefix="/admin")
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Need autorizade"
login_manager.login_message_category = "error"
MAX_CONTENT_LENGTH = 1024 * 1024


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().from_db(user_id, dbase)


def connect_db():
    con = _sqlite3.connect(app.config['DATABASE'])
    con.row_factory = _sqlite3.Row
    return con


#
# menu = [{"name": "Главная", "url": "index"},
#         {"name": "О нас", "url": "about"},
#         {"name": "Обратная связь", "url": "contact"}
# ]


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route("/")
def index():
    print(url_for("index"))
    return render_template("index.html", title="Главня страница", menu=dbase.get_menu(), posts=dbase.get_posts_anonce())


@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.add_post(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash("error", category="error")
            else:
                flash("ok", category='success')
        else:
            flash("no post article", category="error")
    return render_template('add_post')


@app.route("/post/<alias>")
@login_required
def show_post(alias):
    title, post = dbase.get_post(alias)
    if not title:
        abort(404)
    return render_template('post.html', title=title, menu=dbase.get_menu(), post=posts)


@app.route("/about")
def about():
    print(url_for("index"))
    return render_template("about.html", title="О нас", menu=[])


@app.route("/contact", method=["POST", "GET"])
def contact():
    if request.method == "POST":
        if len(request.form['username']) > 2:
            flash('succed', category='success')
        else:
            flash('error', category='error')
        print(request.form)
        context = {
            'username': request.form['username'],
            'email': request.form['email'],
            'message': request.form['message']
        }
        return render_template("contact.html", **context)
    return render_template("contact.html", title="Обратная связь", menu=[])


@app.route("/login")
def login():
    if current_user.is_authetification:
        return redirect(url_for("profile"))
    if request.method == 'POST':
        user = dbase.get_user_by_email(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            user_login = UserLogin().create(user)
            rm = True if request.form.get('remember') else False
            login_user(user_login, remember=rm)
            return redirect(request.args.get("next") or url_for('profile'))
        flash("Ошибка в логине или пароле", "error")
    return render_template("login.html", title="Авторизация", menu=dbase.get_menu())


@app.route("/register", method=["POST", "GET"])
def register():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 and len(request.form['psw']) > 4 and \
                request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.add_user(request.form['name'], request.form['email'], hash)
            if res:
                flash("Регистрация успешна", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка регистрации", 'error')
        else:
            flash("Неверно заполнены поля", "error")

    return render_template("register.html", title="Регистрация", menu=dbase.get_menu())


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", menu=dbase.get_menu(), title="profile")

@app.route("/logaut")
@login_required
def logaut():
    logout_user()
    flash("Your exit", "success")
    return redirect(url_for('login'))


@app.route('/userava')
@login_required
def userava():
    img = current_user.get_avatar(app)
    if not img:
        return ""
    h = app.make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h

@app.route("/upload", methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verify_ext(file.filename):
            try:
                img = file.read()
                res = dbase.update_user_avatar(img, current_user.get_id())
                if not res:
                    flash("ошибка обновления аватара", "error")
                flash("аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("error", "error")
        else:
            flash("Error", "error")
    return redirect((url_for("profile")))



#
# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#     elif request.method == 'POST' and request.form['username'] == 'Sergey' and request.form['passw'] == '123':
#         session['userLogged'] = request.form['username']
#         return redirect(url_for('profile', username=session['userLogged']))
#     return render_template("login.html", title="Авторизация", menu=[])
#
# @app.route("/profile/<username>")
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)
#     return f"Пользователь: {username}"
#
#
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page404.html', title='Страница не найдена', menu=[])


if __name__ == "__main__":
    app.run(debug=True)
