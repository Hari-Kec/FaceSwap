import os
import shutil
from fastapi import UploadFile

def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    file_path = os.path.join(destination, upload_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path
