import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from datetime import datetime
from utilities import DB_NAME
from edit_profile import update_profile_picture

bp = Blueprint("auth", __name__)

@bp.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form["usuario"]
        password = request.form["senha"]

        conn = sqlite3.connect(DB_NAME, timeout = 10)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        user = cursor.execute("select id, password from users where username = ?", (username,)).fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["password"], password):
            flash('Login realizado com sucesso', 'sucesso')
            session.clear()
            session['id'] = user["id"]
            
            return redirect(url_for('dashboard.dashboard'))
        
        else:
            flash('Nome de usuário ou senha incorretos', 'erro')

    return render_template("login.html")

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['nome']
        username = request.form['usuario']
        password = request.form['senha']
        email = request.form['email']
        description = ""
        creation_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        profile_picture = update_profile_picture('static/default-placeholder.jpg')

        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect(DB_NAME, timeout=10)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (full_name, username, password, email, description, creation_date, profile_picture)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (full_name, username, hashed_password, email, description, creation_date, profile_picture))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Conta criada com sucesso!', 'sucesso')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('Senha ou email já existem. Por favor, altere esses dados', 'erro')

    return render_template('register.html')