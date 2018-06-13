import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
#    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine("postgres://ynorvjldptczsr:642db89f29e57eb14c168c81dd9088b79e279edabda65bef8b391d46c31f9d0b@ec2-54-243-137-182.compute-1.amazonaws.com:5432/d1r7oflel96ou")
db = scoped_session(sessionmaker(bind=engine))

# Configure session to use filesystem
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

# Username/Password
usernm = None
passwd = None
loggedIn = 0

# Homepage
@app.route("/")
def index():
    return render_template('index.html', username=usernm,loggedIn=loggedIn)

# Sign up for a new account
@app.route("/signup")
def signup():
    global usernm, passwd, loggedIn
    return render_template("signup.html",loggedIn=loggedIn)

# Sign Up Successful
@app.route("/signupsuccess", methods=["POST"])
def signupsuccess():
    global usernm, passwd, loggedIn
    usernm = request.form.get("username")
    passwd = request.form.get("password")

    #Validate/clean username
    #TO DO:

    # If username doesnt exist
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": usernm}).rowcount == 0:
        # Inset/Commit changes
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",{"username": usernm, "password": passwd})
        db.commit()
        loggedIn = 1
        return render_template("signupsuccess.html", name=usernm, username=usernm,loggedIn=loggedIn)
    else:
        usernm = None
        passwd = None
        loggedIn = 0
        return render_template("signupfail.html", name=usernm,loggedIn=loggedIn)

# Sign In
@app.route("/signin", methods=["POST"])
def signin():
    global usernm, passwd, loggedIn
    usernm = request.form.get("username")
    passwd = request.form.get("password")

    #Validate/clean username
    #TO DO:

    # If username doesnt exist
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": usernm}).rowcount == 0:
        loggedIn = 0
        return render_template("signinfailed.html", name=usernm,loggedIn=loggedIn)

    # Fetch password associated w/usernm and test
    passwd_fetch = db.execute("SELECT password FROM users WHERE global usernm = :username", {"username": usernm}).fetchone()
    if passwd == passwd_fetch.password:
        loggedIn = 1
        return render_template("signinsuccess.html", username=usernm, loggedIn=loggedIn)
    else:
        usernm = None
        passwd = None
        loggedIn = 0
        return render_template("signinfailed.html",loggedIn=loggedIn)

#Log in
@app.route("/login")
def login():
    global usernm, passwd, loggedIn
    return render_template("login.html",loggedIn=loggedIn)

# Log Out
@app.route("/logout")
def logout():
    global usernm, passwd, loggedIn
    tempUsernm = usernm
    usernm = None
    passwd = None
    loggedIn = 0

    return render_template("logout.html",loggedIn=loggedIn)

# Search
@app.route("/search")
def search():
    global usernm, passwd, loggedIn
    return render_template("search.html",username=usernm,loggedIn=loggedIn)

# Search Results
@app.route("/searchresults", methods=["POST"])
def searchresults():
    global usernm, passwd, loggedIn
    query = request.form.get("search_criteria")

    # flasksqlalchemy query here
    books = Book.query.get(query)

    # old
    #results = db.execute("SELECT * FROM books WHERE title LIKE :query", {"query":query}).fetchall


    return render_template("searchresults.html", books=books)
