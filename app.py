from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'mind_due_secret_key'

# Simulated in-memory "database"
users = []
tasks = []

# Default admin user
users.append({
    'id': 1,
    'username': 'admin',
    'password': 'admin',
    'role': 'admin'
})
next_user_id = 2
next_task_id = 1


@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    global next_user_id
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username exists
        if any(u['username'] == username for u in users):
            return "⚠️ Username already exists! Try another one."

        users.append({
            'id': next_user_id,
            'username': username,
            'password': password,
            'role': 'user'
        })
        next_user_id += 1
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        return "Invalid credentials!"
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    today = datetime.today().date()

    if session['role'] == 'admin':
        user_tasks = tasks
        return render_template('admin.html', tasks=user_tasks, today=today)
    else:
        user_tasks = [t for t in tasks if t['user_id'] == session['user_id']]
        return render_template('index.html', tasks=user_tasks, today=today)


@app.route('/add', methods=['POST'])
def add_task():
    global next_task_id
    if 'user_id' not in session:
        return redirect(url_for('login'))

    subject = request.form['subject']
    title = request.form['title']
    deadline = request.form['deadline']

    tasks.append({
        'id': next_task_id,
        'user_id': session['user_id'],
        'subject': subject,
        'title': title,
        'deadline': deadline
    })
    next_task_id += 1
    return redirect(url_for('dashboard'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    global tasks
    if session['role'] == 'admin':
        tasks = [t for t in tasks if t['id'] != task_id]
    else:
        tasks = [t for t in tasks if not (t['id'] == task_id and t['user_id'] == session['user_id'])]
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
