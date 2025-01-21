from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import uuid
from rds import RDS_DATABASE, Usuario
from edit_profile import update_profile_picture
import pymysql

bp = Blueprint("auth", __name__)


@bp.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form["usuario"]
        password = request.form["senha"]

        user = RDS_DATABASE.session.query(Usuario.id, Usuario.password).filter_by(username=username).first()
        if user is not None:
            if check_password_hash(user[1], password) == True:
                flash('Login realizado com sucesso', 'sucesso')
                session.clear()
                session['id'] = user[0]
            
                return redirect(url_for('dashboard.dashboard'))
            else:
                flash('Nome de usuário ou senha incorretos', 'erro')
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

        id = uuid.uuid4().hex
        hashed_password = generate_password_hash(password)

        try:
            email_existe = RDS_DATABASE.session.query(Usuario.id).filter_by(email=email).first() is not None
            senha_existe = RDS_DATABASE.session.query(Usuario.id).filter_by(password=hashed_password).first() is not None

            if senha_existe == True or email_existe == True:
                raise pymysql.IntegrityError("")

            user_obj = Usuario(
                id=id, 
                full_name=full_name,
                username=username,
                password=hashed_password,
                email=email,
                description=description,
                creation_date=creation_date,
                profile_picture=profile_picture
            )
            
            RDS_DATABASE.session.add(user_obj)
            RDS_DATABASE.session.commit()
            flash('Conta criada com sucesso!', 'sucesso')
            return redirect(url_for('auth.login'))
        except Exception as ex:
            flash('Senha ou email já existem. Por favor, altere esses dados', 'erro')

    return render_template('register.html')