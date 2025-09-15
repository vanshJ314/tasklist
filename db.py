import psycopg2
db_name = "TaskListDB"
db_user = "tasklist_user"
db_pw = "vansh"
db_host = "localhost"

def getTaskList():
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_pw,
        host=db_host,
    )
    cur = conn.cursor()
    cur.execute('SELECT task_name, Is_Active FROM public."TaskList"')
    taskList = cur.fetchall()
    cur.close()
    conn.close()
    return taskList