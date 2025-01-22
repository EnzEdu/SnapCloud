from flask import Blueprint, request, jsonify, current_app, session
from werkzeug.utils import secure_filename
import os
from PIL import Image
from utilities import allowed_file, DB_NAME
import piexif
from datetime import datetime
from s3 import S3_BUCKET_NAME, S3_BUCKET_REGION, Imagem

def upload_image(obj, args):
    file = obj

    if file and allowed_file(file.filename):
        image = Image.open(file)
        dpi = image.info.get('dpi', ('Unknown', 'Unknown'))

        file_name = secure_filename(file.filename)
        file_size = file.seek(0, os.SEEK_END)
        file.seek(0, os.SEEK_SET)
        bucket_file_name = file_name
        upload_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        mime_type = file.content_type
        width = image.width
        height = image.height
        color_depth = image.mode
        resolution_dpi_x = dpi[0]
        resolution_dpi_y = dpi[1]

        exif_data = ""
        try:
            exif_dict = piexif.load(image.info['exif'])
            exif_data = {piexif.TAGS[key]: exif_dict['0th'].get(key, 'N/A') for key in exif_dict['0th']}
        except:
            exif_data = ""

        description = args[0]
        tags = args[1]
        user_id = args[3]


        img_obj = Imagem(
            id_usuario=user_id,
            s3_bucket_nome=S3_BUCKET_NAME,
            s3_bucket_regiao=S3_BUCKET_REGION,
            file_name=file_name,
            bucket_file_name=bucket_file_name,
            file_size=file_size,
            upload_date=upload_date,
            mime_type=mime_type,
            width=width,
            height=height,
            color_depth=color_depth,
            resolution_dpi_x=resolution_dpi_x,
            resolution_dpi_y=resolution_dpi_y,
            exif_data=exif_data,
            description=description,
            tags=tags
        )
        #thumbnail_filename = f"thumb_{filename}"
        #image = Image.open(file)
        #image.thumbnail((100, 100))

        return (True, img_obj)

    else:
        return (False, "")
