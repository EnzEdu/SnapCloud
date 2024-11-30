from flask import Flask, request, render_template, flash, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def update_profile_picture(profile_picture):
    profile_picture = profile_picture
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            profile_picture = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(profile_picture)
    return profile_picture

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            description TEXT,
            creation_date TEXT NOT NULL,
            profile_picture TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        description = request.form['description']
        creation_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        profile_picture = update_profile_picture('static/default-placeholder.jpg')

        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (full_name, username, password, email, description, creation_date, profile_picture)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (full_name, username, hashed_password, email, description, creation_date, profile_picture))
            conn.commit()
            conn.close()
            flash('Account created successfully!', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash('Username or email already exists. Please choose a different one.', 'error')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password, id FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()

        if row and check_password_hash(row[0], password):
            session['id'] = row[1]
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'username' not in session:
        flash('You must be logged in to access settings.', 'error')
        return redirect('/login')
    
    id = session['id']
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT full_name, username, email, password, description, profile_picture FROM users WHERE id = ?', (id,))
    user = cursor.fetchone()
    conn.close()

    username = session['username']
    password = user[3]
    current_profile_picture = user[5]

    if request.method == 'POST':
        if 'update' in request.form:
            full_name = request.form['full_name']
            username = request.form['username']
            email = request.form['email']
            if request.form['password']:
                password = generate_password_hash(request.form['password'])
            description = request.form['description']
            profile_picture = update_profile_picture(current_profile_picture)

            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users
                SET full_name = ?, username = ?, email = ?, password = ?, description = ?, profile_picture = COALESCE(?, profile_picture)
                WHERE id = ?
            ''', (full_name, username, email, password, description, profile_picture, id))
            conn.commit()
            conn.close()
            flash('Your settings have been updated.', 'success')
            return redirect('/login')

        elif 'delete' in request.form:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()
            conn.close()
            session.clear()
            flash('Your account has been deleted.', 'success')
            return redirect('/register')

    return render_template('settings.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT full_name, email, description, creation_date, profile_picture FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        return render_template('dashboard.html', user=user)
    else:
        flash('You must be logged in to access the dashboard.', 'error')
        return redirect('/login')

@app.route('/users')
def show_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, full_name, username, email, password, description, creation_date, profile_picture FROM users')
    rows = cursor.fetchall()
    conn.close()

    return render_template('users.html', users=rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
