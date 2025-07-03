from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from face_swapper import swap_faces
from utils import save_upload_file

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = "../static/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/faceswap")
async def swap_faces_api(source_face: UploadFile = File(...), target_image: UploadFile = File(...)):
    source_path = save_upload_file(source_face, OUTPUT_DIR)
    target_path = save_upload_file(target_image, OUTPUT_DIR)

    output_path = os.path.join(OUTPUT_DIR, f"swapped_{target_image.filename}")
    print("Received files:", source_path, target_path)  

    success = swap_faces(source_path, target_path, output_path)

    if success:
        return FileResponse(output_path, media_type="image/jpeg")
    else:
        print("Face swap failed") 
        return JSONResponse(content={"error": "Face swap failed"}, status_code=500)

