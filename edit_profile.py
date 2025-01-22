from flask import request, Blueprint, session, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from utilities import allowed_file
import os
from rds import RDS_DATABASE, Usuario
from s3 import Imagem, S3_BUCKET_NAME, S3_BUCKET_REGION, s3, s3_client
import pymysql
import uuid
from datetime import datetime
from PIL import Image
import io
import piexif

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

                if len(request.files['filename'].filename) != 0:
                    try:
                        uploaded_file = request.files['filename']
                        if uploaded_file and allowed_file(uploaded_file.filename) == False:
                            raise TypeError("")
                    except Exception as ex:
                        flash("Erro de extensao!", "erro")
                        return redirect(url_for("dashboard.dashboard"))
                    fileimage = Image.open(uploaded_file)

                    file_size = uploaded_file.seek(0, os.SEEK_END)
                    uploaded_file.seek(0, os.SEEK_SET)
                    novo_filename = username + "/profile" + "." + uploaded_file.content_type.split("/", 1)[1].lower()
                    dpi = fileimage.info.get('dpi', ('Unknown', 'Unknown'))
                    exif_data = ""
                    try:
                        exif_dict = piexif.load(fileimage.info['exif'])
                        exif_data = {piexif.TAGS[key]: exif_dict['0th'].get(key, 'N/A') for key in exif_dict['0th']}
                    except:
                        exif_data = ""
                    description = ""
                    tags = ""

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

                    if len(request.files['filename'].filename) != 0:
                        usuario = RDS_DATABASE.session.query(Usuario).filter_by(id=session.get("id")).first()

                        procura_profile = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=username + "/")
                        if 'Contents' in procura_profile:
                            profile_antigo = [obj['Key'] for obj in procura_profile['Contents'] if obj['Key'].lower().startswith(username + "/" + 'profile')]

                            if profile_antigo:
                                nome_profile_antigo = profile_antigo[0]
                                s3.Object(S3_BUCKET_NAME, nome_profile_antigo).delete()

                        s3.Bucket(S3_BUCKET_NAME).upload_fileobj(uploaded_file, novo_filename)

                        img_obj = Imagem(
                            id_usuario=-1,
                            s3_bucket_nome=S3_BUCKET_NAME,
                            s3_bucket_regiao=S3_BUCKET_REGION,
                            file_name=uploaded_file.filename,
                            file_size=file_size,
                            bucket_file_name=novo_filename,
                            upload_date=datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                            mime_type=uploaded_file.content_type,
                            width=fileimage.width,
                            height=fileimage.height,
                            color_depth=fileimage.mode,
                            resolution_dpi_x=dpi[0],
                            resolution_dpi_y=dpi[1],
                            exif_data=exif_data,
                            description=description,
                            tags=tags
                        )

                        RDS_DATABASE.session.add(img_obj)
                        RDS_DATABASE.session.commit()

                        id_profile_picture = RDS_DATABASE.session.query(Imagem.id).filter_by(bucket_file_name=novo_filename).first()
                        id_profile_picture = id_profile_picture[0]

                        RDS_DATABASE.session.query(Usuario).filter_by(id=session.get("id")).update({
                            "id_profile_picture": id_profile_picture
                        })

                        RDS_DATABASE.session.commit()

                    session["hashed_password"] = password # salva a nova senha ou senha inalterada na >

                except Exception as ex:
                    if isinstance(ex, pymysql.err.IntegrityError):
                        flash("Nome de usuario já em uso", "erro") # testando se usar o mesmo nome de >
                    else:
                        flash("Ocorreu um erro", "erro")
                    print(str(ex))
                    return redirect(url_for('dashboard.dashboard'))

                flash("Dados válidos atualizados com sucesso", "sucesso")
                return redirect(url_for('dashboard.dashboard'))


        if request.method == 'GET':
            # Recupera as informações para mostrar na página de edição
            user = RDS_DATABASE.session.query(Usuario).filter_by(id=session.get('id')).first()
            pfp = RDS_DATABASE.session.query(Imagem).filter_by(id=user.id_profile_picture).first()

            if user is not None:
                session["hashed_password"] = user.password
                if (pfp is not None):
                    return render_template("edit_profile.html", user=user, pfp=pfp)
                else:
                    return render_template("edit_profile.html", user=user, pfp="static/img/lets-icons--user-box-duotone.png")
            else:
                flash("Você não está logado!", "erro")
                return redirect(url_for('auth.login'))

    else:
        flash("Você não está logado!", "erro")
        return redirect(url_for('auth.login'))