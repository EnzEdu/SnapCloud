from flask import Blueprint, request, render_template, session, redirect, flash, url_for
from rds import RDS_DATABASE, Usuario
from s3 import Audio, Imagem

bp = Blueprint("dashboard", __name__)

@bp.route("/dashboard", methods = ["GET", "POST"])
def dashboard():
    if session.get("id"):
        # submit file (audio, video, image)
        usuario = RDS_DATABASE.session.query(Usuario).filter_by(id=session.get("id")).first()
        if request.method == "GET":
            audios = RDS_DATABASE.session.query(Audio).filter_by(id_usuario=session.get("id")).all()
            imagens = RDS_DATABASE.session.query(Imagem).filter_by(id_usuario=session.get("id")).all()

        return render_template("dashboard.html", user=usuario, audios=audios, imagens=imagens)

    else:
        flash("Você não está logado!", "erro")
        return redirect(url_for('auth.login'))
