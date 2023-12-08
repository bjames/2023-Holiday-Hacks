import project.modules.dashboard_scripts as dashboard_scripts
import project.db.session_db as session_db
import project.db.user_db as user_db

from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    make_response,
)


app = Flask(__name__)
user_db.create_db()
session_db.create_db()
SESSION_COOKIE_NAME = "noco_hackers_2023_session"


def check_cookie() -> str:
    username = ""
    if request.cookies.get(SESSION_COOKIE_NAME):
        username = session_db.check_session(request.cookies.get(SESSION_COOKIE_NAME))

    return username


@app.route("/")
def home():
    # if the user has a valid session, redirect them to the dashboard
    if request.cookies.get(SESSION_COOKIE_NAME):
        if session_db.check_session(request.cookies.get("session")):
            return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/ping", methods=["POST"])
def ping():
    username = check_cookie()
    if username:
        result = dashboard_scripts.ping(request.form.get("host"))
        return render_template("dashboard.html", result=result)
    else:
        return redirect(url_for("login"))


@app.route("/curl", methods=["POST"])
def curl():
    username = check_cookie()
    if username:
        result = dashboard_scripts.curl(request.form.get("host"))
        return render_template("dashboard.html", result=result)
    else:
        return redirect(url_for("login"))


@app.route("/traceroute", methods=["POST"])
def traceroute():
    username = check_cookie()
    if username:
        result = dashboard_scripts.traceroute(request.form.get("host"))
        return render_template("dashboard.html", result=result)
    else:
        return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    username = check_cookie()
    if username:
        return render_template("dashboard.html", username=username)
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""

    username = check_cookie()
    if username:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        result = user_db.check_password(username, password)

        # if we get a result back, create a cookie containing a session token
        if result:
            token = session_db.add_session(result[0])
            # set the session cookie
            msg = make_response(redirect(url_for("dashboard")))
            msg.set_cookie(SESSION_COOKIE_NAME, token)
            return msg
        else:
            msg = "Invalid username/password combination."

    return render_template("login.html", msg=msg)
