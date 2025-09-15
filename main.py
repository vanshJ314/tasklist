from flask import Flask, render_template , request, redirect, url_for
from db import deleteTask, getTaskList, addTask, updateTask 
app = Flask(__name__)


@app.route('/')
def home():
    taskList = getTaskList()
    return render_template('tasklist.html', TaskList=taskList)

@app.route('/add', methods=['POST'])
def add():
    taskName = request.form['taskName']
    duedate = request.form['dueDate']
    addTask(taskName, duedate)
    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def update():
    updatedtaskname = request.form['updateTask']
    id = request.form['id']
    button = request.form['saveOrDelete']
    if button == 'save':
        updateTask(updatedtaskname, id)
    elif button == 'X':
        deleteTask(id)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)