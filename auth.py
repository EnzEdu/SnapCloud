import os
import uuid
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import uuid
from rds import RDS_DATABASE, Usuario
from edit_profile import update_profile_picture
import pymysql
from s3 import s3, S3_BUCKET_NAME, S3_BUCKET_REGION, Imagem
import boto3

bp = Blueprint("auth", __name__)

@bp.route('/', methods=["GET"])
def main_page():
    return redirect(url_for("auth.login"))

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
        id_profile_picture = -1

        hashed_password = generate_password_hash(password)

        if len(request.files) != 0:
            uploaded_file = request.files['filename']
            novo_filename = uuid.uuid4().hex + "." + uploaded_file.filename.rsplit(".", 1)[1].lower()

            file_name = uploaded_file.filename
            file_size = uploaded_file.seek(0, os.SEEK_END)
            uploaded_file.seek(0, os.SEEK_SET)
            bucket_file_name = novo_filename
            upload_date = creation_date
            mime_type = ""
            width = 0
            height = 0
            color_depth = 0
            resolution = 0
            exif_data = ""
            description = ""
            tags = ""

        try:
            email_existe = RDS_DATABASE.session.query(Usuario.id).filter_by(email=email).first() is not None
            senha_existe = RDS_DATABASE.session.query(Usuario.id).filter_by(password=hashed_password).first() is not None

            if senha_existe == True or email_existe == True:
                raise pymysql.IntegrityError("")


            if len(request.files) != 0:
                img_obj = Imagem(
                    s3_bucket_nome=S3_BUCKET_NAME,
                    s3_bucket_regiao=S3_BUCKET_REGION,
                    file_name=file_name,
                    bucket_file_name=bucket_file_name,
                    file_size=file_size,
                    upload_date=upload_date,
                    mime_type=mime_type,
                    width=width,
                    height=height,
                    color_depth=color_depth,
                    resolution=resolution,
                    exif_data=exif_data,
                    description=description,
                    tags=tags
                )

                RDS_DATABASE.session.add(img_obj)
                s3.Bucket(S3_BUCKET_NAME).upload_fileobj(uploaded_file, novo_filename)

                id_profile_picture = RDS_DATABASE.session.query(Imagem.id).filter_by(bucket_file_name=bucket_file_name).first()
                id_profile_picture = id_profile_picture[0]

            user_obj = Usuario(
                full_name=full_name,
                username=username,
                password=hashed_password,
                email=email,
                description=description,
                creation_date=creation_date,
                id_profile_picture=id_profile_picture
            )

            RDS_DATABASE.session.add(user_obj)
            RDS_DATABASE.session.commit()
            flash('Conta criada com sucesso!', 'sucesso')
            return redirect(url_for('auth.login'))
        except Exception as ex:
            print(str(ex))
            flash('Senha ou email já existem. Por favor, altere esses dados', 'erro')

    return render_template('register.html')
