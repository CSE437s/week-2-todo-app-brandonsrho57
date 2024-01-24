# REFERENCES
# https://flask.palletsprojects.com/en/3.0.x/
# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#installation
# https://github.com/brandonsrho57/Simple_Flask_Clone/tree/main (My own repository)

# Library imports
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Instantiate the app
app = Flask(__name__)

# SQLAlchemy db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Defining a ToDo using the SQL db model
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Root Page
@app.route('/')
def root():
    todo_list = ToDo.query.all()
    return render_template("index.html", todo_list = todo_list)

# What happens on add
@app.route('/add', methods = ["POST"])
def add():
    title = request.form.get("title")
    new_todo = ToDo(title = title, complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("root"))

# What happens on update
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = ToDo.query.filter_by(id = todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("root"))

# What happens on delete
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = ToDo.query.filter_by(id = todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("root"))

# Creating db
with(app.app_context()):
    db.create_all()

# Running the app
if __name__ == "__main__":
    app.run(debug=True)