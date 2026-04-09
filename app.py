from flask import Flask, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SET UP FOR THE DATABASE 
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_table()

# HOME PAGE 
@app.route("/")
def home():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()

    html = "<h1>Campus Bulletin Board</h1>"
    html += '<a href="/create">Create Post</a><br><br>'

    for post in posts:
        html += f"<h3>{post['title']}</h3>"
        html += f"<p>{post['content']}</p>"
        html += f'<a href="/edit/{post["id"]}">Edit</a> '
        html += f'<a href="/delete/{post["id"]}">Delete</a><hr>'

    return html

# TO CREATE A POST 
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn = get_db_connection()
        conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    return """
        <h2>Create Post</h2>
        <form method="post">
            Title: <input type="text" name="title"><br><br>
            Content: <textarea name="content"></textarea><br><br>
            <button type="submit">Submit</button>
        </form>
    """

# FOR USER TO BE ABEL TO EDIT A POST 
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        new_title = request.form["title"]
        new_content = request.form["content"]

        conn.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", 
                     (new_title, new_content, id))
        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    conn.close()

    return f"""
        <h2>Edit Post</h2>
        <form method="post">
            Title: <input type="text" name="title" value="{post['title']}"><br><br>
            Content: <textarea name="content">{post['content']}</textarea><br><br>
            <button type="submit">Update</button>
        </form>
    """

# DELETING A POST FROM THE SITE
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

# RUN 
if __name__ == "__main__":
    app.run(debug=True)