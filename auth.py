import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import datetime
from utilities import DB_NAME

bp = Blueprint("auth", __name__)

@bp.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        error = None

        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        user = cursor.execute("select id, password from users where username = ?", (username,)).fetchone()
        conn.close()

        if user is None:
            error = "Incorrect username"

        elif check_password_hash(user["password"], password):
            session.clear()
            session['id'] = user["id"]
            
            return redirect(url_for('dashboard.dashboard'))
        
        else:
            error = "Incorrect password"
            
        flash(error)

    return render_template("login.html")

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("auth.login"))