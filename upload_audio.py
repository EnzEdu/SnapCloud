from flask import Blueprint, request, jsonify, current_app, session,flash, redirect, url_for
from utilities import allowed_audio_file, UPLOAD_FOLDER, DB_NAME
import os
from utilities import extract_audio_info
from werkzeug.utils import secure_filename
import sqlite3


bp = Blueprint('upload_audio', __name__)

@bp.route('/upload/audio', methods = ["POST"])
def upload_audio():
    if session.get("id"):
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']

        if file and allowed_audio_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            audio_info = extract_audio_info(file.filename)

            size = audio_info.get('size')
            mime_type = audio_info.get('mime_type')
            upload_date = audio_info.get('upload_date')
            length_seconds = audio_info.get('length_seconds')
            bit_rate = audio_info.get('bit_rate')
            sampling_rate = audio_info.get('sampling_rate')
            channels = audio_info.get('channels')

            description = request.form["description"]
            genre = request.form["genre"]
            tags = request.form["tags"]

            try:
                conn = sqlite3.connect(DB_NAME, timeout = 10)
                cursor = conn.cursor()

                cursor.execute("INSERT INTO audios (user_id, filename, size, mime_type, upload_date, length_seconds, bit_rate, sampling_rate, channels, description, genre, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (session.get("id"), filename, size, mime_type, upload_date, length_seconds, bit_rate, sampling_rate, channels, description, genre, tags))
                conn.commit()
                conn.close()

                flash("Audio salvo com sucesso", "sucesso")
                return redirect(url_for('dashboard.dashboard'))

            except Exception as e:
                flash("Erro ao salvar informações no banco de dados", "erro")
                return redirect(url_for('dashboard.dashboard'))
            
        else:
            flash("Tipo de arquivo não permitido", "erro")
            return redirect(url_for('dashboard.dashboard'))

    else:
        flash("Você não está logado!", "erro")
        return redirect(url_for('auth.login'))

@bp.route('/audios', methods = ["POST"])
def get_audios():
    if session.get("id"):    
        try:
            conn = sqlite3.connect(DB_NAME, timeout = 10)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("select * from audios where user_id = ?", (session.get("id")))
            audios = cursor.fetchall()

            conn.commit()
            conn.close()

            if audios:
                result = []
                for audio in audios:
                    result.append(
                        {"filename" : audios.get("filename"),
                         "size" : audios.get("size"),
                         "upload_date" : audios.get("upload_date"),
                         "mime_type" : audios.get("mime_type")
                         }
                    )

            else:
                result = None

            return redirect(url_for('dashboard.dashboard', audios = result))

        except Exception as e:
            return redirect(url_for('dashboard.dashboard'))

    else:
        flash("Você não está logado!", "erro")
        return redirect(url_for('auth.login'))

@bp.route('/delete/audio/<audio_id>', methods = ["POST"])
def delete_audio(audio_id):
    if session.get("id"):    
        try:
            conn = sqlite3.connect(DB_NAME, timeout = 10)
            cursor = conn.cursor()

            cursor.execute("delete from audios where audio_id = ?", (audio_id))
            conn.commit()
            conn.close()

            flash("Áudio deletado com sucesso", "sucesso")
            return redirect(url_for('dashboard.dashboard'))

        except Exception as e:
            flash("Erro ao salvar informações no banco de dados", "erro")
            return redirect(url_for('dashboard.dashboard'))

    else:
        flash("Você não está logado!", "erro")
        return redirect(url_for('auth.login'))

@bp.route('/update/audio/<audio_id>', methods = ["POST"])
def update_audio(audio_id):
    if session.get("id"):
        description = request.form["description"]
        genre = request.form["genre"]
        tags = request.form["tags"]
            
        try:
            conn = sqlite3.connect(DB_NAME, timeout = 10)
            cursor = conn.cursor()

            cursor.execute("UPDATE audios set description = ?, genre = ?, tags = ? where audio_id = ?", (description, genre, tags, audio_id))
            conn.commit()
            conn.close()

            flash("Informações de áudio atualizado com sucesso", "sucesso")
            return redirect(url_for('dashboard.dashboard'))

        except Exception as e:
            flash("Erro ao salvar informações no banco de dados", "erro")
            return redirect(url_for('dashboard.dashboard'))

    else:
        flash("Você não está logado!", "erro")
        return redirect(url_for('auth.login'))