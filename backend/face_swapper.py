import os
import cv2
import insightface
from matplotlib import pyplot as plt

insightface.model_zoo.model_zoo.auto_download = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.abspath(os.path.join(BASE_DIR, "../models"))
SWAP_MODEL_PATH = os.path.join(MODEL_DIR, "inswapper_128.onnx")

providers = ["CPUExecutionProvider"]

face_analyser = insightface.app.FaceAnalysis(
    name="buffalo_l",
    root=MODEL_DIR,
    providers=providers,
    allowed_modules=["landmark_3d_68", "landmark_2d_106", "detection", "recognition"]
)
face_analyser.prepare(ctx_id=0, det_size=(640, 640))

swap_model = insightface.model_zoo.get_model(SWAP_MODEL_PATH, providers=providers)

def swap_faces(source_path, target_path, output_path):
    try:
        src_img = cv2.imread(source_path)
        tgt_img = cv2.imread(target_path)

        src_faces = face_analyser.get(src_img)
        tgt_faces = face_analyser.get(tgt_img)

        if not src_faces or not tgt_faces:
            print("❌ No face detected.")
            return False

        result_img = swap_model.get(
            img=tgt_img,
            target_face=tgt_faces[0],
            source_face=src_faces[0],
            paste_back=True
        )

        cv2.imwrite(output_path, result_img)
        return True
    except Exception as e:
        print(f"❌ Face swap failed: {e}")
        return False
