from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo_list.db"
db = SQLAlchemy(app)


@app.route('/')
@app.route('/todo')
def main_page():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    task_text = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    task_id = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<File %r>' % self.id
