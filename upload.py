from flask import Blueprint, request, render_template, session, redirect, flash, url_for
from rds import RDS_DATABASE, Usuario
from s3 import s3, S3_BUCKET_NAME, S3_BUCKET_REGION, Imagem
from PIL import Image
import io
import piexif
import uuid
import os
from upload_audio import upload_audio
from upload_image import upload_image

bp = Blueprint("upload", __name__)

@bp.route("/upload", methods=["POST"])
def upload():
    if (session.get("id")):
        if (request.method == "POST"):

            files = request.files
            if len(request.files) == 0:
                return redirect(url_for("dashboard.dashboard"))

            usuario = RDS_DATABASE.session.query(Usuario).filter_by(id=session.get("id")).first()
            for index_fileobj in range(0, len(files.getlist('files'))):
                fileobj = files.getlist('files')[index_fileobj]
                file_mime = fileobj.content_type
                file_type = file_mime.split("/", 1)[0].lower()

                description = request.form['description-' + str(index_fileobj)]
                tags = request.form['tags-' + str(index_fileobj)]
                genres = request.form['genre-' + str(index_fileobj)]
                args = [description, tags, genres, usuario.id]


                result = ""
                folder = ""
                if (file_type == "audio"):
                    result = upload_audio(fileobj, args)
                    folder = "audios"

                elif (file_type == "image"):
                    result = upload_image(fileobj, args)
                    folder = "imagens"

                else:
                    flash("Arquivo desconhecido", "erro")
                    continue


                if (result[0] == True):
                    print(result[1].mime_type, " ", result[1].upload_date)
                    RDS_DATABASE.session.add(result[1])
                    RDS_DATABASE.session.commit()
                    s3.Bucket(S3_BUCKET_NAME).upload_fileobj(fileobj, usuario.username + "/" + folder + "/" + result[1].file_name)

                else:
                    flash("Arquivo de" + file_type + "invalido", "erro")

    return redirect(url_for("dashboard.dashboard"))
