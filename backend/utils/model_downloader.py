import os
import gdown
import zipfile

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../models"))
os.makedirs(MODEL_DIR, exist_ok=True)

def download_models():
    # InSwapper
    inswapper_url = "https://drive.google.com/uc?id=1w4ZEBhD_3vojTzvaGKwgLUh7OldXgu7W"
    inswapper_path = os.path.join(MODEL_DIR, "inswapper_128.onnx")

    if not os.path.exists(inswapper_path):
        print("📥 Downloading inswapper_128.onnx...")
        gdown.download(inswapper_url, inswapper_path, quiet=False)

    # buffalo_l (ZIP folder of model weights, if zipped)
    buffalo_folder_path = os.path.join(MODEL_DIR, "buffalo_l")
    if not os.path.exists(buffalo_folder_path):
        print("📥 Downloading buffalo_l model folder...")

        # NOTE: You must zip it manually and re-upload to Drive to use this
        buffalo_zip_url = "https://drive.google.com/uc?id=1k10ucZDhFIujgE_9MwEY27zMn5J50qOf"
        buffalo_zip_path = os.path.join(MODEL_DIR, "buffalo_l.zip")

        gdown.download_folder(url=buffalo_zip_url, output=MODEL_DIR, quiet=False, use_cookies=False)
