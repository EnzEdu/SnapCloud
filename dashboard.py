from flask import Blueprint, request, render_template, session, redirect, flash, url_for
from rds import RDS_DATABASE
from s3 import Audio

bp = Blueprint("dashboard", __name__)

@bp.route("/dashboard", methods = ["GET", "POST"])
def dashboard():
    if session.get("id"):
        # submit file (audio, video, image)
        if request.method == "GET":
            audios = RDS_DATABASE.session.query(Audio).filter_by(id_usuario=session.get("id")).all()

        else:
            print("o maluco")
            print(request.forms)

        return render_template("dashboard.html", audios=audios)

    else:
        flash("Você não está logado!", "erro")
        return redirect(url_for('auth.login'))
