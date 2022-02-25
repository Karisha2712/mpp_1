import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo_list.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
statuses = ['Done', 'Processing', 'Expired']


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String(40), nullable=False)
    task_text = db.Column(db.Text, nullable=False)
    date = db.Column(db.String, nullable=False)
    status_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<File %r>' % self.id


@app.route('/')
def main_page():
    tasks = Task.query.order_by(Task.status_id.desc()).all()
    return render_template("index.html", tasks=tasks, statuses=statuses)


@app.route('/add-task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        text = request.form['task-text']
        title = request.form['task-title']
        deadline = request.form['task-deadline']
        task = Task(task_title=title, task_text=text, date=deadline, status_id=1)
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"


@app.route('/<int:id>/delete-task')
def delete_task(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "Error"


@app.route('/<int:id>/update-task', methods=['POST', 'GET'])
def update_task(id):
    task = Task.query.get(id)
    if request.method == 'POST':
        task.task_text = request.form['task-text']
        task.task_title = request.form['task-title']
        task.date = request.form['task-deadline']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template("edit_task.html", task=task)


scheduler = APScheduler()
scheduler.init_app(app=app)
scheduler.start()


@scheduler.scheduler.scheduled_job(trigger='interval', id='apscheduler', seconds=1)
def apscheduler():
    tasks = Task.query.all()
    now = datetime.date.today()
    for task in tasks:
        date = datetime.date.fromisoformat(task.date)
        if now > date and task.status_id != 2:
            task.status_id = 2
        if now < date and task.status_id != 1:
            task.status_id = 1
    try:
        db.session.commit()
    except:
        return "Error"
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
