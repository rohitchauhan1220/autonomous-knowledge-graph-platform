from pathlib import Path
from werkzeug.utils import secure_filename


def save_upload(file_storage, upload_folder):
    Path(upload_folder).mkdir(exist_ok=True)
    filename = secure_filename(file_storage.filename)
    path = Path(upload_folder) / filename
    file_storage.save(path)
    return filename, path
