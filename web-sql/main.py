import user_db
import session_db
import secrets
from flask import Flask, request, render_template, render_template_string, redirect, url_for, make_response



app = Flask(__name__)
user_db.create_db()
session_db.create_db()
SESSION_COOKIE_NAME = "noco_hackers_2023_session"

@app.route('/')
def home():
    # if the user has a valid session, redirect them to the dashboard
    if request.cookies.get(SESSION_COOKIE_NAME):
        if session_db.check_session(request.cookies.get("session")):
            return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if request.cookies.get(SESSION_COOKIE_NAME):
        username = session_db.check_session(request.cookies.get(SESSION_COOKIE_NAME))
        if username:
            return render_template('dashboard.html', username=username)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        result = user_db.check_password(username, password)

        # if we get a result back, create a cookie containing a session token
        if result:
            token = session_db.add_session(result[0])
            # set the session cookie
            msg = make_response(redirect(url_for('dashboard')))
            msg.set_cookie(SESSION_COOKIE_NAME, token)
            return msg
        else:
            msg = "Invalid username/password combination."

    return render_template('login.html', msg=msg)
