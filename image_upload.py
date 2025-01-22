from flask import Blueprint, request, jsonify, current_app, session
from werkzeug.utils import secure_filename
import os
from PIL import Image as PILImage
from utilities import allowed_file, DB_NAME
import sqlite3
from datetime import datetime

bp = Blueprint('image_upload', __name__)

@bp.route('/upload/image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        file.save(filepath)
        
        thumbnail_filename = f"thumb_{filename}"
        thumbnail_path = os.path.join(current_app.config['UPLOAD_FOLDER'], thumbnail_filename)
        image = PILImage.open(filepath)
        image.thumbnail((100, 100))
        image.save(thumbnail_path)
        
        upload_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        user_id = session['id']
        try:
            conn = sqlite3.connect(current_app.config['DATABASE'])
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO images (filename, filepath, thumbnail, upload_date, user_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (filename, filepath, thumbnail_filename, upload_date, user_id))
            
            conn.commit()
            conn.close()

            return jsonify({
                'message': 'Image uploaded and information saved successfully',
                'filename': filename,
                'thumbnail': thumbnail_filename
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400
    
@bp.route('/images', methods=['GET'])
def get_images():
    """ Fetch all images from the 'images' table """
    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM images")
        images = cursor.fetchall()

    if not images:
        return jsonify({"error": "No images found"}), 404

    result = []
    for image in images:
        result.append({
            'id': image[0],
            'filename': image[1],
            'filepath': image[2],
            'thumbnail': image[3],
            'upload_date': image[4]
        })
    
    return jsonify(result)