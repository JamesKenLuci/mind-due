from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

tasks = []  # temporary storage (resets when you restart the app)

@app.route('/')
def home():
    today = datetime.now().date()
    sorted_tasks = sorted(tasks, key=lambda x: x["deadline"])
    return render_template('index.html', tasks=sorted_tasks, today=today)

@app.route('/add', methods=['POST'])
def add_task():
    subject = request.form['subject']
    title = request.form['title']
    deadline = datetime.strptime(request.form['deadline'], "%Y-%m-%d").date()
    tasks.append({"subject": subject, "title": title, "deadline": deadline})
    return redirect(url_for('home'))

@app.route('/delete/<int:index>')
def delete_task(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
