'''codementor.io Building a CRUD application with Flask and SQLAlchemy by Gareth Dwyer.'''
# adding a model to our web app - OK
    # Pylint issue: pip install pylint-flasks, pip install pylint_flask_sqlalchemy > add "python.linting.pylintArgs": ["--load-plugins", "pylint-flask"], to .vscode/settings.json
# creating and storing books - no problem it seems
    # IntegrityError - try-except solves
# initializing our database - unsure if in effect
# retrieving books from out db - addBook(), global books solves
    # UnboundLocalError: local variable 'books' (sometimes TypeError) = inflow enters db, but 2nd round read fails 
# skip to deleting - works but only after save&reload
    #NOTE: can only be done one at a time, but can also del-reload-del-reload-save-reload to del twice
    # sqlalchemy.orm.exc.UnmappedInstanceError: Class 'builtins.NoneType' is not mapped - deleteBook() solves
    # reformat view by copy/paste html - OK
# updating book titles NOTE: Taweesin says this is normal, forums say autoreloads need client-side JS/JQuery.
    # sometimes UnboundLocalError at click update, when comment off global books, but OK when refresh homepage 
    # NOTE: AttributeError: 'NoneType' object has no attribute 'title'
        # NOTE: CANNOT
        # update reload
        # update error back reload fail
        # CAN save and reload - why
        # update two records at once, page refreshes old data at update press
        # CAN update one at a time before reload once
        
    


import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

def addBook(title):
    book = Book(title=request.form.get(str(title)))
    try:
        db.session.add(book)
        return db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()

def updateBook(newtitle):
    newtitle = request.form.get(str(newtitle))
    oldtitle = request.form.get("oldtitle")
    book = Book.query.filter_by(title=oldtitle).first()
    try:
        book.title = newtitle # assignment successful
        return db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()

def deleteBook(title):
    title = request.form.get(str(title))
    book = Book.query.filter_by(title=title).first()
    try:
        db.session.delete(book)
        return db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()

books = Book.query.all()
@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        addBook("title")
        global books
        books = Book.query.all()
    return render_template("home.html", books=books)

@app.route("/update", methods=["POST"])
def update():
    updateBook("newtitle")
    return redirect("/") # fails to refresh page - Taweesin says this is normal.

@app.route("/delete", methods=["POST"])
def delete():
    deleteBook("title")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)