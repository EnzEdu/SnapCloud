from flask import Blueprint, request, render_template, session, redirect, flash, url_for, current_app
from utilities import allowed_video_file, generate_thumbnail
import os
from werkzeug.utils import secure_filename
from utilities import allowed_video_file, generate_thumbnail, save_video_to_db
from utilities import get_user_videos
from utilities import allowed_video_file, generate_thumbnail, generate_resolutions

bp = Blueprint("dashboard", __name__)

@bp.route("/dashboard", methods = ["GET", "POST"])
def dashboard():
    if session.get("id"):
        user_id = session.get("id") # Restringir o acesso dos vídeos apenas para o proprietário -
        # submit file (audio, video, image)
        if request.method == "POST":
            file = request.files.get("file")
            if file and allowed_video_file(file.filename):
                filename = secure_filename(file.filename)
                video_path = os.path.join(current_app.config['VIDEO_UPLOAD_FOLDER'], filename)
                file.save(video_path)
                flash("Arquivo enviado com sucesso!", "sucesso")

                # Gerar thumbnail do vídeo
                thumbnail_path = generate_thumbnail(video_path)

                # Gerar resoluções
                resolution_paths = generate_resolutions(video_path)

                # Salvar informações no banco de dados
                save_video_to_db(
                    user_id=session["id"],
                    filename=filename,
                    filepath=video_path,
                    thumbnail_path=thumbnail_path,
                )

                if thumbnail_path:
                    flash(f"Vídeo enviado e thumbnail gerado em: {thumbnail_path}", "sucesso")
                else:
                    flash("Falha ao gerar o thumbnail.", "erro")
        else:
            flash("Formato de arquivo não suportado!", "erro")

        # Buscar vídeos do usuário
        user_videos = get_user_videos(user_id)
        return render_template("dashboard.html", videos=user_videos)

    else:
        flash("Você não está logado!", "erro")
        return redirect(url_for('auth.login'))
