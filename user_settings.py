from flask import Blueprint, request, render_template, session, redirect, flash, url_for

bp = Blueprint("user_settings", __name__)

@bp.route("/user_settings", methods = ["GET", "POST"])
def user_settings():
    if session.get("id"):
        # update user
        if request.method == "POST":
            pass

        return render_template("/user_settings.html")

    else:
        flash("You are not logged!")
        return redirect(url_for('auth.login'))