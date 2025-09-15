from flask import Flask, render_template

app = Flask(__name__)

taskList = [
    ["Walk Dog", True],
    ["Wash Car", False],
    ["Take Out Trash", True]
]
@app.route('/')
def home():
    return render_template('tasklist.html', TaskList=taskList)

if __name__ == "__main__":
    app.run(debug=True)