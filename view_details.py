from flask import Blueprint, request, render_template, session, redirect, flash, url_for
from rds import RDS_DATABASE, Usuario
from s3 import s3, S3_BUCKET_NAME, Audio, Imagem

bp = Blueprint("view_details", __name__)

@bp.route("/view_details/<id>", methods=["GET", "POST"])
def view_details(id):
    if session.get("id"):
        action = request.form.get("action")
        tipo = request.args.get("type")
        usuario = RDS_DATABASE.session.query(Usuario).filter_by(id=session.get("id")).first()

        if request.method == "GET":
            if tipo == "audio":
                audio = RDS_DATABASE.session.query(Audio).filter_by(id_usuario=session.get("id"), id=id).first()
                return render_template("view_details.html", username=usuario.username, audio=audio)
            elif tipo == "imagem":
                imagem = RDS_DATABASE.session.query(Imagem).filter_by(id_usuario=session.get("id"), id=id).first()
                return render_template("view_details.html", username=usuario.username, imagem=imagem)

        else:
            if (action == "salvar"):
                if tipo == "audio":
                    RDS_DATABASE.session.query(Audio).filter_by(id_usuario=session.get("id"), id=id).update({
                        "file_name": request.form["nome"],
                        "tags": request.form["tags"],
                        "genres": request.form["genero"],
                        "description": request.form["descricao"]
                    })

                elif tipo == "imagem":
                    RDS_DATABASE.session.query(Imagem).filter_by(id_usuario=session.get("id"), id=id).update({
                        "file_name": request.form["nome"],
                        "tags": request.form["tags"],
                        "description": request.form["descricao"]
                    })

                RDS_DATABASE.session.commit()

            elif (action == "excluir"):
                if tipo == "audio":
                    s3.Object(S3_BUCKET_NAME, usuario.username + "/audios/" + request.form["nome"]).delete()
                    RDS_DATABASE.session.query(Audio).filter_by(file_name=request.form["nome"]).delete()

                elif tipo == "imagem":
                    s3.Object(S3_BUCKET_NAME, usuario.username + "/imagens/" + request.form["nome"]).delete()
                    RDS_DATABASE.session.query(Imagem).filter_by(file_name=request.form["nome"]).delete()

                RDS_DATABASE.session.commit()

            return redirect(url_for("dashboard.dashboard"))
