from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo_list.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_text = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, default=date.today())
    status_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<File %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
@app.route('/todo', methods=['POST', 'GET'])
def main_page():
    if request.method == 'POST':
        text = request.form['task-text']
        task = Task(task_text=text, status_id=1)
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run()
