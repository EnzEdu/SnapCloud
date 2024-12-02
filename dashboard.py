from flask import Blueprint, request, render_template, session, redirect, flash, url_for

bp = Blueprint("dashboard", __name__)

@bp.route("/dashboard", methods = ["GET", "POST"])
def dashboard():
    if session.get("id"):
        # submit file (audio, video, image)
        if request.method == "POST":
            pass

        return render_template("dashboard.html")
    
    else:
        flash("Você não está logado!", "erro")
        return redirect(url_for('auth.login'))