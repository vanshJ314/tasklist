from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from db import deleteTask, getTaskList, addTask, updateTask, toggleTaskCompletion
from datetime import datetime, date
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

@app.route('/')
def home():
    taskList = getTaskList()
    # Add status information to each task
    enhanced_tasks = []
    today = date.today()
    
    for task in taskList:
        task_dict = {
            'id': task[0],
            'name': task[1], 
            'is_done': task[2],
            'due_date': task[3],
            'created_at': task[4] if len(task) > 4 else None
        }
        
        # Determine task status
        if task_dict['is_done']:
            task_dict['status'] = 'completed'
        elif task_dict['due_date'] and task_dict['due_date'] < today:
            task_dict['status'] = 'overdue'
        else:
            task_dict['status'] = 'pending'
            
        enhanced_tasks.append(task_dict)
    
    return render_template('tasklist.html', TaskList=enhanced_tasks)

@app.route('/add', methods=['POST'])
def add():
    taskName = request.form['taskName'].strip()
    duedate = request.form['dueDate']
    
    # Validate input
    if not taskName:
        flash('Task name cannot be empty!', 'error')
        return redirect(url_for('home'))
    
    try:
        addTask(taskName, duedate)
        flash('Task added successfully!', 'success')
    except Exception as e:
        flash('Error adding task. Please try again.', 'error')
    
    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def update():
    updatedtaskname = request.form['updateTask'].strip()
    id = request.form['id']
    button = request.form['saveOrDelete']
    
    try:
        if button == 'save':
            if not updatedtaskname:
                flash('Task name cannot be empty!', 'error')
            else:
                updateTask(updatedtaskname, id)
                flash('Task updated successfully!', 'success')
        elif button == 'delete':
            deleteTask(id)
            flash('Task deleted successfully!', 'success')
    except Exception as e:
        flash('Error updating task. Please try again.', 'error')
    
    return redirect(url_for('home'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_completion(task_id):
    try:
        toggleTaskCompletion(task_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task_route(task_id):
    try:
        deleteTask(task_id)
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        flash('Error deleting task. Please try again.', 'error')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)