from flask import Flask,request,jsonify
import sqlite3
import os

app=Flask(__name__)
DB_FILE="notes.db"

def init_db():
    """Initializes the databse and creates the notes table if its doesn't exist. """
    conn=sqlite3.connect(DB_FILE)
    cursor=conn.cursor()
    cursor.execute('''Create table if not exists 
    notes(id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/notes', methods=['GET','POST'])

def handle_notes():
    """Handles GET requests to fetch all notes and POST requests to add a new note. """
    conn=sqlite3.connect(DB_FILE)
    conn.row_factory=sqlite3.Row #This allows accesing columns by name
    cursor=conn.cursor()
    if request.method == 'POST':
        if not request.json or 'content' not in request.json:
            return jsonify({'error':'The new note must have content'}),400
        content=request.json['content']    
        cursor.execute('INSERT INTO notes(content) VALUES(?)',(content,))
        conn.commit()
        conn.close()
        return jsonify({'message':'Note added successfuly'}),201
    
    if request.method == 'GET':
        cursor.execute('SELECT * FROM notes')
        notes= [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(notes)
    
@app.route('/health')
def health_check():
    return "OK",200
if __name__ == '__main__':
    init_db()#Ensure the database is ready before running the app
    app.run(host='0.0.0.0',port=5000,debug=True)

