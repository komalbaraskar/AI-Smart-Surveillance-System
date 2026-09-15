from flask import Flask, render_template
from database import logs, people_count
from flask import Flask, request, redirect, url_for, session
from database import users, authenticate_user
from functools import wraps


app = Flask(__name__)

# Change this in production
app.secret_key = "change-this-secret-key"


# LOGIN REQUIRED

def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return wrapper


# ADMIN REQUIRED

def admin_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("login"))

        if session.get("role") != "admin":
            return render_template(
                "unauthorized.html"
            ), 403

        return function(*args, **kwargs)

    return wrapper


# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = authenticate_user(
            username,
            password
        )

        if user:

            session["user_id"] = str(user["_id"])
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect(
                url_for("dashboard")
            )

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


# LOGOUT

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# DASHBOARD

@app.route("/")
@login_required
def dashboard():

    total_alerts = logs.count_documents({})

    latest_count = people_count.find_one(
        {},
        sort=[("_id", -1)]
    )

    current_people = (
        latest_count["count"]
        if latest_count
        else 0
    )

    recent_logs = logs.find(
        {},
        {
            "_id": 0,
            "message": 1,
            "time": 1
        }
    ).sort("_id", -1).limit(10)

    logs_data = []

    for log in recent_logs:

        logs_data.append((
            log.get("message", ""),
            log.get("time", "")
        ))

    return render_template(
        "dashboard.html",
        total_alerts=total_alerts,
        people_count=current_people,
        logs=logs_data
    )

# ADMIN - USERS

@app.route("/users")
@admin_required
def user_management():

    all_users = users.find(
        {},
        {
            "password": 0
        }
    )

    return render_template(
        "users.html",
        users=all_users
    )


# ADMIN - ADD USER

@app.route("/users/add", methods=["POST"])
@admin_required
def add_user():

    username = request.form.get(
        "username"
    )

    password = request.form.get(
        "password"
    )

    role = request.form.get(
        "role"
    )
    existing_user = users.find_one({
        "username": username
    })
    if existing_user:
        return redirect(
            url_for("user_management")
        )

    from database import create_user
    create_user(
        username,
        password,
        role
    )
    return redirect(
        url_for("user_management")
    )

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )