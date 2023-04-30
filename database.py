from flask import g, session
import sqlite3 

def connect_to_database():
    sql = sqlite3.connect('studentDatabase.db')
    sql.row_factory = sqlite3.Row
    return sql 

def get_database():
    if not hasattr(g, 'student_db'):
        g.student_db = connect_to_database()
    return g.student_db

def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
        db = get_database()
        user_cur = db.execute('select * from teachers where name = ?', [user])
        user = user_cur.fetchone()
        return user
