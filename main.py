import datetime
import os
import webbrowser

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

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
    task_files = db.relationship('File', backref='task', lazy='dynamic')

    def __repr__(self):
        return '<Task %r>' % self.id


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    file_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<File %r>' % self.id


def compare(task):
    if task.status_id != 0:
        now = datetime.date.today()
        date = datetime.date.fromisoformat(task.date)
        if now > date:
            task.status_id = 2
        if now < date:
            task.status_id = 1


@app.route('/')
def main_page():
    tasks = Task.query.order_by(Task.status_id.desc()).all()
    for task in tasks:
        compare(task)
    files = [task.task_files.all()[0] for task in tasks]
    return render_template("index.html", tasks=tasks, files=files, statuses=statuses)


@app.route('/<int:id>/<string:filename>')
def open_file(id, filename):
    current_dir = os.getcwd()
    os.chdir('files')
    webbrowser.open('file://' + os.path.realpath(str(id) + '_' + filename))
    os.chdir(current_dir)
    return redirect('/')


@app.route('/add-task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        text = request.form['task-text']
        title = request.form['task-title']
        deadline = request.form['task-deadline']
        task = Task(task_title=title, task_text=text, date=deadline, status_id=1)
        compare(task)
        file_object = request.files['file']
        file1 = File(file_name=file_object.filename, task=task)
        try:
            db.session.add(task)
            db.session.add(file1)
            db.session.commit()
        except Exception as e:
            print(e)
            return "Error"
        current_dir = os.getcwd()
        os.chdir('files')
        file_object.save(str(task.id) + '_' + file_object.filename)
        os.chdir(current_dir)
        return redirect('/')


@app.route('/<int:id>/delete-task')
def delete_task(id):
    task = Task.query.get_or_404(id)
    file = task.task_files.all()[0]
    try:
        db.session.delete(task)
        db.session.delete(file)
        db.session.commit()
    except:
        return "Error"
    current_dir = os.getcwd()
    os.chdir('files')
    os.remove(str(task.id) + '_' + file.file_name)
    os.chdir(current_dir)
    return redirect('/')


@app.route('/<int:id>/update-task', methods=['POST', 'GET'])
def update_task(id):
    task = Task.query.get(id)
    if request.method == 'POST':
        task.task_text = request.form['task-text']
        task.task_title = request.form['task-title']
        task.date = request.form['task-deadline']
        task.status_id = statuses.index(request.form['task-status'])
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template("edit_task.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)
