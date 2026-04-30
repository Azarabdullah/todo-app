from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from database import init_db

app = Flask(__name__)

# helper function to connect to database...
def get_db():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn

# home page ---- shows all tasks
@app.route('/')
def index():
    conn = get_db()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Add a new task
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    conn = get_db()
    conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# mark a task as complete
@app.route('/complete/<int:id>')
def complete(id):
    conn = get_db()
    conn.execute('UPDATE tasks SET done = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# delete a task
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  #create database on startup
    app.run(debug=True)