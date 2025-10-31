from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "minddue_secret"

# ✅ In-memory storage (NO DATABASE)
users = {}       # { user_id: {"username": "...", "password": "..."} }
tasks = []       # [ {"user_id": 1, "subject": "...", "title": "...", "deadline": "..."} ]
next_user_id = 1
next_task_id = 1


@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/register")


# ✅ REGISTER ONLY (no login)
@app.route("/register", methods=["GET", "POST"])
def register():
    global next_user_id

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Create user
        users[next_user_id] = {"username": username, "password": password}

        # Auto login
        session["user_id"] = next_user_id

        next_user_id += 1
        return redirect("/dashboard")

    return render_template("register.html")


# ✅ DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/register")

    user_tasks = [t for t in tasks if t["user_id"] == session["user_id"]]

    return render_template("dashboard.html", tasks=user_tasks)


# ✅ ADD TASK
@app.route("/add", methods=["POST"])
def add():
    global next_task_id

    if "user_id" not in session:
        return redirect("/register")

    subject = request.form["subject"]
    title = request.form["title"]
    deadline = request.form["deadline"]

    tasks.append({
        "id": next_task_id,
        "user_id": session["user_id"],
        "subject": subject,
        "title": title,
        "deadline": deadline
    })

    next_task_id += 1

    return redirect("/dashboard")


# ✅ DELETE TASK
@app.route("/delete/<int:task_id>")
def delete(task_id):
    global tasks
    tasks = [t for t in tasks if not (t["id"] == task_id and t["user_id"] == session["user_id"])]
    return redirect("/dashboard")


# ✅ LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/register")


if __name__ == "__main__":
    app.run(debug=True)
