import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

# Launch Postgre session
engine = create_engine("postgres://ynorvjldptczsr:642db89f29e57eb14c168c81dd9088b79e279edabda65bef8b391d46c31f9d0b@ec2-54-243-137-182.compute-1.amazonaws.com:5432/d1r7oflel96ou")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)

    # Create new table, 'books'
    # db.execute("CREATE TABLE books(id SERIAL PRIMARY KEY,isbn VARCHAR NOT NULL,title VARCHAR NOT NULL,author VARCHAR NOT NULL, year INTEGER NOT NULL)")

    # For each row in csv
    for isbn, title, author, year in reader:
        print(f"year: {year}")
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added isbn:{isbn}, title:{title}, author:{author}, year:{year}")

    # Commit Changes
    db.commit()

if __name__ == "__main__":
    main()
