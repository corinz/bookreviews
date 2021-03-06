import os

from flask import Flask, render_template, request
from db_models import *
from sqlalchemy import or_

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ynorvjldptczsr:642db89f29e57eb14c168c81dd9088b79e279edabda65bef8b391d46c31f9d0b@ec2-54-243-137-182.compute-1.amazonaws.com:5432/d1r7oflel96ou"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
#    raise RuntimeError("DATABASE_URL is not set")

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
@app.route("/signupstatus", methods=["POST"])
def signupstatus():
    global usernm, passwd, loggedIn
    usernm = request.form.get("username")
    passwd = request.form.get("password")

    #Validate/clean username
    #TO DO:

    # If username doesnt exist
    if User.query.filter_by(username=usernm).first() == None:
        # Insert User & Commit changes
        User.add_user(username=usernm, password=passwd)
        loggedIn = 1
        return render_template("signupsuccess.html", name=usernm, username=usernm,loggedIn=loggedIn)
    else:
        tempUsernm = usernm
        usernm = None
        passwd = None
        loggedIn = 0
        return render_template("signupfail.html", name=tempUsernm,loggedIn=loggedIn)

# Sign In
@app.route("/signin", methods=["POST"])
def signin():
    global usernm, passwd, loggedIn
    usernm = request.form.get("username")
    passwd = request.form.get("password")

    #Validate/clean username
    #TO DO:

    # If username doesnt exist
    if User.query.filter_by(username=usernm).first() == None:
        loggedIn = 0
        return render_template("signinfailed.html", name=usernm,loggedIn=loggedIn)

    # Fetch password associated w/usernm and test
    passwd_fetch = User.query.filter_by(username=usernm).first()
    #passwd_fetch = db.execute("SELECT password FROM users WHERE global usernm = :username", {"username": usernm}).fetchone()
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

    try:
        query_int = int(query)
    except:
        query_int = -9999

    # flasksqlalchemy query here
    #books = Book.query.filter_by(title=query)
    books = Book.query.filter(or_(Book.title==query, Book.author==query, Book.year==query_int, Book.isbn==query))

    # TO DO: Activate search for similar terms
    #if books == None: # if books is None?
    #    query = "%"+query+"%"
    #    books = Book.query.filter(Book.title.like(query))


    return render_template("searchresults.html", books=books, query=query)

# Book Page
@app.route("/book/<int:book_id>")
def book_id(book_id):
    global usernm, passwd, loggedIn

    # Get Book and associated reviews
    book = Book.query.get(book_id)
    reviews = Review.query.filter_by(book_id=book_id)

    # If book doesnt exist return error page
    if book is None:
        return render_template("book.html")

    return render_template("book.html", reviews=reviews, book=book, loggedIn=loggedIn,username=usernm)

# Add review
@app.route("/addreview", methods=["POST"])
def addreview():
    global usernm, passwd, loggedIn

    user = User.query.filter_by(username=usernm).first()
    user_id = user.id

    if loggedIn == 1:
        review = request.form.get("review")
        book_id = request.form.get("book_id")
        Book.add_review(review=review, book_id=book_id, user_id=user_id)
    else:
        return #error page, not logged in

    # Get Book and associated reviews
    book = Book.query.get(book_id)
    reviews = Review.query.filter_by(book_id=book_id)

    return render_template("book.html", reviews=reviews, book=book, loggedIn=loggedIn,username=usernm)
