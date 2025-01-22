import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from mutagen import File


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac'}
DB_NAME = "snapcloud.db"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_audio_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS

def get_mime_type(extension):
  media_types = {
      "jpeg": "image/jpeg",
      "jpg": "image/jpeg",
      "png": "image/png",
      "gif": "image/gif",
      "svg": "image/svg",
      "webp": "image/webp",
      "mp3": "audio/mp3",
      "wav": "audio/wav",
      "ogg": "audio/ogg",
      "flac": "audio/flac"
  }
  return media_types.get(extension.lower())

def extract_audio_info(file_path):
    try:
        filename = secure_filename(os.path.basename(file_path))
        size = os.path.getsize(file_path)  # Size in bytes
        extension = os.path.splitext(file_path)[1][1:] # Gets everything after "."
        mime_type = get_mime_type(extension)
        upload_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        
        # Load the audio file using mutagen
        audio = File(file_path)
        if not audio:
            raise ValueError("Unable to read audio file metadata.")
        
        audio_length = audio.info.length  # Length in seconds
        bit_rate = audio.info.bitrate  # Bitrate in bits per second
        sample_rate = audio.info.sample_rate  # Sampling rate in Hz
        channels = audio.info.channels  # Number of audio channels
        
        # Return the information as a dictionary
        return {
            "filename": filename,
            "size": size,
            "mime_type" : mime_type,
            "upload_date" : upload_date,
            "length_seconds": round(audio_length),
            "bit_rate": bit_rate // 1000 if bit_rate else None,  # Convert to kbps
            "sampling_rate": sample_rate,
            "channels": channels
        }
    
    except Exception as e:
        return {"error": str(e)}

def create_folders():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
