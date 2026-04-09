from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

posts = [
    {
        "title": "Math 2417 Study Group Tonight",
        "content": "We’re meeting at the library at 7:00 PM to review for the exam. Everyone is welcome.",
        "category": "Study Groups",
        "icon": "📚",
        "timestamp": datetime.now().strftime("%b %d, %Y at %I:%M %p")
    },
    {
        "title": "Roommate Needed Near Campus",
        "content": "Looking for one roommate for next semester. Apartment is 10 minutes from UTRGV.",
        "category": "Housing",
        "icon": "🏠",
        "timestamp": datetime.now().strftime("%b %d, %Y at %I:%M %p")
    },
    {
        "title": "Campus Club Fair This Friday",
        "content": "Come check out student organizations, meet new people, and get involved on campus.",
        "category": "Events",
        "icon": "🎉",
        "timestamp": datetime.now().strftime("%b %d, %Y at %I:%M %p")
    }
]

CATEGORY_ICONS = {
    "Study Groups": "📚",
    "Events": "🎉",
    "Housing": "🏠",
    "Clubs": "⭐",
    "General": "📌"
}

@app.route("/")
def index():
    return render_template("index.html", posts=posts)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]

        posts.insert(0, {
            "title": title,
            "content": content,
            "category": category,
            "icon": CATEGORY_ICONS.get(category, "📌"),
            "timestamp": datetime.now().strftime("%b %d, %Y at %I:%M %p")
        })

        return redirect(url_for("index"))

    return render_template("create_post.html")

@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(posts):
        posts.pop(index)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)