from flask import Flask, url_for, render_template, request, redirect, session, g
from database import get_database, get_current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'student_db'):
        g.student_db.close()


@app.route('/')
def index():
    user = get_current_user()
    return render_template('home.html', user=user)


@app.route('/login', methods=["POST", "GET"])
def login():
    user = get_current_user()
    error = None
    db = get_database()

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_cursor = db.execute('select * from teachers where name = ?', [name])
        user = user_cursor.fetchone()

        if user:
            if check_password_hash(user['password'], password):
                session['user'] = user['name']
                return redirect(url_for('dashboard'))
            else:
                error = "Username or Password did not match"
        else:
            error = "Username or Password did not match"
    return render_template('login.html', login_error=error, user=user)


@app.route('/register', methods=["POST", "GET"])
def register():
    user = get_current_user()
    db = get_database()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        dbuser_cursor = db.execute('select * from teachers where name = ?', [name])
        existing_username = dbuser_cursor.fetchone()

        if existing_username:
            return render_template('register.html', register_error="Username already taken")

        db.execute('insert into teachers ( name, password ) values (?,?)', [name, hashed_password])
        db.commit()
        return redirect(url_for('index'))

    return render_template('register.html', user=user)


@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    db = get_database()
    emp_cursor = db.execute('select * from students')
    all_emp = emp_cursor.fetchall()
    return render_template('dashboard.html', user=user, all_emp=all_emp)


@app.route('/addnewstudent', methods=["POST", "GET"])
def addnewstudent():
    user = get_current_user()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        marks = request.form['marks']
        address = request.form['address']

        db = get_database()
        db.execute(' insert into students (name, email, marks, address) values (?,?,?,?) ',
                   [name, email, marks, address])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('addnewstudent.html', user=user)


@app.route('/fetchone/<int:stuid>')
def fetchone(stuid):
    user = get_current_user()
    db = get_database()
    emp_cursor = db.execute('select * from students where stuid = ?', [stuid])
    single_emp = emp_cursor.fetchone()
    return render_template('updatestudent.html', user=user, single_emp=single_emp)


@app.route('/updatestudent', methods=['POST', 'GET'])
def updatestudent():
    user = get_current_user()
    if request.method == 'POST':
        stuid = request.form['stuid']
        name = request.form['name']
        email = request.form['email']
        marks = request.form['marks']
        address = request.form['address']
        db = get_database()
        db.execute(' update students set name = ?, email = ?, marks = ?, address = ? where stuid = ? ',
                   [name, email, marks, address, stuid])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('updatestudent.html', user=user)


@app.route('/deleteemp/<int:stuid>', methods=['POST', 'GET'])
def deleteemp(stuid):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from students where stuid = ?', [stuid])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
