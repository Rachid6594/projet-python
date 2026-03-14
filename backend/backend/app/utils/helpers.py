import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, upload_folder):
    filename = secure_filename(file.filename)
    path = os.path.join(upload_folder, filename)
    file.save(path)
    return filename
