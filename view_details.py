from flask import Blueprint, request, render_template, session, redirect, flash, url_for
from rds import RDS_DATABASE, Usuario
from s3 import s3, S3_BUCKET_NAME, Audio

bp = Blueprint("view_details", __name__)

@bp.route("/view_details/<id>", methods=["GET", "POST"])
def view_details(id):
    if session.get("id"):
        action = request.form.get("action")

        if request.method == "GET":
            audio = RDS_DATABASE.session.query(Audio).filter_by(id_usuario=session.get("id"), id=id).first()
            usuario = RDS_DATABASE.session.query(Usuario).filter_by(id=session.get("id")).first()

            return render_template("view_details.html", username=usuario.username, audio=audio)

        else:
            print(request.form)
            if (action == "salvar"):
                RDS_DATABASE.session.query(Audio).filter_by(id_usuario=session.get("id"), id=id).update({
                    "file_name": request.form["nome"],
                    "tags": request.form["tags"],
                    "genres": request.form["genero"],
                    "description": request.form["descricao"]
                })
                RDS_DATABASE.session.commit()

            elif (action == "excluir"):
                usuario = RDS_DATABASE.session.query(Usuario).filter_by(id=session.get("id")).first()
                s3.Object(S3_BUCKET_NAME, usuario.username + "/audios/" + request.form["nome"]).delete()
                RDS_DATABASE.session.query(Audio).filter_by(file_name=request.form["nome"]).delete()
                RDS_DATABASE.session.commit()

            return redirect(url_for("dashboard.dashboard"))