import json
import os
import uuid
from datetime import datetime, timedelta

from flask import Flask, jsonify, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "shazam-dev-secret-change-later")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")
TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=2)


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


@app.route("/")
def login_page():
    username = session.get("username")
    if username:
        return redirect(f"/user/{username}")
    return render_template("login.html")


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "Please enter your name and password."}), 400

    users = load_users()

    if username in users:
        if not check_password_hash(users[username], password):
            return jsonify({"error": "Wrong password. Try again."}), 401
    else:
        users[username] = generate_password_hash(password)
        save_users(users)

    session.permanent = True
    session["username"] = username
    return jsonify({"success": True, "redirect": f"/user/{username}"})


@app.route("/user/<username>")
def user_page(username):
    if session.get("username") != username:
        return redirect("/")
    return render_template("user_page.html", username=username)


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    username = session.get("username")
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    tasks = load_tasks()
    user_tasks = tasks.get(username, [])
    return jsonify(user_tasks)


@app.route("/api/tasks", methods=["POST"])
def add_task():
    username = session.get("username")
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Task text cannot be empty."}), 400

    task_id = str(uuid.uuid4())
    created_at = datetime.now().strftime("%b %d, %I:%M %p")

    new_task = {
        "id": task_id,
        "text": text,
        "completed": False,
        "created_at": created_at
    }

    tasks = load_tasks()
    if username not in tasks:
        tasks[username] = []
    tasks[username].append(new_task)
    save_tasks(tasks)

    return jsonify(new_task), 201


@app.route("/api/tasks/<task_id>", methods=["PATCH"])
def toggle_task(task_id):
    username = session.get("username")
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    completed = data.get("completed")
    if completed is None:
        return jsonify({"error": "Missing 'completed' status."}), 400

    tasks = load_tasks()
    user_tasks = tasks.get(username, [])

    task_found = None
    for task in user_tasks:
        if task["id"] == task_id:
            task["completed"] = bool(completed)
            task_found = task
            break

    if not task_found:
        return jsonify({"error": "Task not found"}), 404

    tasks[username] = user_tasks
    save_tasks(tasks)
    return jsonify(task_found)


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    username = session.get("username")
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    tasks = load_tasks()
    user_tasks = tasks.get(username, [])

    new_user_tasks = [t for t in user_tasks if t["id"] != task_id]

    if len(new_user_tasks) == len(user_tasks):
        return jsonify({"error": "Task not found"}), 404

    tasks[username] = new_user_tasks
    save_tasks(tasks)
    return jsonify({"success": True})


@app.post("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)

