from flask import Blueprint, request, jsonify, current_app, session,flash, redirect, url_for
from utilities import  UPLOAD_FOLDER, DB_NAME
import os
from werkzeug.utils import secure_filename
import sqlite3

bp = Blueprint("upload", __name__)

@bp.route("/upload", methods = ["POST", "GET"])
def upload():
    if session.get("id"):

        # The user chose its file. Send the file data to fill the page.
        if request.method == "POST":
            filename = secure_filename(request.form["files"])

            return redirect("")

        # The user didn't choose its file yet.
        elif request.method == "GET":
            pass

    else:
        flash("Você não está logado!", "erro")
        return redirect(url_for('auth.login'))