from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

posts = []

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        posts.append({
            'title': title,
            'content': content
        })

        return redirect(url_for('index'))

    return render_template('create_post.html')

@app.route('/delete/<int:index>')
def delete(index):
    if 0 <= index < len(posts):
        posts.pop(index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)