import os

from flask import Flask, render_template, request
from db_models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ynorvjldptczsr:642db89f29e57eb14c168c81dd9088b79e279edabda65bef8b391d46c31f9d0b@ec2-54-243-137-182.compute-1.amazonaws.com:5432/d1r7oflel96ou"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
