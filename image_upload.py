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
        # Secure the filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Save the original file
        file.save(filepath)
        
        # Create a thumbnail of the image
        thumbnail_filename = f"thumb_{filename}"
        thumbnail_path = os.path.join(current_app.config['UPLOAD_FOLDER'], thumbnail_filename)
        image = PILImage.open(filepath)
        image.thumbnail((100, 100))  # Adjust the size of the thumbnail
        image.save(thumbnail_path)
        
        # Get the current time to store in upload_date
        upload_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insert the image information into the database using raw SQL
        user_id = 1 #session['id']
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(current_app.config['DATABASE'])
            cursor = conn.cursor()
            
            # Insert the image data into the 'images' table
            cursor.execute('''
                INSERT INTO images (filename, filepath, thumbnail, upload_date, user_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (filename, filepath, thumbnail_filename, upload_date, user_id))
            
            # Commit the changes and close the connection
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

    # If no images found, return an error message
    if not images:
        return jsonify({"error": "No images found"}), 404

    # Format the response
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