import sqlite3
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "campusnow-secret-key"

DATABASE = "database.db"

CATEGORY_ICONS = {
    "Study Groups": "📚",
    "Events": "🎉",
    "Housing": "🏠",
    "Clubs": "⭐",
    "General": "📌"
}


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            icon TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    db.commit()


@app.before_request
def before_request():
    init_db()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    db = get_db()
    posts = db.execute("""
        SELECT posts.*, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.id DESC
    """).fetchall()

    return render_template("index.html", posts=posts, current_user_id=session.get("user_id"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            flash("All fields are required.")
            return redirect(url_for("register"))

        db = get_db()
        existing_user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        db.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Logged in successfully.")
            return redirect(url_for("index"))

        flash("Invalid username or password.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("index"))


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]

        if not title or not content or not category:
            flash("All fields are required.")
            return redirect(url_for("create"))

        icon = CATEGORY_ICONS.get(category, "📌")
        timestamp = datetime.now().strftime("%b %d, %Y at %I:%M %p")

        db = get_db()
        db.execute("""
            INSERT INTO posts (title, content, category, icon, timestamp, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, content, category, icon, timestamp, session["user_id"]))
        db.commit()

        flash("Post created successfully.")
        return redirect(url_for("index"))

    return render_template("create_post.html")


@app.route("/delete/<int:post_id>")
@login_required
def delete(post_id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()

    if post and post["user_id"] == session["user_id"]:
        db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        db.commit()
        flash("Post deleted successfully.")
    else:
        flash("You can only delete your own posts.")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)