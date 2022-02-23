from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo_list.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
@app.route('/todo', methods=['POST', 'GET'])
def main_page():
    if request.method == 'POST':
        text = request.form['task-text']
        date = request.form['task-date']
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_text = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    status_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    task_id = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<File %r>' % self.id
