from flask import request, Blueprint, session, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from utilities import allowed_file
import os
from rds import RDS_DATABASE, Usuario
from s3 import Imagem, S3_BUCKET_NAME, s3
import pymysql
import uuid
from datetime import datetime

bp = Blueprint("edit_profile", __name__)

# TODO: adicionar profile_picture
# TODO: refatorar
@bp.route('/edit_profile', methods = ["GET", "POST"])
def edit_profile():
    if session.get("id"):
        if request.method == 'POST':
            action = request.form.get("action")

            if (action == "cancelar"):
                return redirect(url_for('dashboard.dashboard'))

            elif (action == "salvar"):
                full_name = request.form["nome"]
                username = request.form["usuario"]
                password = request.form["senha"]
                email = request.form["email"]
                description = request.form["descricao"]

                if len(request.files) != 0:
                    uploaded_file = request.files['filename']
                    file_size = uploaded_file.seek(0, os.SEEK_END)
                    uploaded_file.seek(0, os.SEEK_SET)
                    hashed_filename = uuid.uuid4().hex + "." + uploaded_file.filename.rsplit(".", 1)[1].lower()

                is_the_password_the_same = (password == session["hashed_password"])

                try:
                    # senha menor do que 6 caracteres ou inalterada
                    if len(password) < 6 or is_the_password_the_same:

                        # Checa se o nome de usuário existe
                        result = RDS_DATABASE.session.query(Usuario).filter_by(username=username).first()
                        if result is not None:
                            RDS_DATABASE.session.query(Usuario).filter_by(id=session.get("id")).update({
                                "full_name": full_name,
                                "email": email,
                                "description": description
                            })
                        else:
                            RDS_DATABASE.session.query(Usuario).filter_by(id=session.get("id")).update({
                                "full_name" : full_name,
                                "username": username,
                                "email": email,
                                "description": description
                            })

                        RDS_DATABASE.session.commit()

                        if len(password) < 6:
                            flash("Não são permitidas senhas com menos de 6 caracteres", "erro")
                            return redirect(url_for('dashboard.dashboard'))

                    else:
                        hashed_password = generate_password_hash(password) # hasheia a nova senha

                        # Checa se o nome de usuário existe
                        result = RDS_DATABASE.session.query(Usuario).filter_by(username=username).first()
                        if result is not None:
                            RDS_DATABASE.session.query(Usuario).filter_by(id=session.get("id")).update({
                                "full_name": full_name,
                                "email": email,
                                "password": hashed_password,
                                "description": description
                            })
                        else:
                            RDS_DATABASE.session.query(Usuario).filter_by(id=session.get("id")).update({
                                "full_name" : full_name,
                                "username": username,
                                "email": email,
                                "password": hashed_password,
                                "description": description
                            })

                        RDS_DATABASE.session.commit()

                    if len(request.files) != 0:
                        s3.Bucket(S3_BUCKET_NAME).upload_fileobj(uploaded_file, hashed_filename)

                        usuario = RDS_DATABASE.session.query(Usuario).filter_by(id=session.get("id")).first()

                        RDS_DATABASE.session.query(Imagem).filter_by(id=usuario.id_profile_picture).update({
                            "file_name": uploaded_file.filename,
                            "file_size": file_size,
                            "bucket_file_name": hashed_filename,
                            "upload_date": datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                        })
                        RDS_DATABASE.session.commit()

                    session["hashed_password"] = password # salva a nova senha ou senha inalterada na >

                except Exception as ex:
                    if isinstance(ex, pymysql.err.IntegrityError):
                        flash("Nome de usuario já em uso", "erro") # testando se usar o mesmo nome de >
                    else:
                        flash("Ocorreu um erro", "erro")
                    return redirect(url_for('dashboard.dashboard'))

                flash("Dados válidos atualizados com sucesso", "sucesso")
                return redirect(url_for('dashboard.dashboard'))


        if request.method == 'GET':
            # Recupera as informações para mostrar na página de edição
            user = RDS_DATABASE.session.query(Usuario).filter_by(id=session.get('id')).first()
            pfp = RDS_DATABASE.session.query(Imagem).filter_by(id=user.id_profile_picture).first()

            if user is not None:
                session["hashed_password"] = user.password
                return render_template("edit_profile.html", user=user, pfp=pfp)
            else:
                flash("Você não está logado!", "erro")
                return redirect(url_for('auth.login'))

    else:
        flash("Você não está logado!", "erro")
        return redirect(url_for('auth.login'))


def update_profile_picture(profile_picture):
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            profile_picture = os.path.join('static/uploads', filename)
            file.save(profile_picture)
    return profile_picture
