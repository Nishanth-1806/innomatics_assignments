import string
import random

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
import validators

from models import db, User, URL


app = Flask(__name__)
app.config["SECRET_KEY"] = "change_this_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choices(chars, k=length))
        if not URL.query.filter_by(short_code=code).first():
            return code


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if len(username) < 5 or len(username) > 9:
            flash("Username must be between 5 to 9 characters long", "danger")
            return render_template("signup.html")

        existing = User.query.filter_by(username=username).first()
        if existing:
            flash("This username already exists…", "danger")
            return render_template("signup.html")

        password_hash = generate_password_hash(password)
        user = User(username=username, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        flash("Signup successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid username or password", "danger")
            return render_template("login.html")

        login_user(user)
        return redirect(url_for("shortener"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/shortener", methods=["GET", "POST"])
@login_required
def shortener():
    short_url = None
    error = None

    if request.method == "POST":
        original_url = request.form.get("original_url", "").strip()

        if not validators.url(original_url):
            error = "Please enter a valid URL (including http:// or https://)."
        else:
            code = generate_short_code()
            url_entry = URL(
                original_url=original_url,
                short_code=code,
                user_id=current_user.id,
            )
            db.session.add(url_entry)
            db.session.commit()

            short_url = request.host_url.rstrip("/") + "/" + code

    history = URL.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "shortener.html",
        short_url=short_url,
        error=error,
        history=history,
    )


@app.route("/<short_code>")
def redirect_short(short_code: str):
    url_entry = URL.query.filter_by(short_code=short_code).first_or_404()
    return redirect(url_entry.original_url)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
