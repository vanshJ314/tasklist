import psycopg2
from datetime import datetime

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
    cur.execute('''
        SELECT id, task_name, Is_Done, due_date, created_at 
        FROM public."TaskList" 
        ORDER BY Is_Done ASC, due_date ASC, created_at DESC
    ''')
    taskList = cur.fetchall()
    cur.close()
    conn.close()
    return taskList

def executeQuery(query, params=()):
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_pw,
        host=db_host,
    )
    cur = conn.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

def addTask(name, date):
    # If no date provided, set to None
    due_date = date if date else None
    created_at = datetime.now()
    executeQuery('''
        INSERT INTO public."TaskList" (task_name, due_date, created_at, Is_Done) 
        VALUES (%s, %s, %s, %s);
    ''', (name, due_date, created_at, False))

def updateTask(name, id):
    executeQuery('UPDATE public."TaskList" SET task_name = %s WHERE id = %s;', (name, id))

def deleteTask(id):
    executeQuery('DELETE FROM public."TaskList" WHERE id = %s;', (id,))

def toggleTaskCompletion(id):
    executeQuery('UPDATE public."TaskList" SET Is_Done = NOT Is_Done WHERE id = %s;', (id,))

# Database setup function (run this once to update your table structure)
def updateTableStructure():
    """
    Run this function once to add the created_at column if it doesn't exist
    """
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_pw,
            host=db_host,
        )
        cur = conn.cursor()
        
        # Add created_at column if it doesn't exist
        cur.execute('''
            ALTER TABLE public."TaskList" 
            ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        ''')
        
        # Update existing rows with current timestamp if they don't have one
        cur.execute('''
            UPDATE public."TaskList" 
            SET created_at = CURRENT_TIMESTAMP 
            WHERE created_at IS NULL;
        ''')
        
        conn.commit()
        cur.close()
        conn.close()
        print("Table structure updated successfully!")
        
    except Exception as e:
        print(f"Error updating table structure: {e}")

if __name__ == "__main__":
    # Uncomment the line below and run this file once to update your database structure
    updateTableStructure()