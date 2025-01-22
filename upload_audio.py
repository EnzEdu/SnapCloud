from flask import Blueprint, request, jsonify, current_app, session,flash, redirect, url_for
from utilities import allowed_audio_file, DB_NAME
import os
from utilities import extract_audio_info
from werkzeug.utils import secure_filename
from s3 import S3_BUCKET_NAME, S3_BUCKET_REGION, Audio

def upload_audio(obj, args):
    file = obj

    if file and allowed_audio_file(file.filename):
        filename = secure_filename(file.filename)
        audio_info = extract_audio_info(file)

        print(audio_info)
        if audio_info.get('error') is None:
            size = audio_info.get('size')
            mime_type = audio_info.get('mime_type')
            upload_date = audio_info.get('upload_date')
            length_seconds = audio_info.get('length_seconds')
            bit_rate = audio_info.get('bit_rate')
            sampling_rate = audio_info.get('sampling_rate')
            channels = audio_info.get('channels')

            description = args[0]
            tags = args[1]
            genres = args[2]

            audio_obj = Audio(
                id_usuario=args[3],
                s3_bucket_nome=S3_BUCKET_NAME,
                s3_bucket_regiao=S3_BUCKET_REGION,
                file_name=filename,
                file_size=size,
                upload_date=upload_date,
                mime_type=mime_type,
                duration=length_seconds,
                bitrate=bit_rate,
                sample_rate=sampling_rate,
                channels=channels,
                description=description,
                tags=tags,
                genres=genres
            )
            print(audio_obj.mime_type, " ", audio_obj.upload_date, " ")

            return (True, audio_obj)

        else:
            return (False, "")
    else:
        return (False, "")