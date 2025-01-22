import sqlite3
import cv2
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import ffmpeg

UPLOAD_FOLDER = 'static/uploads'
VIDEO_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'videos')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov'}
DB_NAME = "snapcloud.db"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def generate_thumbnail(video_path, output_folder="static/uploads/thumbnails"):
    # Gera o thumbnail do primeiro frame do vídeo
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Abre o vídeo
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()  # Lê o primeiro frame
    if success:
        # Cria um nome seguro para o thumbnail
        filename = secure_filename(os.path.basename(video_path)).rsplit('.', 1)[0] + "_thumb.jpg"
        output_path = os.path.join(output_folder, filename)

        # Salva o frame como imagem
        cv2.imwrite(output_path, frame)
        cap.release()
        return output_path  # Retorna o caminho do thumbnail

    cap.release()
    return None

def save_video_to_db(user_id, filename, filepath, thumbnail_path):
    # Salva os dados do vídeo no banco
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO videos (user_id, filename, filepath, thumbnail_path, upload_date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, filename, filepath, thumbnail_path, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def get_user_videos(user_id):
    # Retorna os vídeos de um usuário específico
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, filename, filepath, thumbnail_path, upload_date
        FROM videos
        WHERE user_id = ?
    """, (user_id,))
    videos = cursor.fetchall()
    conn.close()
    return videos

def generate_resolutions(video_path, output_folder="static/uploads/videos/resolutions"):
    # Gera múltiplas resoluções para o vídeo
    resolutions = {
        "480p": {"width": 854, "height": 480},
        "720p": {"width": 1280, "height": 720},
        "1080p": {"width": 1920, "height": 1080},
    }

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_paths = {}

    for label, res in resolutions.items():
        output_file = os.path.join(output_folder, f"{os.path.basename(video_path).split('.')[0]}_{label}.mp4")
        ffmpeg.input(video_path).output(
            output_file, vf=f"scale={res['width']}:{res['height']}"
        ).run(quiet=True)  # para não imprimir logs no terminal
        output_paths[label] = output_file

    return output_paths

def create_folders():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(VIDEO_UPLOAD_FOLDER):
        os.makedirs(VIDEO_UPLOAD_FOLDER)

def create_tables():
    with open("schema.sql", "r") as file:
        schema = file.read()
        conn = sqlite3.connect(DB_NAME)
        conn.executescript(schema)
