# A very simple Flask Hello World app for you to get started with...
from datetime import timedelta
import secrets
import configparser
from flask import Flask, render_template, send_from_directory , request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
# Werkzeug security tools for password hashing (uncomment when you use your User class)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError



app = Flask(__name__)

"""1. connecting flask to the Datbase"""

# 1. Parse credentials from config.txt
config = configparser.ConfigParser()
config.read('/home/helix0py/mysite/config.txt')

# 2. Extract configuration variables
app.config['SECRET_KEY'] = config.get('flask', 'SECRET_KEY')

# Configure session timeout length to last 1.5 hours
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1, minutes=30)
db_user = config.get('mysql', 'USER')
db_pass = config.get('mysql', 'PASSWORD')
db_host = config.get('mysql', 'HOST')
db_name = config.get('mysql', 'DB_NAME')

# 3. Configure the SQLAlchemy Connection URI for PythonAnywhere
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"


"""test"""
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@host/databasename'

# PythonAnywhere drops inactive connections after 5 minutes; pool_recycle prevents connection drop errors
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 280,
    'connect_args': {'connect_timeout': 5}
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 4. Initialize Database Engine
db = SQLAlchemy(app)



""" 2. Database Model (Your Table Structure) """


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())



@app.before_request
def make_session_permanent():
    session.permanent = True

    # If they have no identity, restrict access to everything EXCEPT public entry pages
    if not session.get("user_id") and not session.get("guest_id"):
        # Added 'join_guest' to the exclusion list so the guest route can execute
        if request.endpoint not in ['start_app', 'join_guest', 'login', 'signup', 'static', 'interactive']:
            return redirect(url_for('start_app'))


# url routes

@app.route('/')
def start_app():
    # Totally clean: No ID is assigned just for looking at the home page
    return render_template("home.html")


@app.route("/guest")
def join_guest():
    # Explicit Trigger: ID is ONLY generated when they click the "Join as Guest" button
    if not session.get("user_id") and not session.get("guest_id"):
        session["guest_id"] = f"guest_{secrets.token_hex(8)}"
    return redirect(url_for("dash"))


@app.route("/logout")
def logout():
    session.clear()     #pop("user_id", None)
    session.clear()     #pop("guest_id", None)
    return redirect(url_for("start_app"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # ID-less entry route
    if request.method == "POST":
        user_name = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not user_name or not password:
            return render_template("signup.html", error="Enter a username and password.")

        new_user = User(
            username=user_name,
            password_hash=generate_password_hash(password)
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template("signup.html", error="That username is already taken.")

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # ID-less entry route
    if request.method == "POST":
        user_name = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not user_name or not password:
            return render_template("login.html", error="Enter a username and password.")

        user = User.query.filter_by(username=user_name).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect(url_for("dash"))

    return render_template("login.html")


@app.route("/dash", methods=["GET", "POST"])
def dash():
    # If a clever user types "/dash" manually without logging in or choosing guest, kick them out
    if not session.get("user_id") and not session.get("guest_id"):
        return redirect(url_for("start_app"))

    user_id = session.get("user_id")
    username = None

    if user_id:
        user = User.query.get(user_id)
        if user:
            username = user.username
    else:
        username = session.get("guest_id")

    return render_template("dashboard.html", username=username, logged_in=bool(user_id))


@app.route("/settings")
def setting():
    if not session.get("user_id") and not session.get("guest_id"):
        return redirect(url_for("start_app"))
    return render_template("settings.html")

@app.route("/interactive/<path:filename>")
def interactive(filename):
    return send_from_directory("interactive", filename)

'''  use to check  bd contections.
@app.route('/testdb')
def test_db():
    try:
        # Attempt to run a raw SQL query against the database
        db.session.execute(db.text('SELECT 1'))
        return "<h3>🟢 Success! Connected to MySQL Database.</h3>", 200
    except Exception as e:
        return f"<h3>🔴 Connection Failed!</h3><p>Error: {str(e)}</p>", 500
'''


# Required pattern for PythonAnywhere Web Tab Reload
if __name__ == '__main__':
    app.run(debug=True) # when done with site set debug=False
